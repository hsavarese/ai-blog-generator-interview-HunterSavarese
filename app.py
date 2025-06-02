from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "test to see if this works"})

if __name__ == '__main__':
    app.run(debug=True)
