# Fastapi GRPC asynchronous template application

## Description

The Fastapi GRPC-REST Template is a modern, scalable application template designed for seamless integration between frontend interfaces and backend
microservices. At the
core of its architecture, it leverages the power of gRPC services, known for their high-performance inter-service communication capabilities. This template is ideal for developers
looking to implement a microservices architecture while maintaining a straightforward and efficient pathway for frontend applications to interact with backend logic.

## Installation

create a new directory and clone the Fastapi template application into it

```
mkdir project_name
cd project_name
git clone git@github.com:acast83/fastapi-grpc-acync-boilerplate.git .
```

### Prerequisites

Before installing Fastapi template application, ensure you have the following:

- python 3.11
- vq:

github:
https://github.com/mikefarah/yq

Linux via snap:

```
sudo snap install yq
```

MacOS / Linux via Homebrew:

```
brew install yq
```

### Installing

from project's root directory run:

```
./create_environment.sh
source venv/bin/activate
```

### Setup environment variables

```
cd config/environments
```

after that, edit the env files with your preferences

### Setup postgres databases

Fastapi GRPC template uses postgres as a database service,
so after installing postgres db you need to create the users
and the databases according to the credentials.env file

## Using Fastapi GRPC template base application as monolith app

from project's root directory run:

```
python start_monolith.py
```

## Using Fastapi GRPC template base application as microservices

from project's root directory run:

```
python start_services.py
```

## Compiling proto files

from project's root directory run:

```
./compile_protos.sh
```
