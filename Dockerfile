FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Expose port
EXPOSE 80

# Set environment variables
ENV NODE_ENV=production

# Start the application
CMD ["npm", "start"]