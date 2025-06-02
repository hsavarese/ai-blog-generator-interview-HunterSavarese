import random

def get_seo_metrics(keyword):

    return {
        "search_volume": random.randint(100, 10000), #random number between 100 and 10000
        "keyword_difficulty": round(random.uniform(0.1, 1.0), 2), #random decimal between 0.1 and 1.0
        "avg_cpc": round(random.uniform(0.5, 5.0), 2) # rounds the decimal to 2 places
    }

if __name__ == "__main__":
    test_keyword = ""
    metrics = get_seo_metrics(test_keyword)
    print(f"SEO Metrics for '{test_keyword}':")
    print(f"Search Volume: {metrics['search_volume']}")
    print(f"Keyword Difficulty: {metrics['keyword_difficulty']}")
    print(f"Average CPC: ${metrics['avg_cpc']}")

