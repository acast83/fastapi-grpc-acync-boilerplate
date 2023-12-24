# Fastapi GRPC asynchronous template application

## Description

The Fastapi GRPC-REST Template is an advanced,
scalable application framework designed to operate
in an asynchronous environment, enhancing performance
and efficiency. It's crafted using FastAPI as the web
framework, ensuring quick development and response times.
Central to its data handling is the asynchronous Tortoise ORM,
which allows for non-blocking database interactions, making it
ideal for high-load applications. The template integrates gRPC
services for robust inter-service communication. Additionally,
it adopts the MVC (Model-View-Controller) architectural pattern,
organizing code structure into logical components that separate
the internal representations of information from the ways information
is presented to and accepted from the user. This makes the template
particularly suitable for developers looking to implement a microservices
architecture while maintaining clear, manageable codebases that facilitate
both frontend and backend development.

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
