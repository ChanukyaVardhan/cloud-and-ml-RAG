import sys
sys.path.append('generated/')

from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp

import grpc
import text_embedding_pb2
import text_embedding_pb2_grpc

def iso_datetime_to_timestamp(iso_datetime_string):
    datetime_obj = datetime.fromisoformat(iso_datetime_string.replace('Z', '+00:00'))
    timestamp = Timestamp()
    timestamp.FromDatetime(datetime_obj)
    return timestamp

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
    # with grpc.insecure_channel('34.74.89.40:80') as channel:
        stub = text_embedding_pb2_grpc.TextEmbeddingStub(channel)

        response = stub.GetPreferenceArticles(text_embedding_pb2.GetPreferenceArticlesRequest(
            # preference_text="Interested in news related to the Dutch government and flight movement in Amsterdam."
            preference_text="Interested in news related to gold.",
            start_time=iso_datetime_to_timestamp("2023-11-01T04:00:00.000Z"),
            # end_time=iso_datetime_to_timestamp("2023-11-05T04:00:00.000Z"),
            # num_matches=5
        ))

        print(response)

if __name__ == '__main__':
    run()
