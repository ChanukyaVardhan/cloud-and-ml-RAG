import sys

sys.path.append('generated/')

import grpc
import text_embedding_pb2
import text_embedding_pb2_grpc
from llama_cpp import Llama


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
    # with grpc.insecure_channel('34.74.89.40:80') as channel:
        stub = text_embedding_pb2_grpc.TextEmbeddingStub(channel)

        response = stub.GetPreferenceArticles(text_embedding_pb2.GetPreferenceArticlesRequest(
            # preference_text="Interested in news related to the Dutch government and flight movement in Amsterdam."
            preference_text="Interested in news related to gold."
        ))
        
        print(response)

if __name__ == '__main__':
    run()
