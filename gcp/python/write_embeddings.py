import sys
sys.path.append('generated/')

import grpc
import json
import text_embedding_pb2
import text_embedding_pb2_grpc
import time

def get_urls_from_json(file_name):
    # Open the file and load the JSON content
    with open(file_name, 'r') as file:
        data = json.load(file)
    
    # Extract the list of articles
    articles = data.get('articles_metadata', [])
    
    # Extract URLs from each article
    urls = [article.get('article_url') for article in articles if 'Earnings Call Presentation' not in article['title']]
    print(f"Total inserting articles - {len(urls)}")

    return urls

def run_json(file_name):
    urls = get_urls_from_json(file_name)

    start_time = time.time()
    with grpc.insecure_channel('localhost:50051') as channel: # Local Host
        stub = text_embedding_pb2_grpc.TextEmbeddingStub(channel)

        for url in urls:
            response = stub.SaveTextEmbedding(text_embedding_pb2.SaveTextEmbeddingRequest(url=url,))

            print(f"Server response for url {url} : {response.status}")

    end_time = time.time()
    print(f"Total run time : {end_time - start_time} secs!")

import os

if __name__ == '__main__':
    run_json(f"/home/chanukya/Desktop/SEM 3/Cloud and ML/Project/cloud-and-ml-RAG/json_dumps/2023-11-28T04:00:00.000Z.json")
