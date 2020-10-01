FROM node:13.12.0-alpine

# set working directory
RUN mkdir /app
WORKDIR /app

# install app dependencies
COPY package.json .
# COPY package-lock.json .
RUN npm install
# RUN npm install react-scripts@3.4.1 -g

# add app
COPY . .

# start app
CMD ["npm", "start"]
