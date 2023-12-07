from bs4 import BeautifulSoup
from collections import defaultdict
from concurrent import futures
from datetime import datetime, timedelta
from google.cloud.sql.connector import Connector
from google.protobuf.timestamp_pb2 import Timestamp
from pgvector.asyncpg import register_vector

import sys
sys.path.append('generated/')

import asyncpg
import asyncio
import bert
import grpc
import json
import logging
import os
import re
import requests
import text_embedding_pb2
import text_embedding_pb2_grpc
import torch
import numpy as np

# Set the path to the service account key
if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", None):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/chanukya/Desktop/SEM 3/Cloud and ML/Project/cloud-and-ml-406515-21425057babc.json"

class TextEmbeddingServicer(text_embedding_pb2_grpc.TextEmbedding):

    def __init__(self):
        self.bert = bert.Bert()
        self.db_pool = None
        self.similarity_threshold = 0.9
        self.default_num_matches = 5
        self.epoch_start = datetime.fromisoformat("1970-01-01T00:00:00")

    async def init_db(self):
        loop = asyncio.get_running_loop()
        connector = Connector(loop=loop)
        self.db_pool = await connector.connect_async(
            "cloud-and-ml-406515:us-east1:vectordb-instance",
            "asyncpg",
            user="postgres",
            password="cloudml",
            db="text-database"
        )
        await register_vector(self.db_pool)

    def _get_article_information(self, html_content):
        match = re.search(r'<script>window\.SSR_DATA = (.*);</script>', html_content)
        if match:
            json_data = match.group(1)
            json_data = json.loads(json_data)["article"]["response"]["data"]
            article_id = json_data["id"]
            publish_time = json_data["attributes"]["publishOn"]
            title = json_data["attributes"]["title"]
            parsed_data = json_data["attributes"]["content"]
            content_soup = BeautifulSoup(parsed_data, 'html.parser')
            paragraphs = content_soup.find_all("p")
            paragraphs = [p.text for p in paragraphs if len(p.text.split()) >= 6]

            return {
                "id": article_id,
                "publish_time": publish_time,
                "title": title,
                "content": "".join(paragraphs)
            }
        else:
            return {}

    async def SaveTextEmbedding(self, request, context):
        url = request.url
        logging.info(f"Start SaveTextEmbedding request for url - {url}")

        headers = {'Cookie': '', 'User-Agent': ''}
        response = requests.get(url, headers=headers)
        article = BeautifulSoup(response.text, 'html.parser')
        article_information = self._get_article_information(str(article))

        chunks, all_embeddings = self.bert.get_embedding(article_information["content"], split_chunks = True)

        try:
            # CHECK - FIX THIS, IS IT BETTER TO MAINTAIN A POOL?
            # CHECK - INSERT CHUNKS AS A BATCH INSTEAD OF ONE EACH TIME
            for chunk_number, (chunk, embedding) in enumerate(zip(chunks, all_embeddings)):
                await self.db_pool.execute(
                        "INSERT INTO text_embeddings (id, chunk_number, article_url, publish_time, title, content, embedding) VALUES ($1, $2, $3, $4, $5, $6, $7)",
                        article_information["id"], chunk_number, url, datetime.fromisoformat(article_information["publish_time"]), article_information["title"], chunk, embedding
                    )
            logging.info(f"Completed SaveTextEmbedding request for url - {url} in {len(chunks)} chunks")
            status = True
        except Exception as e:
            logging.error(f"Error saving embedding: {e}")
            status = False

        return text_embedding_pb2.SaveTextEmbeddingResponse(status = status)

    def _cosine_similarity(self, vec1, vec2):
        dot_product = np.dot(vec1, vec2)
        magnitude = np.linalg.norm(vec1) * np.linalg.norm(vec2)
        if magnitude == 0:
            return 0
        return dot_product / magnitude

    async def GetSimilarity(self, request, context):
        text1 = request.text1
        text2 = request.text2

        _, embedding1 = self.bert.get_embedding(text1, split_chunks = False)
        chunks, all_embeddings2 = self.bert.get_embedding(text2, split_chunks = True)

        response = text_embedding_pb2.GetSimilarityResponse()
        for chunk, embedding2 in zip(chunks, all_embeddings2):
            response.text_similarity.append(
                text_embedding_pb2.TextSimilarity(
                    text1 = text1,
                    text2 = chunk,
                    similarity = self._cosine_similarity(embedding1, embedding2),
                )
            )

        return response

    async def GetPreferenceArticles(self, request, context):
        preference_text = request.preference_text
        start_time = request.start_time.ToDatetime()
        end_time = request.end_time.ToDatetime()
        num_matches = request.num_matches

        if end_time == self.epoch_start: # No end time passed
            end_time = datetime.now()
        if start_time == self.epoch_start: # No start time passed
            start_time = end_time - timedelta(days=7)
        if num_matches == 0: # If no matches requested, default to 5
            num_matches = self.default_num_matches

        logging.info(f"Start GetPreferenceArticles request for {num_matches} articles between {start_time} and {end_time}!")

        _, preference_embedding = self.bert.get_embedding(preference_text, split_chunks = False)
        try:
            similarity_query_results = await self.db_pool.fetch(
                """
                WITH vector_matches AS (
                  SELECT id, 1 - (embedding <=> $1) AS similarity
                  FROM text_embeddings
                  WHERE publish_time > $4 AND publish_time < $5 AND 1 - (embedding <=> $1) > $2
                )
                SELECT id, MAX(similarity) AS max_similarity
                FROM vector_matches
                GROUP BY id
                ORDER BY MAX(similarity) DESC
                LIMIT $3
                """,
                preference_embedding,
                self.similarity_threshold,
                num_matches,
                start_time,
                end_time
            )
            article_to_similarity = {row['id']: row['max_similarity'] for row in similarity_query_results}

            query_results = await self.db_pool.fetch(
                """
                SELECT id, article_url, chunk_number, content FROM text_embeddings
                WHERE id = ANY($1)
                """,
                list(article_to_similarity.keys()),
            )

            # Process the query results
            articles_by_url = defaultdict(list)
            for row in query_results:
                article_id, article_url, chunk_number, content = row['id'], row['article_url'], row['chunk_number'], row['content']
                articles_by_url[article_url].append((chunk_number, content, article_id))

            # Construct the response using Proto message types
            response = text_embedding_pb2.GetPreferenceArticlesResponse()
            articles_with_similarity = []
            for article_url, chunks in articles_by_url.items():
                sorted_chunks = sorted(chunks, key=lambda x: x[0])
                article_text = ' '.join([chunk[1] for chunk in sorted_chunks])
                similarity = article_to_similarity[chunks[0][2]]
                article = text_embedding_pb2.PreferenceArticle(url=article_url, summary=article_text, similarity=similarity)
                
                # Append the article along with its similarity to the list
                articles_with_similarity.append(article)

            # Sort the articles by similarity in descending order
            sorted_articles = sorted(articles_with_similarity, key=lambda x: x.similarity, reverse=True)

            # Append sorted articles to the response
            for article in sorted_articles:
                response.article.append(article)

            logging.info(f"Completed GetPreferenceArticles request for {num_matches} articles between {start_time} and {end_time}!")
            return response

        except Exception as e:
            logging.error(f"Error retrieving: {e}")

        return text_embedding_pb2.GetPreferenceArticlesResponse()


async def serve():
    servicer = TextEmbeddingServicer()
    await servicer.init_db()

    server = grpc.aio.server()
    text_embedding_pb2_grpc.add_TextEmbeddingServicer_to_server(servicer, server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
