FROM node:14
WORKDIR /code

ARG creds

# add and install dependencies
COPY CCCAssignment2/db_api/package*.json ./
RUN npm install

# add app code
COPY CCCAssignment2/db_api/ ./

# add credentials
COPY $creds "/src/credentials.json"

# run
CMD npm start
