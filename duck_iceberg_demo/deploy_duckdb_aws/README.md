# DuckDB AWS Flask App
This directory contains a Flask app that runs SQL queries with DuckDB against files in AWS S3. 


## Configuration Setup
To setup edit `config.py`:
```
ACCESS_KEY = "<AWS_ACCESS_KEY>"
SECRET_KEY_NAME = "<AWS_SECRET_KEY_NAME>"
S3_BUCKET_REGION = "<S3_BUCKET_REGION>"
SECRET_REGION = "<SECRET_REGION>"
```
Get your AWS Access and Secret Keys. Store your Secret Key in AWS [Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/create_secret.html) and put the name of the secret in `config.py` for the `SECRET_KEY_NAME` variable.

## Running The App Locally
You may need to authenticate with the AWS CLI first:
```
aws sso login
```
####  Using Flask
`python main.py`
#### In Docker
Build with linux/amd64 architecture to be compatible with AWS ECS.
```
docker buildx build --platform=linux/amd64  -t duckdb-deploy .
```
```
docker run -p 5000:5000 -v ~/.aws:/root/.aws -it duckdb-deploy
```

## Deploy the app to AWS ECS
See blog post: [**Running Iceberg and Serverless DuckDB in AWS**](https://www.definite.app/blog/cloud-iceberg-duckdb-aws)

## Query Files in S3
```
import requests 

sql = f'''
select 
    count(*)
from read_parquet('s3://<BUCKET_PATH>/some_data.parquet');
'''

url = 'http://127.0.0.1:5000/query' # if running locally
query = {
    "query": sql
}
response = requests.post(url, params=query)
response.json()
```