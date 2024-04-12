# Stage 1: Build the application
FROM node:lts AS build

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./
COPY tsconfig.json ./

# Install dependencies
RUN npm install

# Copy the rest of your application's source code
COPY . .

COPY .env.example .env
# Build the application
RUN npm run build

# Stage 2: Serve the application from the build folder
FROM node:lts AS serve

WORKDIR /app

# Copy the build folder from the build stage
COPY --from=build //package*.json ./
COPY --from=build //build ./build

# Install prod dependencies. They are not included into the build folder
RUN npm install --prod

# Run the application
CMD node build