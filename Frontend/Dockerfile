# 1. Use Node.js to build the website
FROM node:18-alpine

# 2. Set working directory
WORKDIR /app

# 3. Copy the package.json file
COPY package.json .

# 4. Install the tools
RUN npm install

# 5. Copy the rest of the code
COPY . .

# 6. Open Port 5173
EXPOSE 5173

# 7. Start the React server
CMD ["npm", "run", "dev", "--", "--host"]