# This repo contains code referenced in the following blog posts
- [**How We Migrated Our Data Warehouse from Snowflake to DuckDB**](https://www.definite.app/blog/duckdb-datawarehouse)
- [**Why Databricks paid $1B for a 40 person startup (Tabular)**](https://www.definite.app/blog/databricks-tabular-acquisition)
- [**Comparing Iceberg Query Engines**](https://www.definite.app/blog/iceberg-query-engine)
- [**Running Iceberg and Serverless DuckDB in Google Cloud**](https://www.definite.app/blog/cloud-iceberg-duckdb)
- [**Running Iceberg and Serverless DuckDB in AWS**](https://www.definite.app/blog/cloud-iceberg-duckdb-aws)


# Installation
To install all dependencies run:
```
poetry install
```

# DuckDB Flask App
A simple Flask app for running DuckDB in GCP and AWS can be found in `duck_iceberg_demo/deploy_duckdb_gcp` and `duck_iceberg_demo/deploy_duckdb_aws`