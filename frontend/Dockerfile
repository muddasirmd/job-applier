FROM node:20-alpine
WORKDIR /app
COPY job-applier-app/package*.json ./
RUN npm ci
COPY job-applier-app .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]
