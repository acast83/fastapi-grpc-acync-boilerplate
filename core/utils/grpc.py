from google.protobuf.json_format import MessageToDict

def grpc_response_to_dict(grpc_response):
    return MessageToDict(grpc_response, preserving_proto_field_name=True)
