import requests
import time
import json

# Set your API key here if you get one (optional for basic access)
API_KEY = None  # Replace with "your_key" if needed

HEADERS = {"x-api-key": API_KEY} if API_KEY else {}

# Query settings
QUERY = "machine learning OR statistics OR optimization OR data science"
FIELDS = "title,abstract,year,citationCount,fieldsOfStudy"
LIMIT = 100  # max per request
MAX_RESULTS = 30000
OUTPUT_FILE = "semantic_papers.jsonl"


def fetch_papers():
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    total_downloaded = 0
    offset = 0

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        while total_downloaded < MAX_RESULTS:
            params = {
                "query": QUERY,
                "fields": FIELDS,
                "limit": LIMIT,
                "offset": offset
            }

            response = requests.get(base_url, headers=HEADERS, params=params)
            if response.status_code != 200:
                print(f"Error: {response.status_code} - {response.text}")
                break

            data = response.json()
            papers = data.get("data", [])

            if not papers:
                break

            for paper in papers:
                if paper.get("abstract") and paper.get("title") and paper.get("citationCount") is not None:
                    f.write(json.dumps(paper) + "\n")
                    total_downloaded += 1
                    if total_downloaded >= MAX_RESULTS:
                        break

            print(f"Downloaded {total_downloaded} papers...")
            offset += LIMIT
            time.sleep(1)  # polite rate limit

    print(f"Finished! Saved {total_downloaded} papers to {OUTPUT_FILE}")


if __name__ == "__main__":
    fetch_papers()
