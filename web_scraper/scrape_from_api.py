"""
https://seekingalpha.com/latest-articles?page=1
https://seekingalpha.com/latest-articles?from=2023-11-28T05%3A00%3A00.000Z&to=2023-12-01T04%3A59%3A59.9990
"""
import calendar
import re
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

base_url = "https://seekingalpha.com"


def iso_datetime_to_epoch(iso_datetime_string):
    # Parsing the ISO 8601 datetime format
    datetime_obj = datetime.fromisoformat(iso_datetime_string.replace('Z', '+00:00'))
    
    # Converting to epoch time
    epoch_time = calendar.timegm(datetime_obj.utctimetuple())
    return epoch_time


# https://seekingalpha.com/api/v3/articles?filter[category]=latest-articles&filter[since]=1698811200&filter[until]=1699070399&page[size]=50
def scrape_from_api(start_date, end_date):
    print(f"Started request between {start_date} to {end_date}!")

    # Custom headers based on the network tab information
    # headers = {}
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    articles_metadata = []
    total_pages = None
    current_page = 1
    while total_pages is None or total_pages > 0:
        # Parameters for the GET request
        params = {
            "filter[category]": "latest-articles",
            "filter[since]": iso_datetime_to_epoch(start_date),
            "filter[until]": iso_datetime_to_epoch(end_date),
            "page[size]": 50,
            "page[number]": current_page
        }

        # Sending the GET request
        response = requests.get(f"{base_url}/api/v3/articles", params=params, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response text into JSON
            response_json = response.json()
            response_data = response_json["data"]
            response_meta = response_json["meta"]

            if total_pages is None:
                total_pages = response_meta["page"]["totalPages"]
                total_articles = response_meta["page"]["total"]
                print(f"Requesting for total pages of {total_pages} and {total_articles} articles")

            for data in response_data:
                articles_metadata.append({
                    "id": data["id"],
                    "publish_time": data["attributes"]["publishOn"],
                    "title": data["attributes"]["title"],
                    "article_url": f"{base_url}/{data['links']['self']}",
                })

            print(f"Completed request for page number: {current_page}")
            total_pages -= 1
            current_page += 1

        else:
            print(f"Request failed with status code: {response.status_code} for page number: {current_page}")

        if total_pages is None:
            total_pages = 0

    print(f"Completed request between {start_date} to {end_date} and gathered meta data for {len(articles_metadata)} articles!")
    return articles_metadata


def get_article_content(html_content):
    match = re.search(r'<script>window\.SSR_DATA = (.*);</script>', html_content)
    if match:
        json_data = match.group(1)
        parsed_data = json.loads(json_data)["article"]["response"]["data"]["attributes"]["content"]
        content_soup = BeautifulSoup(parsed_data, 'html.parser')
        paragraphs = content_soup.find_all("p")
        paragraphs = [p.text for p in paragraphs if len(p.text.split()) >= 6]
        return "".join(paragraphs)
    else:
        return ""


def get_articles(start_date, end_date, article_count = None):
    headers = {'Cookie': '', 'User-Agent': ''}
    articles_metadata = scrape_from_api(start_date, end_date)

    article_count = len(articles_metadata) if article_count is None else min(article_count, len(articles_metadata))
    articles= []
    for article_metadata in articles_metadata:
        response = requests.get(article_metadata["article_url"], headers=headers)
        article = BeautifulSoup(response.text, 'html.parser')
        article_content = get_article_content(str(article))

        articles.append({
            "id": article_metadata["id"],
            "article_url": article_metadata["article_url"],
            "publish_time": article_metadata["publish_time"],
            "title": article_metadata["title"],
            "content": article_content
        })

        if len(articles) >= article_count:
            break

    return articles


if __name__ == "__main__":
    
    start_date = "2023-11-01T04:00:00.000Z"
    end_date = "2023-11-02T03:59:59.999Z"

    articles_metadata = scrape_from_api(start_date, end_date)

    # Dumping the dictionary into a JSON file
    if (len(articles_metadata)) > 0:
        with open(f'json_dumps/{start_date}.json', 'w') as file:
            json.dump({"count": len(articles_metadata), "articles_metadata": articles_metadata}, file, indent=4)

    # articles = get_articles(start_date, end_date, article_count = 1)
    # print(json.dumps(articles[0], indent = 4))
