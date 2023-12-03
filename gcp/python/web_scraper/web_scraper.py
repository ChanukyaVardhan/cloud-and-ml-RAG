"""
https://seekingalpha.com/latest-articles?page=1
https://seekingalpha.com/latest-articles?from=2023-11-28T05%3A00%3A00.000Z&to=2023-12-01T04%3A59%3A59.9990
"""
import re
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from datetime import datetime, timedelta

def find_url(tag):
	return tag.name and tag.get('data-test-id') == 'post-list-item-title'

def find_date(tag):
	return tag.name and tag.get('data-test-id') == 'post-list-date'

def generate_url_encoded_dates(start_date, end_date):
	formatted_start_date = start_date.strftime('%Y-%m-%dT%H:%M:%S.000Z')
	formatted_end_date = end_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-3]  # Remove microseconds, keep milliseconds
	url_encoded_dates = f'from={quote(formatted_start_date)}&to={quote(formatted_end_date)}'
	return url_encoded_dates

def getArticlesMetadata(start_date, end_date):
	base_url = "https://seekingalpha.com"
	headers = {'Cookie': '', 'User-Agent': ''}

	metadata = []
	for page in range(1, 3):
		news_url = f"{base_url}/latest-articles?page={page}"
		response = requests.get(news_url, headers=headers)

		if response.ok:
			web_soup = BeautifulSoup(response.text, 'html.parser')
			article_soup = web_soup.find_all('div', class_="flex grow self-center")

			for article in article_soup:
				title = article.find(find_url)
				date = article.find(find_date)

				if title != None and date != None:
					url = title.get('href')
					metadata.append({'date': date.text, 'url': f"{base_url}/{url}", 'title': title.text})

	return metadata

def getArticleParagraphs(html_content):
	match = re.search(r'<script>window\.SSR_DATA = (.*);</script>', html_content)
	if match:
		json_data = match.group(1)
		parsed_data = json.loads(json_data)["article"]["response"]["data"]["attributes"]["content"]
		content_soup = BeautifulSoup(parsed_data, 'html.parser')
		paragraphs = content_soup.find_all("p")
		paragraphs = [p.text for p in paragraphs if len(p.text.split()) >= 6]
		return paragraphs
	else:
		return [""]

def getArticles(start_date, end_date):
	articles= []
	headers = {'Cookie': '', 'User-Agent': ''}
	metadata_list = getArticlesMetadata(start_date, end_date)
	print(f"Length of articles list: {len(metadata_list)}")
	for metadata in metadata_list:
		url = metadata['url']
		response = requests.get(url, headers=headers)
		article = BeautifulSoup(response.text, 'html.parser')
		paragraphs = getArticleParagraphs(str(article))
		text = ' '.join(paragraphs)
		articles.append({ 'url': url, 'date': metadata['date'], 
			'title': metadata['title'], 'text': text })
	return articles

if __name__ == "__main__":
	start_date = datetime(2023, 11, 15, 5, 0, 0)
	end_date = datetime(2023, 11, 20, 4, 59, 59, 999000)
	articles = getArticles(start_date, end_date)
	print(articles)
