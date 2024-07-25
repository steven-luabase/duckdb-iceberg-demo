# DuckDB Flask App
This directory contains a Flask app that runs SQL queries with DuckDB against files in Google Cloud Storage. 


## Configuration Setup
To setup edit `config.py`:
```
PROJECT_ID = "<YOUR_PROJECT_ID>"
HMAC_KEY = "<YOUR_HMAC_KEY>"
HMAC_SECRET_KEY_NAME = "<YOUR_HMAC_SECRET_KEY_NAME>"
```
Create an HMAC key and secret for your Google Cloud Storage buckets [here](https://cloud.google.com/storage/docs/authentication/managing-hmackeys#create). Store your HMAC secret in Google Secrets Manager and put the name of the secret as HMAC_SECRET_KEY_NAME and the HMAC key as HMAC_KEY in `config.py`

## Deploy the app to Cloud Run
```
bash build_cloud_run.sh
```

## Query Files in GCS
```
import requests 

sql = f'''
select 
    count(*)
from read_parquet('gs://<OTHER_BUCKET>/some_data.parquet');
'''

url = '<CLOUD_RUN_URL>/queryquery'
query = {
    "query": sql
}
response = requests.post(url, params=query)
response.json()
```