ifneq (,$(wildcard ./.env))
    include .env
    export
endif

SHELL:= /bin/bash
# Current datetime for unique purposes
CURRENT_DATETIME:=$(shell date +%Y-%m-%d-%H-%M-%S)
# Config ID for the Gateway
WEB_API_CONFIG:="web-api-config-$(CURRENT_DATETIME)"
SHORT_COMMIT_SHA:=$(shell git rev-parse --short HEAD)
IMAGE_PREFIX:=us.gcr.io/${GOOGLE_CLOUD_PROJECT}/ai_chat
BOT_IMAGE:=${IMAGE_PREFIX}/bot-image:${SHORT_COMMIT_SHA}
WEB_IMAGE:=${IMAGE_PREFIX}/web-image:${SHORT_COMMIT_SHA}


configure:
	@echo '${SERVICE_ACCOUNT}' > keyfile.txt
	gcloud auth activate-service-account --key-file keyfile.txt; rm keyfile.txt

build-web:
	gcloud --project ${GOOGLE_CLOUD_PROJECT} builds submit ./web --region ${GOOGLE_CLOUD_REGION} --suppress-logs --tag ${WEB_IMAGE}

build-bot:
	gcloud --project ${GOOGLE_CLOUD_PROJECT} builds submit ./bot --region ${GOOGLE_CLOUD_REGION} --suppress-logs --tag ${BOT_IMAGE}

deploy-bot:
	gcloud --project ${GOOGLE_CLOUD_PROJECT} run deploy telegram-bot --allow-unauthenticated --region ${GOOGLE_CLOUD_REGION} --image ${BOT_IMAGE} && \
	gcloud --project ${GOOGLE_CLOUD_PROJECT} run services update-traffic telegram-bot --to-latest --region ${GOOGLE_CLOUD_REGION}

deploy-web:
	gcloud --project ${GOOGLE_CLOUD_PROJECT} run deploy web --no-allow-unauthenticated --region ${GOOGLE_CLOUD_REGION} --image ${WEB_IMAGE} && \
    gcloud --project ${GOOGLE_CLOUD_PROJECT} run services update-traffic web --to-latest --region ${GOOGLE_CLOUD_REGION}

deploy-api-gateway:
	@echo "Use new config $(WEB_API_CONFIG)"
	gcloud --project ${GOOGLE_CLOUD_PROJECT} api-gateway api-configs create $(WEB_API_CONFIG) --api=web-api \
		--openapi-spec=infra/web_api_config.yml --backend-auth-service-account=api-gateway@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com \
		&& \
	gcloud --project ${GOOGLE_CLOUD_PROJECT} api-gateway gateways update web-api-gw --api=web-api \
	--api-config=${WEB_API_CONFIG} --location=${GOOGLE_CLOUD_REGION} \


deploy: deploy-web deploy-bot
build: build-web build-bot
all: build deploy
web: build-web deploy-web
bot: build-bot deploy-bot
