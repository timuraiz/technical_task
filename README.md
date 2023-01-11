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
>>>>>>> 5460b7a (Update)
```
docker-compose build
docker-compose up
```
<<<<<<< HEAD
And if you want to see logs, just put such command(recommended)

```
docker-compose logs -f
```

## How to see results?
- To see results you need to come to this address http://0.0.0.0:8000/docs
=======
- And go to this web page http://0.0.0.0:8000/docs
>>>>>>> 5460b7a (Update)
