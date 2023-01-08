# technical_task

## To run docker you need:
- configure env file:
  - create your own postgres database
  - put into file all required settings of this database(change variables where first part of var is 'POSTGRES')
## After all you can run the docker
```
docker-compose build
docker-compose up -d
```
And if you want to see logs, just put such command(recommended)

```
docker-compose logs -f
```

## How to see results?
- To see results you need to come to this address http://0.0.0.0:8000/docs