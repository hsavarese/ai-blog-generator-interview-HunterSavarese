from flask import Flask, jsonify, request, render_template
from seo_fetcher import get_seo_metrics
from ai_generator import generate_blog_post
import os
import json
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__) 
TEMPLATE = 'index.html' #template for home page

@app.route('/') #route for home page
def home():
    return render_template(TEMPLATE)

@app.route('/generate', methods=['GET']) #route for generating blog post
def generate(): 
    keyword = request.args.get('keyword', '') 
    if not keyword:
        return render_template(TEMPLATE) #if no keyword, render home page
    
    # gets SEO metrics
    metrics = get_seo_metrics(keyword)
    post = generate_blog_post(keyword, metrics)  # generates blog post
    # returns both metrics and post
    return render_template(TEMPLATE, keyword=keyword, metrics=metrics, post=post)

@app.route('/templates/example_wireless_earbuds')
def example_wireless_earbuds():
    keyword = "wireless earbuds"
    metrics = get_seo_metrics(keyword)
    post = generate_blog_post(keyword, metrics)
    return render_template('example_wireless_earbuds.html', post=post)



def generate_daily_post():
    keyword = "wireless earbuds"
    try:
        metrics = get_seo_metrics(keyword)
        post = generate_blog_post(keyword, metrics)
        save_generated_post(keyword, metrics, post)  # Only save daily posts
        print(f"Daily post generated and saved for keyword: {keyword}")
    except Exception as e:
        print(f"Error generating daily post: {e}")


def save_generated_post(keyword, metrics, post):
    timestamp=datetime.now().strftime("%Y-%m-%d %H-%M-%S") #get current timestamp
    filename=f"{timestamp}_{keyword.lower().replace(' ', '_')}.json" #create filename with timestamp and keyword
    filepath=os.path.join("generated_posts", filename) 
    data={
        "timestamp":timestamp,
        "keyword":keyword,
        "metrics":metrics,
        "post":post
    }

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    #save generated post to database
    

if __name__ == '__main__': #run app
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=generate_daily_post, trigger="cron", hour=3, minute=0)
    scheduler.start()
    app.run(debug=True)

