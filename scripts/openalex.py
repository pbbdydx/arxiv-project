import requests
import json
import time
import os

# Query settings
FILTER = "concepts.id:C41008148|C136512526|C154945302|C121332964"  # ML, statistics, applied math, optimization
FIELDS = "id,title,abstract_inverted_index_v3,publication_year,cited_by_count,concepts"
PER_PAGE = 200
MAX_PAPERS = 30000
OUTPUT_FILE = "openalex_applied_filtered.jsonl"


def fetch_openalex_data():
    count = 0
    cursor = "*"
    base_url = "https://api.openalex.org/works"

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        while count < MAX_PAPERS:
            query_url = 'https://api.openalex.org/works?filter=concepts.id:C41008148%7CC136512526%7CC154945302%7CC121332964&per-page=200&cursor=*&select=id,title,abstract_inverted_index,publication_year,cited_by_count,concepts&mailto=pb601027@gmail.com'
        
            r = requests.get(query_url)
            if r.status_code != 200:
                print("Error fetching data:", r.status_code)
                break

            data = r.json()
            results = data.get("results", [])
            for paper in results:
                # Filter to papers with title, abstract, year, and citation count
                if not paper.get("title") or not paper.get("abstract_inverted_index_v3"):
                    continue

                paper_entry = {
                    "id": paper["id"],
                    "title": paper["title"],
                    "abstract": paper["abstract_inverted_index_v3"],
                    "year": paper["publication_year"],
                    "citation_count": paper["cited_by_count"],
                    "fields_of_study": [c["display_name"] for c in paper.get("concepts", [])],
                    "isHighlyCited": int(paper["cited_by_count"] >= 100)
                }
                f.write(json.dumps(paper_entry) + "\n")
                count += 1

                if count >= MAX_PAPERS:
                    break

            print(f"Fetched {count} papers so far...")

            # Update cursor for pagination
            cursor = data["meta"]["next_cursor"]
            time.sleep(1)  # rate limiting

    print(f"Finished! Saved {count} papers to {OUTPUT_FILE}")


if __name__ == "__main__":
    fetch_openalex_data()
