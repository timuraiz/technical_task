# Social Networking Application

## Prerequisites
- Install PostgreSQL (I use PostgreSQL 12.13)
- Install Docker (I use Docker 20.10.12)
- Create database in PostgreSQL

## To run project:
- Configure .env file:
  - Put into .env file settings of your PostgreSQL db
  - Take API_KEY from emailhunter.co and put into .env file
- After all run such commands in src dir:
```
docker-compose build
docker-compose up
```
- To see results you need to come to this address http://0.0.0.0:8000/docs

# Additional task

- In file tasks/task_2.py implementation of endpoint that can accept an unencoded link as a parameter and return it encoded
- source link https://www.urlencoder.io/python/
