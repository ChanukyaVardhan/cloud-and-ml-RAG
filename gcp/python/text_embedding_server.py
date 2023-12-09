import sys
from collections import defaultdict
from concurrent import futures
from datetime import datetime

from bs4 import BeautifulSoup
from google.cloud.sql.connector import Connector
from pgvector.asyncpg import register_vector

sys.path.append('generated/')

import asyncio
import json
import logging
import os
import re

import asyncpg
import bert
import grpc
import requests
import text_embedding_pb2
import text_embedding_pb2_grpc
import torch

# Set the path to the service account key
if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", None):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/scratch/sca321/cloud/proj2/cloud-and-ml-RAG/service_account.json"

class TextEmbeddingServicer(text_embedding_pb2_grpc.TextEmbedding):

    def __init__(self):
        self.bert = bert.Bert()
        self.db_pool = None

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

    async def GetPreferenceArticles(self, request, context):
        logging.info(f"Start GetPreferenceArticles request")
        # CHECK - LIMIT TEXT TO 512 TOKENS? - OR JUST ERROR
        preference_text = request.preference_text

        _, preference_embedding = self.bert.get_embedding(preference_text, split_chunks = False)

        similarity_threshold = 0.9
        num_matches = 5
        try:
            # CHECK - FIX THE QUERY BASED ON REQUIREMENT. SHOULD BE DISTINCT URLs SEARCH?
            query_results = await self.db_pool.fetch(
                """
                WITH vector_matches AS (
                  SELECT id, 1 - (embedding <=> $1) AS similarity
                  FROM text_embeddings
                  WHERE 1 - (embedding <=> $1) > $2
                  ORDER BY similarity DESC
                  LIMIT $3
                )
                SELECT id, article_url, chunk_number, content FROM text_embeddings
                WHERE id IN (SELECT id FROM vector_matches)
                """,
                preference_embedding,
                similarity_threshold,
                num_matches
            )

            # Process the query results
            articles_by_url = defaultdict(list)
            for row in query_results:
                article_url, chunk_number, content = row['article_url'], row['chunk_number'], row['content']
                articles_by_url[article_url].append((chunk_number, content))

            # Construct the response using Proto message types
            response = text_embedding_pb2.GetPreferenceArticlesResponse()
            # CHECK - WILL THIS CHANGE THE ORDER??
            for article_url, chunks in articles_by_url.items():
                sorted_chunks = sorted(chunks, key=lambda x: x[0])
                article_text = ' '.join([chunk[1] for chunk in sorted_chunks])
                article = text_embedding_pb2.PreferenceArticle(url=article_url, summary=article_text)
                response.article.append(article)

            logging.info(f"Completed GetPreferenceArticles request")
            return response

        except Exception as e:
            logging.error(f"Error retrieving: {e}")

        return text_embedding_pb2.GetPreferenceArticlesResponse()

    # async def SaveTextEmbedding(self, request, context):
    #     url = request.url
    #     logging.info(f"Start SaveTextEmbedding request for url - {url}")
    #     chunks, all_embeddings = self.bert.get_embedding(request.text, split_chunks = True)

    #     try:
    #         # CHECK - FIX THIS, IS IT BETTER TO MAINTAIN A POOL?
    #         # CHECK - INSERT CHUNKS AS A BATCH INSTEAD OF ONE EACH TIME
    #         for chunk_number, (chunk, embedding) in enumerate(zip(chunks, all_embeddings)):
    #             await self.db_pool.execute(
    #                     "INSERT INTO text_embeddings (url, chunk_number, text, embedding) VALUES ($1, $2, $3, $4)",
    #                     url, chunk_number, chunk, embedding
    #                 )
    #         logging.info(f"Completed SaveTextEmbedding request for url - {url} in {len(chunks)} chunks")
    #         status = True
    #     except Exception as e:
    #         logging.error(f"Error saving embedding: {e}")
    #         status = False

    #     return text_embedding_pb2.SaveTextEmbeddingResponse(status = status)

    # async def GetPreferenceArticles(self, request, context):
    #     logging.info(f"Start GetPreferenceArticles request")
    #     # CHECK - LIMIT TEXT TO 512 TOKENS? - OR JUST ERROR
    #     preference_text = request.preference_text

    #     _, preference_embedding = self.bert.get_embedding(preference_text, split_chunks = False)

    #     similarity_threshold = 0.9
    #     num_matches = 10
    #     try:
    #         # CHECK - FIX THE QUERY BASED ON REQUIREMENT. SHOULD BE DISTINCT URLs SEARCH?
    #         query_results = await self.db_pool.fetch(
    #             """
    #             WITH vector_matches AS (
    #               SELECT url, 1 - (embedding <=> $1) AS similarity
    #               FROM text_embeddings
    #               WHERE 1 - (embedding <=> $1) > $2
    #               ORDER BY similarity DESC
    #               LIMIT $3
    #             )
    #             SELECT url, chunk_number, text FROM text_embeddings
    #             WHERE url IN (SELECT url FROM vector_matches)
    #             """,
    #             preference_embedding,
    #             similarity_threshold,
    #             num_matches
    #         )

    #         # Process the query results
    #         articles_by_url = defaultdict(list)
    #         for row in query_results:
    #             url, chunk_number, text = row['url'], row['chunk_number'], row['text']
    #             articles_by_url[url].append((chunk_number, text))

    #         # Construct the response using Proto message types
    #         response = text_embedding_pb2.GetPreferenceArticlesResponse()
    #         # CHECK - WILL THIS CHANGE THE ORDER?? - DON'T THINK SO
    #         for url, chunks in articles_by_url.items():
    #             sorted_chunks = sorted(chunks, key=lambda x: x[0])
    #             article_text = ' '.join([chunk[1] for chunk in sorted_chunks])
    #             article = text_embedding_pb2.PreferenceArticle(url=url, summary=article_text)
    #             response.article.append(article)

    #         logging.info(f"Completed GetPreferenceArticles request")
    #         return response

    #     except Exception as e:
    #         logging.error(f"Error retrieving: {e}")

    #     return text_embedding_pb2.GetPreferenceArticlesResponse()



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
