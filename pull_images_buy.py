from serpapi import google_search
import os
from dotenv import load_dotenv 
import requests

load_dotenv()
key = os.getenv("SERPAPI_KEY")

def search_perfume(perfume_name):
    url = "https://serpapi.com/search"
    params = {
        "engine": "amazon",
        "k": f"{perfume_name} cologne",
        "amazon_domain": "amazon.com",
        "api_key": key
    }
    response = requests.get(url, params=params)
    data = response.json()

    results = (
        data.get("organic_results", []) or
        data.get("product_ads", []) or
        data.get("sponsored_brands", []) or
        data.get("video_results", []) or
        []
    )

    if not results:
        print("No product found.")
        return None, None

    top_result = results[0]
    image = top_result.get("thumbnail")
    link = top_result.get("link") or top_result.get("amazon_url")

    return image, link

