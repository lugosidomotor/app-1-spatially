from flask import Flask
import os
import base64
import requests
import psycopg2
from kubernetes import client, config

app = Flask(__name__)

def get_kubernetes_secret(secret_name, key_name, namespace='default'):
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    secret = v1.read_namespaced_secret(secret_name, namespace)
    return secret.data[key_name]

def decode_base64_twice(encoded_value):
    first_decode = base64.b64decode(encoded_value)
    second_decode = base64.b64decode(first_decode)
    return second_decode.decode('utf-8')

def get_keyvault_secret(vault_address, secret_name):
    # This function should include authentication details to access the key vault
    # Assuming it's an HTTP GET request for the example
    response = requests.get(f"{vault_address}/secrets/{secret_name}")
    return response.json()['value']

def create_table_if_not_exists(connection_string):
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS app_data (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def write_to_db(connection_string, data):
    conn = psycopg2.connect(connection_string)
    cur = conn.cursor()
    create_table_if_not_exists(connection_string)
    cur.execute("INSERT INTO app_data (content) VALUES (%s)", (data,))
    conn.commit()
    cur.close()
    conn.close()

def initialize_database():
    try:
        encoded_vault_address = get_kubernetes_secret("keyvault-address", "vault-address")
        vault_address = decode_base64_twice(encoded_vault_address)
        postgres_connection_string = get_keyvault_secret(vault_address, "postgres-connection-string")
        with open("data.txt", "r") as file:
            content = file.read()
        write_to_db(postgres_connection_string, content)
        print("Data written to database successfully.")
    except Exception as e:
        print(f"Error: {str(e)}")

@app.route("/")
def hello_world():
    try:
        with open("data.txt", "r") as file:
            content = file.read()
    except FileNotFoundError:
        content = "Data file not found."

    return f"<h1>app-1-spatially</h1><p>{content}</p>"

if __name__ == "__main__":
    initialize_database()
    app.run(host='0.0.0.0', port=8080, debug=True)

