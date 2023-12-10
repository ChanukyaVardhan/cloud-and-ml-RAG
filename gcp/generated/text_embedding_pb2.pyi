from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SaveTextEmbeddingRequest(_message.Message):
    __slots__ = ("url",)
    URL_FIELD_NUMBER: _ClassVar[int]
    url: str
    def __init__(self, url: _Optional[str] = ...) -> None: ...

class SaveTextEmbeddingResponse(_message.Message):
    __slots__ = ("status",)
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: bool
    def __init__(self, status: bool = ...) -> None: ...

class GetSimilarityRequest(_message.Message):
    __slots__ = ("text1", "text2")
    TEXT1_FIELD_NUMBER: _ClassVar[int]
    TEXT2_FIELD_NUMBER: _ClassVar[int]
    text1: str
    text2: str
    def __init__(self, text1: _Optional[str] = ..., text2: _Optional[str] = ...) -> None: ...

class GetSimilarityResponse(_message.Message):
    __slots__ = ("text_similarity",)
    TEXT_SIMILARITY_FIELD_NUMBER: _ClassVar[int]
    text_similarity: _containers.RepeatedCompositeFieldContainer[TextSimilarity]
    def __init__(self, text_similarity: _Optional[_Iterable[_Union[TextSimilarity, _Mapping]]] = ...) -> None: ...

class TextSimilarity(_message.Message):
    __slots__ = ("text1", "text2", "similarity")
    TEXT1_FIELD_NUMBER: _ClassVar[int]
    TEXT2_FIELD_NUMBER: _ClassVar[int]
    SIMILARITY_FIELD_NUMBER: _ClassVar[int]
    text1: str
    text2: str
    similarity: float
    def __init__(self, text1: _Optional[str] = ..., text2: _Optional[str] = ..., similarity: _Optional[float] = ...) -> None: ...

class GetPreferenceArticlesRequest(_message.Message):
    __slots__ = ("preference_text", "start_time", "end_time", "num_matches")
    PREFERENCE_TEXT_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    NUM_MATCHES_FIELD_NUMBER: _ClassVar[int]
    preference_text: str
    start_time: _timestamp_pb2.Timestamp
    end_time: _timestamp_pb2.Timestamp
    num_matches: int
    def __init__(self, preference_text: _Optional[str] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., num_matches: _Optional[int] = ...) -> None: ...

class GetPreferenceArticlesResponse(_message.Message):
    __slots__ = ("article",)
    ARTICLE_FIELD_NUMBER: _ClassVar[int]
    article: _containers.RepeatedCompositeFieldContainer[PreferenceArticle]
    def __init__(self, article: _Optional[_Iterable[_Union[PreferenceArticle, _Mapping]]] = ...) -> None: ...

class PreferenceArticle(_message.Message):
    __slots__ = ("url", "summary", "similarity", "published_on")
    URL_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    SIMILARITY_FIELD_NUMBER: _ClassVar[int]
    PUBLISHED_ON_FIELD_NUMBER: _ClassVar[int]
    url: str
    summary: str
    similarity: float
    published_on: _timestamp_pb2.Timestamp
    def __init__(self, url: _Optional[str] = ..., summary: _Optional[str] = ..., similarity: _Optional[float] = ..., published_on: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
