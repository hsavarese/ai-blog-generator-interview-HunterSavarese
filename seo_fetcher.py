import json
import os

def get_seo_metrics(keyword):
    data_dir = os.path.join(os.path.dirname(__file__), "data") #get the path to the data directory
    json_path = os.path.join(data_dir, "seo_data.json") #get the path to the seo_data.json file

    with open(json_path, "r") as file:
        seo_data = json.load(file)
    
    keyword = keyword.lower() #convert keyword to lowercase
    return seo_data.get(keyword, seo_data['default']) #return metrics for keyword or default if not found

if __name__ == "__main__":
    test_keywords = ["beats", "headphones", "unknown_keyword"] #testing with different keywords
    
    for keyword in test_keywords:
        try:
            metrics = get_seo_metrics(keyword)
            print(f"\nSEO Metrics for '{keyword}':")
            print(f"Search Volume: {metrics['search_volume']}")
            print(f"Keyword Difficulty: {metrics['keyword_difficulty']}")
            print(f"Average CPC: ${metrics['avg_cpc']}")
        except Exception as e:
            print(f"\nError getting metrics for '{keyword}': {str(e)}")

