# the name of the application
NAME=liquorpark

# GCP Project ID
GCR_TAG=gcr.io/${PROJECT_ID}/$(NAME)

# Container Version
VERSION=$(shell git describe --tags)


## Run the docker build command to create the container and compile the
## application inside the container.
build: check-env
	docker build -t $(GCR_TAG):$(VERSION) .

## Run the test suite inside the docker container
test: build
	docker run --name $(NAME)-test --rm $(NAME) python manage.py test

## Build and run the application using ENV_FILE for configuration.
run: build
	docker run -it -p 8080:8080 $(GCR_TAG):$(VERSION)

## Publish container to GCP Repository
push: build
	gcloud docker -- push $(GCR_TAG):$(VERSION)


## Create the GCP Cluster
createcluster:
	gcloud container clusters create $(NAME)

## Once the cluster is ready, create a Kubernetes deployment pod
createpod: check-env
	kubectl run $(NAME) --image=$(GCR_TAG):$(VERSION) --port=80
	kubectl expose deployment $(NAME) --type="LoadBalancer"


## Update the version in the cloud
deploy: check-env
	kubectl set image deployment/$(NAME) $(NAME)=$(GCR_TAG):$(VERSION)

stats:
	kubectl get services $(NAME)


## Require Project ID to be set
check-env:
ifndef PROJECT_ID
    $(error PROJECT_ID is undefined)
endif


