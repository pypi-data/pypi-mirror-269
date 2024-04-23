import typing

T = typing.TypeVar('T')


class TableField:
    property_name: str
    property_type: typing.Type[T]
    property_formatter: typing.Union[str, typing.Callable[[T], str]]
    header_name: str

    def __init__(self, property_name: str, header_name: typing.Optional[str] = None):
        self.property_name = property_name
        self.header_name = header_name if header_name is not None else property_name.upper()


class ShowMixin(object):
    TableFields: typing.List[TableField]
    WideTableExtraFields: typing.List[TableField]

    def table_title(self):
        ...