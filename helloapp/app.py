from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    try:
        with open("data.txt", "r") as file:
            content = file.read()
    except FileNotFoundError:
        content = "Data file not found."
    return f"<h1>app-1-spatially</h1><p>{content}</p>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
