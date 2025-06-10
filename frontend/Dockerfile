# Frontend Dockerfile for React Todo App
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Set environment variables
ENV PATH /app/node_modules/.bin:$PATH
ENV REACT_APP_API_BASE_URL=http://localhost:5001/api

# Install dependencies
COPY package*.json ./
RUN npm ci --only=production --silent

# Copy application code
COPY . .

# Build for production (optional, for production builds)
# RUN npm run build

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:3000 || exit 1

# Command to run the application
CMD ["npm", "start"]