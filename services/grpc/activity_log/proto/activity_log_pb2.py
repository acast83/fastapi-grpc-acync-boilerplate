# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: activity_log.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12\x61\x63tivity_log.proto\x12\x12\x61\x63tivitylogservice\"+\n\x14\x43reateMessageRequest\x12\x13\n\x0b\x64\x65scription\x18\x01 \x01(\t\"8\n\x15\x43reateMessageResponse\x12\n\n\x02id\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t2z\n\x12\x41\x63tivityLogService\x12\x64\n\rCreateMessage\x12(.activitylogservice.CreateMessageRequest\x1a).activitylogservice.CreateMessageResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'activity_log_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_CREATEMESSAGEREQUEST']._serialized_start=42
  _globals['_CREATEMESSAGEREQUEST']._serialized_end=85
  _globals['_CREATEMESSAGERESPONSE']._serialized_start=87
  _globals['_CREATEMESSAGERESPONSE']._serialized_end=143
  _globals['_ACTIVITYLOGSERVICE']._serialized_start=145
  _globals['_ACTIVITYLOGSERVICE']._serialized_end=267
# @@protoc_insertion_point(module_scope)
