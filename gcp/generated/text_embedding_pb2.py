# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: text_embedding.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14text_embedding.proto\x12\x0etext_embedding\"\'\n\x18SaveTextEmbeddingRequest\x12\x0b\n\x03url\x18\x01 \x01(\t\"+\n\x19SaveTextEmbeddingResponse\x12\x0e\n\x06status\x18\x01 \x01(\x08\"7\n\x1cGetPreferenceArticlesRequest\x12\x17\n\x0fpreference_text\x18\x01 \x01(\t\"S\n\x1dGetPreferenceArticlesResponse\x12\x32\n\x07\x61rticle\x18\x01 \x03(\x0b\x32!.text_embedding.PreferenceArticle\"1\n\x11PreferenceArticle\x12\x0b\n\x03url\x18\x01 \x01(\t\x12\x0f\n\x07summary\x18\x02 \x01(\t2\xef\x01\n\rTextEmbedding\x12h\n\x11SaveTextEmbedding\x12(.text_embedding.SaveTextEmbeddingRequest\x1a).text_embedding.SaveTextEmbeddingResponse\x12t\n\x15GetPreferenceArticles\x12,.text_embedding.GetPreferenceArticlesRequest\x1a-.text_embedding.GetPreferenceArticlesResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'text_embedding_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_SAVETEXTEMBEDDINGREQUEST']._serialized_start=40
  _globals['_SAVETEXTEMBEDDINGREQUEST']._serialized_end=79
  _globals['_SAVETEXTEMBEDDINGRESPONSE']._serialized_start=81
  _globals['_SAVETEXTEMBEDDINGRESPONSE']._serialized_end=124
  _globals['_GETPREFERENCEARTICLESREQUEST']._serialized_start=126
  _globals['_GETPREFERENCEARTICLESREQUEST']._serialized_end=181
  _globals['_GETPREFERENCEARTICLESRESPONSE']._serialized_start=183
  _globals['_GETPREFERENCEARTICLESRESPONSE']._serialized_end=266
  _globals['_PREFERENCEARTICLE']._serialized_start=268
  _globals['_PREFERENCEARTICLE']._serialized_end=317
  _globals['_TEXTEMBEDDING']._serialized_start=320
  _globals['_TEXTEMBEDDING']._serialized_end=559
# @@protoc_insertion_point(module_scope)
