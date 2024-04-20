from yaml.emitter import Emitter
from yaml.serializer import Serializer
from yaml.representer import BaseRepresenter, Representer, SafeRepresenter
from yaml.resolver import BaseResolver, Resolver

class BaseDumper(Emitter, Serializer, BaseRepresenter, BaseResolver):
    def __init__(self, stream, default_style=..., default_flow_style=..., canonical=..., indent=..., width=..., allow_unicode=..., line_break=..., encoding=..., explicit_start=..., explicit_end=..., version=..., tags=...) -> None: ...

class SafeDumper(Emitter, Serializer, SafeRepresenter, Resolver):
    def __init__(self, stream, default_style=..., default_flow_style=..., canonical=..., indent=..., width=..., allow_unicode=..., line_break=..., encoding=..., explicit_start=..., explicit_end=..., version=..., tags=...) -> None: ...

class Dumper(Emitter, Serializer, Representer, Resolver):
    def __init__(self, stream, default_style=..., default_flow_style=..., canonical=..., indent=..., width=..., allow_unicode=..., line_break=..., encoding=..., explicit_start=..., explicit_end=..., version=..., tags=...) -> None: ...
