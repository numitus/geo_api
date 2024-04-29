### Setup
You need to copy `.env.dev` to `.env` and  set `geocode_api` key in `.env` file. You may use 
`geocode_api=662fd2bea5c75771485923hpq602dcb` for testing.

### Run the application
Execute the following command to start the application.
```
docker-compose -f docker-compose.yml up --build
```
It will start the application on port 8080.


#### Tests with curl
```
curl \
  -F "filecomment=This is an image file" \
  -F "test=@test.csv" \
  localhost:8080/api/calculateDistances
```

```
curl localhost:8080/api/getResult?task_id=xxxxx
```

### Run tests

```
pip3 install -r requirements.test.txt
pytest
```


### Setup git pre-commit-hook

```
pip3 install -r requirements.dev.txt
pre-commit install
```
