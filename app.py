from flask import Flask, jsonify, request, render_template
from seo_fetcher import get_seo_metrics

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/test', methods=['GET']) #when you go to the url /test , it will return the message
def test():
    return jsonify({"message": "test to see if this works"})

@app.route('/seo', methods=['GET'])
def get_seo():
    keyword = request.args.get('keyword', '')
    if not keyword:
        return render_template('index.html')
    
    metrics = get_seo_metrics(keyword)
    return render_template('index.html', keyword=keyword, metrics=metrics)

if __name__ == '__main__':
    app.run(debug=True)
