from collections.abc import Callable, Mapping


class AttributeNode:
    @property
    def source_info(self) -> SourceInfo: ...

    @property
    def value_source_info(self) -> SourceInfo: ...

    @property
    def name(self) -> str: ...

    @property
    def value(self) -> ObjectNode | ReferenceNode | NumericExpressionNode | StringExpressionNode | ListNode | DictNode | bool | int | float | str: ...

class DictNode:
    @property
    def source_info(self) -> SourceInfo: ...

    @property
    def items(self) -> list[KeyVal]: ...

class DocString:
    @property
    def source_info(self) -> SourceInfo: ...

    @property
    def lines(self) -> list[str]: ...

class ErrorLine:
    @property
    def where(self) -> LineInfo: ...

    @property
    def message(self) -> str: ...

class KeyVal:
    @property
    def key(self) -> str: ...

    @property
    def value(self) -> ObjectNode | ReferenceNode | NumericExpressionNode | StringExpressionNode | ListNode | DictNode | bool | int | float | str: ...

class LineInfo:
    @property
    def line(self) -> int: ...

    @property
    def column(self) -> int: ...

class LineRange:
    @property
    def begin(self) -> LineInfo: ...

    @property
    def end(self) -> LineInfo: ...

class ListNode:
    @property
    def source_info(self) -> SourceInfo: ...

    @property
    def items(self) -> list[ObjectNode | ReferenceNode | NumericExpressionNode | StringExpressionNode | ListNode | DictNode | bool | int | float | str]: ...

class NumericExpressionNode:
    @property
    def source_info(self) -> SourceInfo: ...

    @property
    def value(self) -> str: ...

    @property
    def references(self) -> list[ReferenceNode]: ...

class ObjectNode:
    @property
    def source_info(self) -> SourceInfo: ...

    @property
    def docstring(self) -> DocString: ...

    @property
    def classname(self) -> str: ...

    @property
    def id(self) -> str: ...

    @property
    def children(self) -> list[ObjectNode]: ...

    @property
    def attributes(self) -> list[AttributeNode]: ...

class Profile:
    def __init__(self, source: str) -> None: ...

    def values(self) -> dict:
        """Profile values."""

    def root(self) -> ObjectNode:
        """Profile AST root node."""

    def line_info(self, info: ObjectNode | ReferenceNode | NumericExpressionNode | StringExpressionNode | ListNode | DictNode | SourceInfo) -> LineRange:
        """Get line info for node."""

    def to_source(self) -> str:
        """Profile AST source representation."""

    def to_json_ast(self, eval_expressions: bool = True) -> str:
        """Profile AST JSON representation."""

    def to_updated_source(self, values: Mapping[str, int | float | str | bool]) -> str:
        """Original source with value substitutions."""

class ProfileError(Exception):
    pass

class ReferenceNode:
    @property
    def source_info(self) -> SourceInfo: ...

    @property
    def reference(self) -> str: ...

class SourceInfo:
    @property
    def offset(self) -> int: ...

    @property
    def length(self) -> int: ...

class StringExpressionNode:
    @property
    def source_info(self) -> SourceInfo: ...

    @property
    def fragments(self) -> list[str | ReferenceNode]: ...

def parse(src: str) -> Profile:
    """Parse profile source and create AST."""

def validate(profile: Profile, is_allowed_ref: Callable[[str], bool] = lambda ref: False) -> None:
    """Validate profile structure."""
