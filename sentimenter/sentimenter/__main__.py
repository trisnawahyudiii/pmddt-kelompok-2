from flask import jsonify
from sentimenter import create_app

app = create_app()

@app.route('/', methods=["GET"])
def index():
    return "ok"

@app.route('/users', methods=["GET"])
def get_all_users():
    all_users = [{"id": 1, "name": "trisna"}, {"id": 2, "name": "purnami"}, {"id": 3, "name": "rev"}]
    return jsonify(all_users)

if __name__ == "__main__":
    app.run(host="127.0.0.1")