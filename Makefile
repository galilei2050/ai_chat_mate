ifneq (,$(wildcard ./.env))
    include .env
    export
endif

SHELL:= /bin/bash
# Current datetime for unique purposes
CURRENT_DATETIME:=$(shell date +%Y-%m-%d-%H-%M-%S)
# Config ID for the Gateway
WEB_API_CONFIG:="web-api-config-$(CURRENT_DATETIME)"


configure:
	@echo '${SERVICE_ACCOUNT}' > keyfile.txt
	gcloud auth activate-service-account --key-file keyfile.txt; rm keyfile.txt

build-web:
	gcloud --project ${PROJECT_ID} builds submit ./web --region ${REGION} --suppress-logs --tag ${IMAGE_PREFIX}/web-image:latest

build-bot:
	gcloud --project ${PROJECT_ID} builds submit . --region ${REGION} --suppress-logs --tag ${IMAGE_PREFIX}/bot-image:latest

deploy-bot:
	gcloud --project ${PROJECT_ID} run deploy telegram-bot --region ${REGION} --image ${IMAGE_PREFIX}/bot-image:latest --max-instances=1 --memory=512Mi --cpu=1 --port=8080

deploy-web:
	gcloud --project ${PROJECT_ID} run deploy web --no-allow-unauthenticated --region ${REGION} --image ${IMAGE_PREFIX}/web-image:latest --max-instances=1 --memory=256Mi --cpu=1

deploy-api-gateway:
	@echo "Use new config $(WEB_API_CONFIG)"
	gcloud --project ${PROJECT_ID} api-gateway api-configs create $(WEB_API_CONFIG) --api=web-api --openapi-spec=infra/web_api.yml
	gcloud --project ${PROJECT_ID} api-gateway gateways update web-api-gw --api=web-api --api-config=${WEB_API_CONFIG} --location=${REGION}

deploy: deploy-web deploy-bot
build: build-web build-bot
all: build deploy
web: build-web deploy-web
bot: build-bot deploy-bot
