# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: _proto/runtime/runtime_shared/v2/config.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n-_proto/runtime/runtime_shared/v2/config.proto\x12 _proto.runtime.runtime_shared.v2"\x8e\x01\n\x10\x42\x61seTaskMetadata\x12\x13\n\x0bshared_root\x18\x01 \x01(\t\x12\x0f\n\x07step_id\x18\x02 \x01(\t\x12\x44\n\ttask_type\x18\x03 \x01(\x0e\x32\x31._proto.runtime.runtime_shared.v2.RuntimeTaskType\x12\x0e\n\x06run_id\x18\x04 \x01(\t"J\n\x0b\x44\x61taCatalog\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x0b\n\x03url\x18\x05 \x01(\t\x12\x14\n\x0c\x64\x61talake_uri\x18\x06 \x01(\tJ\x04\x08\x01\x10\x02J\x04\x08\x03\x10\x05"9\n\x16\x42\x61seRunnerInstructions\x12\x1f\n\x17runtime_output_filepath\x18\x01 \x01(\t*\x87\x01\n\x0fRuntimeTaskType\x12!\n\x1dRUNTIME_TASK_TYPE_UNSPECIFIED\x10\x00\x12(\n$RUNTIME_TASK_TYPE_CREATE_IMPORT_PLAN\x10\x01\x12\'\n#RUNTIME_TASK_TYPE_APPLY_IMPORT_PLAN\x10\x02\x42\x32Z0github.com/BauplanLabs/runtime/runtime_shared/v2b\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, '_proto.runtime.runtime_shared.v2.config_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    _globals['DESCRIPTOR']._options = None
    _globals['DESCRIPTOR']._serialized_options = b'Z0github.com/BauplanLabs/runtime/runtime_shared/v2'
    _globals['_RUNTIMETASKTYPE']._serialized_start = 364
    _globals['_RUNTIMETASKTYPE']._serialized_end = 499
    _globals['_BASETASKMETADATA']._serialized_start = 84
    _globals['_BASETASKMETADATA']._serialized_end = 226
    _globals['_DATACATALOG']._serialized_start = 228
    _globals['_DATACATALOG']._serialized_end = 302
    _globals['_BASERUNNERINSTRUCTIONS']._serialized_start = 304
    _globals['_BASERUNNERINSTRUCTIONS']._serialized_end = 361
# @@protoc_insertion_point(module_scope)
