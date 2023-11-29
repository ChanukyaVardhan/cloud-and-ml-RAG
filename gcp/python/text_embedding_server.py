from concurrent import futures
from google.cloud.sql.connector import Connector
from pgvector.asyncpg import register_vector

import sys
sys.path.append('generated/')

import asyncpg
import asyncio
import bert
import grpc
import logging
import os
import text_embedding_pb2
import text_embedding_pb2_grpc
import torch

# Set the path to the service account key
if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", None):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/chanukya/Desktop/SEM 3/Cloud and ML/Project/cloud-and-ml-406515-21425057babc.json"

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

    async def SaveTextEmbedding(self, request, context):
        url = request.url
        logging.info(f"Start SaveTextEmbedding request for url - {url}")
        chunks, all_embeddings = self.bert.get_embedding(request.text, split_chunks = True)

        try:
            # CHECK - FIX THIS, IS IT BETTER TO MAINTAIN A POOL?
            for chunk_number, (chunk, embedding) in enumerate(zip(chunks, all_embeddings)):
                await self.db_pool.execute(
                        "INSERT INTO text_embeddings (url, chunk_number, text, embedding) VALUES ($1, $2, $3, $4)",
                        url, chunk_number, chunk, embedding
                    )
            logging.info(f"Completed SaveTextEmbedding request for url - {url} in {len(chunks)} chunks")
            status = True
        except Exception as e:
            logging.error(f"Error saving embedding: {e}")
            status = False

        return text_embedding_pb2.SaveTextEmbeddingResponse(status = status)


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
