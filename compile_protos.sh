#!/bin/bash

# Install the required packages
#brew install yq
#sudo snap install yq
#https://github.com/mikefarah/yq

# Path to the services.yaml file
config_file="config/services.yaml"

# Read the gRPC service names from the YAML file
# This command extracts the keys under 'services.grpc'
grpc_services=($(yq e '.services.grpc | keys' "$config_file" -o=json | jq -r '.[]'))

# Loop through each service
for service in "${grpc_services[@]}"; do
    # Navigate to the service's proto directory
    # Update this path according to your project's structure
    cd "services/grpc/$service/proto" || continue

    # Run the protoc command
    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. "$service.proto"

    # Optionally, navigate back to the original directory
    cd - || continue
done
