FROM node:14
WORKDIR /code

ARG creds

# add and install dependencies
COPY CCCAssignment2/client/package*.json ./
RUN npm install

# add app code
COPY CCCAssignment2/client/ ./

# add credentials
COPY $creds "src/credentials.json"

# run
CMD npm start
