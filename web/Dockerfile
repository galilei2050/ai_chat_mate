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

# Build the application
RUN npm run build

# Stage 2: Serve the application from the build folder
FROM node:lts AS serve

WORKDIR /app

# Copy the build folder from the build stage
COPY --from=build /app/package*.json ./
COPY --from=build /app/build ./build

# Run the application
CMD node build