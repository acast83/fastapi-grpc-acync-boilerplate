#!/usr/bin/bash
set -e

python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

current_folder=$(pwd)

echo $current_folder >> "$current_folder/.venv/lib/python3.11/site-packages/pythonpaths.pth"

config_file="config/services.yaml"

# Read the gRPC service names from the YAML file
# This command extracts the keys under 'services.grpc'
grpc_services=($(yq e '.services.grpc | keys' "$config_file" -o=json | jq -r '.[]'))

# Loop through each service
for service in "${grpc_services[@]}"; do
    # Navigate to the service's proto directory
    # Update this path according to your project's structure
    echo "$current_folder/services/grpc/$service/proto" >> "$current_folder/.venv/lib/python3.11/site-packages/pythonpaths.pth"
done

cd ./config/environments || exit
cp preferences.env.sample preferences.env
cp logging.env.sample logging.env
cp installation.env.sample installation.env
cp credentials.env.sample credentials.env
cd - || exit


