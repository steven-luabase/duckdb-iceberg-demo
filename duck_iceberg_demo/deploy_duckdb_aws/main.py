import duckdb
from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import ClientError
import config
import json



app = Flask(__name__)

# gets secrets from aws secret manager
def get_secret(secret_name, region_name):
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    secret = json.loads(get_secret_value_response['SecretString'])
    return secret.get('secret_key')


def init_duckdb_connection():
    access_key = config.ACCESS_KEY
    secret_key = get_secret(config.SECRET_KEY_NAME, config.SECRET_REGION)
    con = duckdb.connect()
    setup_sql = f"""
        INSTALL iceberg;
        LOAD iceberg;

        INSTALL httpfs;
        LOAD httpfs;

        CREATE SECRET (
            TYPE S3,
            KEY_ID '{access_key}',
            SECRET '{secret_key}',
            REGION '{config.S3_BUCKET_REGION}'
        );
    """
    con.execute(setup_sql)
    return con


# global duckdb connection
duckdb_conn = init_duckdb_connection()


@app.route("/query", methods=["POST"])
def query_iceberg():
    try:
        query = request.args.get("query")
        if not query:
            return jsonify({"error": "Query parameter 'query' is required"}), 400
        result = duckdb_conn.execute(query).fetchall()
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
