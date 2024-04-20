# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: runner_task.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x11runner_task.proto\x12\x07\x62\x61uplan"\x86\x01\n\x05Mount\x12\x1a\n\x12source_object_path\x18\x01 \x01(\t\x12\x18\n\x10source_object_id\x18\x02 \x01(\t\x12\x16\n\x0esource_content\x18\x03 \x01(\t\x12\x0e\n\x06target\x18\x04 \x01(\t\x12\x0c\n\x04mode\x18\x05 \x01(\t\x12\x11\n\tlifecycle\x18\x06 \x01(\t""\n\x03\x45nv\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t"\x14\n\x04Port\x12\x0c\n\x04port\x18\x01 \x01(\x05"7\n\x08LogGroup\x12\n\n\x02id\x18\x01 \x01(\t\x12\x11\n\tparent_id\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t"]\n\x0eTaskInputModel\x12\n\n\x02id\x18\x01 \x01(\t\x12\x16\n\x0esource_task_id\x18\x02 \x01(\t\x12\x12\n\ntable_name\x18\x03 \x01(\t\x12\x13\n\x0b\x66ile_format\x18\x04 \x01(\t"^\n\x0fTaskOutputModel\x12\n\n\x02id\x18\x01 \x01(\t\x12\x16\n\x0esource_task_id\x18\x02 \x01(\t\x12\x12\n\ntable_name\x18\x03 \x01(\t\x12\x13\n\x0b\x66ile_format\x18\x04 \x01(\t"\xbb\x02\n\x0cTaskMetadata\x12.\n\x05level\x18\x01 \x01(\x0e\x32\x1f.bauplan.TaskMetadata.TaskLevel\x12 \n\x18human_readable_task_type\x18\x02 \x01(\t\x12\x11\n\ttask_type\x18\x03 \x01(\t\x12\x1a\n\rfunction_name\x18\x04 \x01(\tH\x00\x88\x01\x01\x12\x18\n\x0bline_number\x18\x05 \x01(\x05H\x01\x88\x01\x01\x12\x16\n\tfile_name\x18\x06 \x01(\tH\x02\x88\x01\x01\x12\x17\n\nmodel_name\x18\x07 \x01(\tH\x03\x88\x01\x01" \n\tTaskLevel\x12\x07\n\x03\x44\x41G\x10\x00\x12\n\n\x06SYSTEM\x10\x01\x42\x10\n\x0e_function_nameB\x0e\n\x0c_line_numberB\x0c\n\n_file_nameB\r\n\x0b_model_name"@\n\x0cTaskExitCode\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x05\x12\r\n\x05\x66\x61tal\x18\x02 \x01(\x08\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t"\xc1\x06\n\x04Task\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x13\n\x06region\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\x18\n\x0b\x62ucket_name\x18\x03 \x01(\tH\x01\x88\x01\x01\x12\x17\n\nobject_key\x18\x04 \x01(\tH\x02\x88\x01\x01\x12\x11\n\x04hash\x18\x05 \x01(\tH\x03\x88\x01\x01\x12\x11\n\x04name\x18\x06 \x01(\tH\x04\x88\x01\x01\x12\x15\n\x08image_id\x18\x07 \x01(\tH\x05\x88\x01\x01\x12\x17\n\nimage_name\x18\x08 \x01(\tH\x06\x88\x01\x01\x12\x17\n\x0finput_model_ids\x18\t \x03(\t\x12\x17\n\nmodel_name\x18\n \x01(\tH\x07\x88\x01\x01\x12\x30\n\ninput_data\x18\x0b \x03(\x0b\x32\x1c.bauplan.Task.InputDataEntry\x12\x0f\n\x07\x63ommand\x18\x0c \x03(\t\x12\x1e\n\x06mounts\x18\r \x03(\x0b\x32\x0e.bauplan.Mount\x12\x1a\n\x04\x65nvs\x18\x0e \x03(\x0b\x32\x0c.bauplan.Env\x12\x1c\n\x05ports\x18\x0f \x03(\x0b\x32\r.bauplan.Port\x12\x1d\n\x10isolated_network\x18\x10 \x01(\x08H\x08\x88\x01\x01\x12\x12\n\ncan_invoce\x18\x11 \x03(\t\x12\x14\n\x07workdir\x18\x12 \x01(\tH\t\x88\x01\x01\x12\x14\n\x07network\x18\x13 \x01(\tH\n\x88\x01\x01\x12,\n\x08metadata\x18\x14 \x01(\x0b\x32\x15.bauplan.TaskMetadataH\x0b\x88\x01\x01\x12-\n\x0cinput_models\x18\x15 \x03(\x0b\x32\x17.bauplan.TaskInputModel\x12/\n\routput_models\x18\x16 \x03(\x0b\x32\x18.bauplan.TaskOutputModel\x1a\x30\n\x0eInputDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\t\n\x07_regionB\x0e\n\x0c_bucket_nameB\r\n\x0b_object_keyB\x07\n\x05_hashB\x07\n\x05_nameB\x0b\n\t_image_idB\r\n\x0b_image_nameB\r\n\x0b_model_nameB\x13\n\x11_isolated_networkB\n\n\x08_workdirB\n\n\x08_networkB\x0b\n\t_metadataB?Z=github.com/BauplanLabs/playground/commander-service/protobufsb\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'runner_task_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    _globals['DESCRIPTOR']._options = None
    _globals[
        'DESCRIPTOR'
    ]._serialized_options = b'Z=github.com/BauplanLabs/playground/commander-service/protobufs'
    _globals['_TASK_INPUTDATAENTRY']._options = None
    _globals['_TASK_INPUTDATAENTRY']._serialized_options = b'8\001'
    _globals['_MOUNT']._serialized_start = 31
    _globals['_MOUNT']._serialized_end = 165
    _globals['_ENV']._serialized_start = 167
    _globals['_ENV']._serialized_end = 201
    _globals['_PORT']._serialized_start = 203
    _globals['_PORT']._serialized_end = 223
    _globals['_LOGGROUP']._serialized_start = 225
    _globals['_LOGGROUP']._serialized_end = 280
    _globals['_TASKINPUTMODEL']._serialized_start = 282
    _globals['_TASKINPUTMODEL']._serialized_end = 375
    _globals['_TASKOUTPUTMODEL']._serialized_start = 377
    _globals['_TASKOUTPUTMODEL']._serialized_end = 471
    _globals['_TASKMETADATA']._serialized_start = 474
    _globals['_TASKMETADATA']._serialized_end = 789
    _globals['_TASKMETADATA_TASKLEVEL']._serialized_start = 694
    _globals['_TASKMETADATA_TASKLEVEL']._serialized_end = 726
    _globals['_TASKEXITCODE']._serialized_start = 791
    _globals['_TASKEXITCODE']._serialized_end = 855
    _globals['_TASK']._serialized_start = 858
    _globals['_TASK']._serialized_end = 1691
    _globals['_TASK_INPUTDATAENTRY']._serialized_start = 1482
    _globals['_TASK_INPUTDATAENTRY']._serialized_end = 1530
# @@protoc_insertion_point(module_scope)
