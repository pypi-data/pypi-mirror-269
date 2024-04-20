from typing import Any, Optional, Text

def default_stream_factory(total_content_length, filename, content_type, content_length: Optional[Any] = ...): ...
def parse_form_data(environ, stream_factory: Optional[Any] = ..., charset: Text = ..., errors: Text = ...,
                    max_form_memory_size: Optional[Any] = ..., max_content_length: Optional[Any] = ...,
                    cls: Optional[Any] = ..., silent: bool = ...): ...
def exhaust_stream(f): ...

class FormDataParser:
    stream_factory: Any
    charset: Text
    errors: Text
    max_form_memory_size: Any
    max_content_length: Any
    cls: Any
    silent: Any
    def __init__(self, stream_factory: Optional[Any] = ..., charset: Text = ..., errors: Text = ...,
                 max_form_memory_size: Optional[Any] = ..., max_content_length: Optional[Any] = ..., cls: Optional[Any] = ...,
                 silent: bool = ...): ...
    def get_parse_func(self, mimetype, options): ...
    def parse_from_environ(self, environ): ...
    def parse(self, stream, mimetype, content_length, options: Optional[Any] = ...): ...
    parse_functions: Any

def is_valid_multipart_boundary(boundary): ...
def parse_multipart_headers(iterable): ...

class MultiPartParser:
    charset: Text
    errors: Text
    max_form_memory_size: Any
    stream_factory: Any
    cls: Any
    buffer_size: Any
    def __init__(self, stream_factory: Optional[Any] = ..., charset: Text = ..., errors: Text = ...,
                 max_form_memory_size: Optional[Any] = ..., cls: Optional[Any] = ..., buffer_size=...): ...
    def fail(self, message): ...
    def get_part_encoding(self, headers): ...
    def get_part_charset(self, headers) -> Text: ...
    def start_file_streaming(self, filename, headers, total_content_length): ...
    def in_memory_threshold_reached(self, bytes): ...
    def validate_boundary(self, boundary): ...
    def parse_lines(self, file, boundary, content_length, cap_at_buffer: bool = ...): ...
    def parse_parts(self, file, boundary, content_length): ...
    def parse(self, file, boundary, content_length): ...
