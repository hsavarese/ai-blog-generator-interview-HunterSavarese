from flask import Flask, jsonify, request, render_template
from seo_fetcher import get_seo_metrics
from ai_generator import generate_blog_post

app = Flask(__name__)
TEMPLATE = 'index.html'

@app.route('/')
def home():
    return render_template(TEMPLATE)

@app.route('/generate', methods=['GET'])
def generate():
    keyword = request.args.get('keyword', '')
    if not keyword:
        return render_template(TEMPLATE)
    
    # gets SEO metrics
    metrics = get_seo_metrics(keyword)
    
    # generates blog post
    post = generate_blog_post(keyword, metrics)
    
    # returns both metrics and post
    return render_template(TEMPLATE, keyword=keyword, metrics=metrics, post=post)

if __name__ == '__main__':
    app.run(debug=True)
