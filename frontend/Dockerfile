# Change from node:18-alpine to node:22-alpine
FROM node:22-alpine

WORKDIR /app

# Copy package files first for better caching
COPY package*.json ./

RUN npm install

# Copy source code
COPY . .

# Expose the port defined in vite.config.ts
EXPOSE 3000

# Start development server
CMD ["npm", "run", "dev", "--", "--host"]