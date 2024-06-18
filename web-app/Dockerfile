# Use the official Node.js image from the Docker Hub
FROM node:16-slim

# Set the working directory
WORKDIR /app

# Copy the package.json and package-lock.json
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 5173

# Command to run the Vite app
CMD ["npm", "run", "dev", "--", "--host"]
