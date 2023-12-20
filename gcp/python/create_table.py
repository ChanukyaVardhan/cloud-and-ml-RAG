import asyncio
import asyncpg
import google.auth
from google.cloud.sql.connector import Connector
from pgvector.asyncpg import register_vector
import os

import numpy as np

# Set the path to the service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account_key.json"

project_id = "PROJECT ID"
region = "us-east1"
instance_name = "vectordb-instance"
database_user = "postgres"
database_name = "DATABASE NAME"
database_password = "DATABASE PASSWORD"

async def main():
    # get current running event loop to be used with Connector
    loop = asyncio.get_running_loop()

    # Load credentials from the service account key file
    credentials, project = google.auth.default()

    # initialize Connector object as async context manager
    async with Connector(loop=loop) as connector:
        # create connection to Cloud SQL database
        conn: asyncpg.Connection = await connector.connect_async(
            f"{project_id}:{region}:{instance_name}",  # Cloud SQL instance connection name
            "asyncpg",
            user=f"{database_user}",
            password=f"{database_password}",
            db=f"{database_name}"
        )

        # query Cloud SQL database
        results = await conn.fetch("SELECT version()")
        print(results[0]["version"])

        await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        await register_vector(conn)

        # Create the `text_embeddings` table to store vector embeddings.
        await conn.execute(
            """CREATE TABLE text_embeddings(
                                id VARCHAR NOT NULL,
                                chunk_number INT NOT NULL,
                                article_url VARCHAR,
                                publish_time TIMESTAMP WITH TIME ZONE,
                                title VARCHAR,
                                content VARCHAR,
                                embedding vector(768),
                                PRIMARY KEY (id, chunk_number))"""
        )

        # close asyncpg connection
        await conn.close()


if __name__ == '__main__':
    asyncio.run(main())
