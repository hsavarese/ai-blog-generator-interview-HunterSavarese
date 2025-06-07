import pytest
from app import app
from seo_fetcher import get_seo_metrics
from ai_generator import generate_blog_post
from app import save_generated_post
import os
from app import generate_daily_post
from apscheduler.schedulers.background import BackgroundScheduler
from unittest.mock import patch 






@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test the home page loads correctly"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Blog Post Generator' in response.data

def test_generate_endpoint_no_keyword(client):
    """Test generate endpoint without keyword returns home page"""
    response = client.get('/generate')
    assert response.status_code == 200
    assert b'Blog Post Generator' in response.data

def test_generate_endpoint_with_keyword(client):
    """Test generate endpoint with keyword returns blog post"""
    response = client.get('/generate?keyword=test')
    assert response.status_code == 200
    assert b'test' in response.data.lower()

def test_seo_metrics():
    """Test SEO metrics function returns expected data"""
    metrics = get_seo_metrics('test keyword')
    assert isinstance(metrics, dict)
    assert 'search_volume' in metrics
    assert 'keyword_difficulty' in metrics
    assert 'avg_cpc' in metrics
    assert isinstance(metrics['search_volume'], int)
    assert isinstance(metrics['keyword_difficulty'], float)
    assert isinstance(metrics['avg_cpc'], float)

def test_blog_generation():
    """Test blog post generation returns expected format"""
    metrics = get_seo_metrics('test keyword')
    post = generate_blog_post('test keyword', metrics)
    assert isinstance(post, str)
    assert len(post) > 0
    # Check for common blog post elements
    assert '###' in post  # Check for markdown title
    assert 'https://example.com/affiliate/' in post  # Check for affiliate links
    assert len(post.split()) > 100  # Check for reasonable length (more than 100 words)

def test_example_wireless_earbuds(client):
    """Test example wireless earbuds page loads"""
    response = client.get('/templates/example_wireless_earbuds')
    assert response.status_code == 200
    assert b'Wireless Earbuds' in response.data

def test_generate_endpoint_with_keyword(client):
    """Test generate endpoint with keyword returns blog post"""
    response = client.get('/generate?keyword=test')
    assert response.status_code == 200
    assert b'test' in response.data.lower()

def test_generate_endpoint_with_keyword_and_affiliate_links(client):
    """Test generate endpoint with keyword and affiliate links returns blog post"""
    response = client.get('/generate?keyword=test&affiliate_links=true')
    assert response.status_code == 200
    assert b'test' in response.data.lower()
    assert b'https://example.com/affiliate/' in response.data



def test_example_wireless_earbuds_endpoint(client):
    """Test example wireless earbuds endpoint returns blog post"""
    response = client.get('/templates/example_wireless_earbuds')
    assert response.status_code == 200
    assert b'Wireless Earbuds' in response.data



def test_generate_daily_post():
    """Test daily post generation"""
    keyword = "wireless earbuds"
    metrics = get_seo_metrics(keyword)
    post = generate_blog_post(keyword, metrics)
    assert isinstance(post, str)
    assert len(post) > 0
    assert 'Title:' in post or 'title:' in post.lower()
    assert 'https://example.com/affiliate/' in post
    assert len(post.split()) > 100

def test_save_generated_post():
    """Test save generated post"""
    os.makedirs("generated_posts", exist_ok=True) # Create generated_posts directory if it doesn't exist
    
    keyword = "wireless earbuds"
    metrics = get_seo_metrics(keyword)
    post = generate_blog_post(keyword, metrics)
    save_generated_post(keyword, metrics, post)
    
    files = [f for f in os.listdir("generated_posts") if keyword.lower().replace(' ', '_') in f]
    assert len(files) > 0, "No file was created with the keyword in its name"
    assert os.path.getsize(os.path.join("generated_posts", files[0])) > 0
    

    for file in files:
        os.remove(os.path.join("generated_posts", file)) # Clean up test-generated files

def test_generate_daily_post_with_scheduler():
    """Test daily post generation with scheduler"""
    with app.test_request_context('/generate?keyword=test'):
        generate_daily_post()
        files = [f for f in os.listdir("generated_posts") if f.endswith('.json')] # Check if a new post was generated
        assert len(files) > 0, "No daily post was generated"

    
def test_app_error_handling(client):
    """Test app error handling"""
    response = client.get('/generate?keyword=')
    assert response.status_code == 200
    assert b'Blog Post Generator' in response.data

    with app.test_request_context('/generate?keyword=test'):
        metrics = get_seo_metrics('test')
        post = generate_blog_post('test', metrics)
        assert isinstance(post, str)
        assert len(post) > 0

def test_scheduler_configuration():
    """Test that the scheduler is properly configured with the daily post generation job"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=generate_daily_post, trigger="cron", hour=3, minute=0)
    
    scheduler.start()
    
    jobs = scheduler.get_jobs()
    assert len(jobs) == 1, "Scheduler should have exactly one job"
    
    job = jobs[0]
    assert job.func == generate_daily_post, "Job should be configured to run generate_daily_post"
    
    assert str(job.trigger) == "cron[hour='3', minute='0']", "Job should be scheduled for 3:00 AM"
    
    scheduler.shutdown()

def test_seo_fetcher_error_handling():
    """Test SEO fetcher error handling"""
    metrics = get_seo_metrics("")
    assert isinstance(metrics, dict)
    assert all(key in metrics for key in ['search_volume', 'keyword_difficulty', 'avg_cpc'])
    assert all(isinstance(value, (int, float)) for value in metrics.values())

def test_ai_generator_error_handling():
    """Test AI generator error handling"""
    with patch('ai_generator.client') as mock_client:
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        post = generate_blog_post("test", {"search_volume": 1000, "keyword_difficulty": 0.5, "avg_cpc": 1.0})
        assert "Error generating blog post" in post
        assert "API Error" in post

def test_seo_fetcher_api_error():
    """Test SEO fetcher API error handling"""
    with pytest.raises(Exception):
        get_seo_metrics(None)

def test_ai_generator_api_error():
    """Test AI generator API error handling"""
    with pytest.raises(Exception):
        generate_blog_post(None, None)

def test_app_scheduler_startup():
    """Test app scheduler startup"""
    with app.test_request_context():
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=generate_daily_post, trigger="cron", hour=3, minute=0)
        scheduler.start()
        assert scheduler.running
        scheduler.shutdown()

def test_app_scheduler_shutdown():
    """Test app scheduler shutdown"""
    with app.test_request_context():
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=generate_daily_post, trigger="cron", hour=3, minute=0)
        scheduler.start()
        scheduler.shutdown()
        assert not scheduler.running

def test_app_example_endpoint(client):
    """Test example endpoint"""
    response = client.get('/templates/example_wireless_earbuds')
    assert response.status_code == 200
    assert b'Wireless Earbuds' in response.data

def test_app_generate_with_affiliate(client):
    """Test generate endpoint with affiliate links"""
    response = client.get('/generate?keyword=test&affiliate_links=true')
    assert response.status_code == 200
    assert b'test' in response.data.lower()
    assert b'https://example.com/affiliate/' in response.data

def test_generate_daily_post_error_handling():
    """Test generate daily post error handling"""
    with patch('app.get_seo_metrics', side_effect=Exception("Test error")), \
         patch('builtins.print') as mock_print:
        generate_daily_post()
        mock_print.assert_called_once_with("Error generating daily post: Test error")

def test_generate_endpoint_empty_keyword(client):
    """Test generate endpoint with empty keyword returns home page"""
    response = client.get('/generate?keyword=')
    assert response.status_code == 200
    assert b'Blog Post Generator' in response.data

def test_save_generated_post_error():
    """Test save generated post error handling"""
    with pytest.raises(Exception):
        save_generated_post(None, None, None)

def test_generate_daily_post_error():
    """Test generate daily post error handling"""
    with patch('app.get_seo_metrics', side_effect=Exception("Test error")), \
         patch('builtins.print') as mock_print:
        generate_daily_post()
        mock_print.assert_called_once_with("Error generating daily post: Test error")

def test_seo_fetcher_main():
    """Test SEO fetcher main function"""
    test_keywords = ["beats", "headphones", "unknown_keyword"]
    for keyword in test_keywords:
        metrics = get_seo_metrics(keyword)
        assert isinstance(metrics, dict)
        assert all(key in metrics for key in ['search_volume', 'keyword_difficulty', 'avg_cpc'])

def test_setup_test_env(setup_test_env):
    """Test setup_test_env fixture"""
    # Test that OPENAI_API_KEY is set
    assert os.getenv('OPENAI_API_KEY'), "OPENAI_API_KEY not found in environment variables"
    
    # Test that generated_posts directory exists
    assert os.path.exists('generated_posts'), "generated_posts directory not created"
    
    # Test the assertion in conftest.py line 20
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(AssertionError) as exc_info:
            assert os.getenv('OPENAI_API_KEY'), "OPENAI_API_KEY not found in environment variables"
        assert "OPENAI_API_KEY not found in environment variables" in str(exc_info.value)

def test_generate_endpoint_empty_keyword_handling(client):
    """Test generate endpoint with empty keyword handling"""
    response = client.get('/generate?keyword=')
    assert response.status_code == 200
    assert b'Blog Post Generator' in response.data




   

    