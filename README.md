# Market Flux Finder: Cloud ML Synergy In Finance

## Setup

For local setup we recommend to create a conda environment and install the requried packages as follows.
```
conda create --name ENV_NAME
conda activate ENV_NAME
pip install -r requirements.txt
```

## Scraping Data

Running the following script (update the dates in the file as required) saves the articles metadata.
```
python web_scraper/scrape_from_api.py
```

## Cloud SQL

Setup a postgresql database in a google cloud SQL server. Create a table in this database (with appropriate GCP permissioning and database parameters) with the below script.
```
python gcp/python/create_table.py
```

## Web Service

To run the web service, we first need to generate py files for the protos.
```
cd gcp
mkdir generated
python -m grpc_tools.protoc -I=protos/ --python_out=generated/ --pyi_out=generated/ --grpc_python_out=generated/ protos/text_embedding.proto
```

### Local Server

After this we can start the server as below to to get a local running web service.
```
cd gcp
python python/text_embedding_server.py
```

### Deploy Server To GKE

To deploy this web service code on GKE, we first create a docker image using the Dockerfile. We tag it and push to dockerhub.
```
cd gcp
docker build -t cloudml-project .
docker tag cloudml-project-comp:latest chanukya43/cloudml-project-comp:fall2023
docker push chanukya43/cloudml-project-comp:fall2023
```

Once the docker images are available at dockerhub, we now apply the service and deployment configs on GKE that will create the service and deployment for our web service. The above docker image is pulled from dockerhub and GKE creates a pod for the deployment.
```
cd gcp
kubectl apply -f deployments/service.yaml
kubectl apply -f deployments/deployment.yaml
```

## Inserting Data

We can insert the data for the articles metadata that was generated earlier using the following script. This will read each article url, get the content, send a request to the web service (choose local or appropriate endpoint on GKE for the service), which will insert the data into the table.
```
python write_embeddings.py
```

To identify the endpoint on GKE for the web service, we can run the following `kubectl` command and get the external IP for the appropriate service.
```
kubectl get service
```

## Inference/Retrieving

We created a simple UI interface to retrieve results using gradio. To start this UI interface, run the following command (by setting the appropriate urls in the script). The interface is simple to understand all the fields and parameters.
```
cd demo
python demo.py
```

Write a query, select the requried fields and click submit to get the results for your query.
