#stage 1: build
FROM node:18.20.2-alpine as builder

# set work directory, all commands will be run under this directory
WORKDIR /frontend

# copy dependecies to current work directory
COPY package*.json ./

# instll dependencies
# RUN npm config set registry https://registry.npm.taobao.org
RUN npm install

# copy all files to work directory
COPY . .

# run build to generate static files
RUN npm run build

# stage 2: run
FROM nginx:stable-alpine as runtime

# copy static files to nginx directory
COPY --from=builder /app/build /usr/share/nginx/html

# optional custom configuration
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# expose port 80, which nginx listen by default
EXPOSE 80

# run nginx
CMD ["nginx", "-g", "daemon off;"]