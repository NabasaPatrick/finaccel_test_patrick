# Finaccel Test Patrick Backend API

## Installation
this project can be run with or without docker

#### With Docker
to build docker image
```
docker-compose build
```

after build, run the container
```
docker-compose up -d
```
navigate to http://localhost:8090/docs to see the API docs of the project

#### without Docker
create virtual environment

```
python3 -m venv .venv
```

activate the virtual environment
```
source .venv/bin/activate
```

next install the project requirement
```
pip install -r requirements.txt
```

next run the database migration using following command
```
alembic upgrade head
```

to run the project use the following command
```
uvicorn src.main:app --port 8090 --reload
```
> Note: change the port into any desire port you want to use

navigate to http://localhost:8090/docs to access the API doc

##Project Explanation
in this project the codebase is under `/src` folder.

there is an alembic folder in root directory of the project
that folder contains the version of migration ever made for the project.

In this project i split the source code into seperate folder, each folder contains a module that use in this project.

each folder contain at least `api, schema, helpers, and model`

### api
```
the endpoint for each modules can be found in this file
```

### schema
```
this file contain the model views of each module
```

### helpers
```
this file contain the business logic of each modules
```

### model
```
this file contain the database table model of this project
```

###Assumption
when running this project we use the assumption that the user already authenticated so we dont need to login to access the api.

this project consist of 5 modules: `User, Master Limit, User Limit, Loan, and Payment`

####Master Limit
The master limit module is use to capture all data about the transaction limit like `30 days, 3mo, 6 mo and etc`

####User Limit
This module will capture all the limit that user have

####Loan
This module allow user to have a loan base of user limit. Using this module also, user can see their existing loan that give them the information of how much they need to pay this month or if they already pay their bill for this month. 

####Payment
This module allow user to pay the loan he made, each payment that user paid will change the outstanding balance and limit balance of user limit. also the payment will determine the next payment date user need to pay if their loan is not fully paid.

###Note
If user do a payment bigger than its outstanding loan. The user next loan will be deducted from the overpaid that the user has made 
