# Maximus 

A simple project that has the following features: 

**A user can:**
1. sign up
2. sign in 
3. have other users as friends 
4. create a decision topic 
5. recieve a request to fill in preferences 
6. fill in preference on a decision topic


## Tech Stack 

- Django + Django Rest Framework
The backend of the microservices 

- VueJs + Vuetify + Vuex + Axios 
The frontend of the project 

- Docker
Containerization for services 

- Kubernetes
Container orchestration 

- Ambassador 
API Gateway for the microservices

- RabbitMQ
A message queue 


## Microservices 

1. User Service
Registeration/Login/Tokens/Friends

2. Auth Service 
Authenticate every request

3. Survey Service 
Create/process surveys 
