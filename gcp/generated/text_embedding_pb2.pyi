from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SaveTextEmbeddingRequest(_message.Message):
    __slots__ = ["url"]
    URL_FIELD_NUMBER: _ClassVar[int]
    url: str
    def __init__(self, url: _Optional[str] = ...) -> None: ...

class SaveTextEmbeddingResponse(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: bool
    def __init__(self, status: bool = ...) -> None: ...

class GetPreferenceArticlesRequest(_message.Message):
    __slots__ = ["preference_text"]
    PREFERENCE_TEXT_FIELD_NUMBER: _ClassVar[int]
    preference_text: str
    def __init__(self, preference_text: _Optional[str] = ...) -> None: ...

class GetPreferenceArticlesResponse(_message.Message):
    __slots__ = ["article"]
    ARTICLE_FIELD_NUMBER: _ClassVar[int]
    article: _containers.RepeatedCompositeFieldContainer[PreferenceArticle]
    def __init__(self, article: _Optional[_Iterable[_Union[PreferenceArticle, _Mapping]]] = ...) -> None: ...

class PreferenceArticle(_message.Message):
    __slots__ = ["url", "summary"]
    URL_FIELD_NUMBER: _ClassVar[int]
    SUMMARY_FIELD_NUMBER: _ClassVar[int]
    url: str
    summary: str
    def __init__(self, url: _Optional[str] = ..., summary: _Optional[str] = ...) -> None: ...
