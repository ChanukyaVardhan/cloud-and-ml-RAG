FROM pytorch/pytorch

WORKDIR /app

COPY ./requirements.txt .
COPY ./protos ./protos
COPY ./python ./python
COPY ./generated ./generated

RUN pip install -r requirements.txt

RUN python3 -m grpc_tools.protoc -I=protos/ --python_out=generated/ --pyi_out=generated/ --grpc_python_out=generated/ protos/text_embedding.proto

CMD ["python", "python/text_embedding_server.py"]
