from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello! Welcome to my DevOps Intern Project. I am ready to learn and contribute!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)