# Stage 1: Test runner
FROM node:20-alpine AS test

WORKDIR /app

# Copy package files and install dependencies
COPY package.json ./
RUN npm install

# Copy the rest of the app files
COPY . .

# Set the command to run tests
CMD ["npm", "test"]


# Stage 2: Production server
FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf

# Copy static files from the source context
COPY . /usr/share/nginx/html

