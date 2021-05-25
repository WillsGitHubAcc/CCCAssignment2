FROM node:14
WORKDIR /code

# add and install dependencies
COPY package*.json ./
RUN npm install

# add app code
COPY . ./

# run
CMD npm start