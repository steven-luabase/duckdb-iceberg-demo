import duckdb
from flask import Flask, request, jsonify
from google.cloud import secretmanager
import config


app = Flask(__name__)

# gets secrets from google secret manager
def get_secret(secret_name: str, project_id: str):
    client = secretmanager.SecretManagerServiceClient()
    secret = client.access_secret_version(
        name=f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    )
    return secret.payload.data.decode("utf-8")


def init_duckdb_connection():
    hmac_key = config.HMAC_KEY
    hmac_secret = get_secret(config.HMAC_SECRET_KEY_NAME, config.PROJECT_ID)
    con = duckdb.connect()
    setup_sql = f"""
        INSTALL iceberg;
        LOAD iceberg;

        INSTALL httpfs;
        LOAD httpfs;

        CREATE SECRET (
            TYPE GCS,
            KEY_ID '{hmac_key}',
            SECRET '{hmac_secret}'
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
    app.run(debug=True)