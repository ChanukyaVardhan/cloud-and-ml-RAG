FROM pytorch/pytorch

WORKDIR /app

COPY ./requirements.txt .
COPY ./protos ./protos
COPY ./python ./python
COPY ./generated ./generated

RUN pip install -r requirements.txt

RUN python3 -m grpc_tools.protoc -I=protos/ --python_out=generated/ --pyi_out=generated/ --grpc_python_out=generated/ protos/text_embedding.proto

CMD ["python", "python/text_embedding_server.py"]


# sudo docker build -t cloudml-project .
# sudo docker images
# sudo docker run cloudml-project

# gcloud auth list
# gcloud auth login
#	gcloud config set account `ACCOUNT`

# gcloud config set project cloud-and-ml-406515

# gcloud services enable artifactregistry.googleapis.com
# gcloud auth configure-docker
# gcloud auth configure-docker us-east1-docker.pkg.dev
# gcloud artifacts repositories create cloudml-project-repository --repository-format=docker --location=us-east1 --description="Cloud and ML Project artifactory repository"
# gcloud artifacts repositories describe cloudml-project-repository --project=cloud-and-ml-406515 --location=us-east1
# sudo docker tag cloudml-project:latest chanukya43/cloudml-project:fall2023
# sudo docker push chanukya43/cloudml-project:fall2023
# kubectl apply -f ./deployments/service.yaml
# kubectl apply -f ./deployments/deployment.yaml

# sudo docker tag [SOURCE_IMAGE]:[TAG] [LOCATION]-docker.pkg.dev/[PROJECT-ID]/[REPOSITORY_NAME]/[IMAGE]:[TAG]
	# sudo docker tag cloudml-project:latest us-east1-docker.pkg.dev/cloud-and-ml-406515/cloudml-project-repository/cloudml-project:fall2023
# gcloud projects add-iam-policy-binding cloud-and-ml-406515 --member='user:chanukyagujjula01@gmail.com' --role='roles/artifactregistry.writer'
# sudo docker push [LOCATION]-docker.pkg.dev/[PROJECT-ID]/[REPOSITORY_NAME]/[IMAGE]:[TAG]
	# sudo docker push us-east1-docker.pkg.dev/cloud-and-ml-406515/cloudml-project-repository/cloudml-project:fall2023
	# sudo docker push us-east1-docker.pkg.dev/cloud-and-ml-406515/cloudml-project-repository/cloudml-project:fall2023


# gcloud container clusters get-credentials cloudml-gke-cluster-1 --zone=us-east1-c



# kubectl create secret generic google-credentials --from-file=service-account.json="/home/chanukya/Desktop/SEM 3/Cloud and ML/Project/cloud-and-ml-406515-21425057babc.json"
# kubectl config use-context gke_cloud-and-ml-406515_us-east1-c_cloudml-gke-cluster-1
