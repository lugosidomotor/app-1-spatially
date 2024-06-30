from flask import Flask
import os
import time
import base64
import requests
import psycopg2
from kubernetes import client, config
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app = Flask(__name__)

def get_kubernetes_secret(secret_name, key_name, namespace='default'):
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    try:
        secret = v1.read_namespaced_secret(secret_name, namespace)
        if key_name in secret.data:
            return secret.data[key_name]
        else:
            raise KeyError(f"Key '{key_name}' not found in secret '{secret_name}'")
    except Exception as e:
        print(f"Error accessing secret {secret_name}: {e}")
        raise

def decode_base64_twice(encoded_value):
    try:
        first_decode = base64.b64decode(encoded_value)
        second_decode = base64.b64decode(first_decode)
        return second_decode.decode('utf-8')
    except Exception as e:
        print(f"Error decoding base64 value: {e}")
        raise

def get_keyvault_secret(vault_address, secret_name):
    try:
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=vault_address, credential=credential)
        secret = client.get_secret(secret_name)
        return secret.value
    except Exception as e:
        print(f"Error accessing key vault: {e}")
        raise

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
    retries = 5
    delay = 100  # seconds
    attempt = 0

    while attempt < retries:
        try:
            encoded_vault_address = get_kubernetes_secret("keyvault-address", "address")
            print(f"Encoded vault address: {encoded_vault_address}")
            vault_address = decode_base64_twice(encoded_vault_address)
            print(f"Decoded vault address: {vault_address}")
            postgres_connection_string = get_keyvault_secret(vault_address, "postgres-connection-string")
            print(f"Postgres connection string: {postgres_connection_string}")
            with open("data.txt", "r") as file:
                content = file.read()
            write_to_db(postgres_connection_string, content)
            print("Data written to database successfully.")
            break
        except Exception as e:
            print(f"Error: {str(e)}")
            attempt += 1
            if attempt < retries:
                print(f"Retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})")
                time.sleep(delay)
            else:
                print("All retry attempts failed.")

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
