import typing

T = typing.TypeVar('T')


class TableField:
    property_name: str
    header_name: str

    def __init__(self, property_name: str, header_name: typing.Optional[str] = None):
        self.property_name = property_name
        self.header_name = header_name if header_name is not None else property_name.upper()


class ShowMixin(object):
    # class property
    table_fields: typing.List[TableField] = []
    wide_table_extra_fields: typing.List[TableField] = []

    @classmethod
    def table_title(cls, wide: bool = False) -> typing.List[str]:
        fields = cls.table_fields.copy()
        if wide:
            fields.append(*cls.wide_table_extra_fields)

        return [field.header_name for field in fields]

    def table_row(self, wide: bool = False) -> typing.List:
        result = []

        def add_fields(fields: typing.List[TableField]):
            for field in fields:
                if not hasattr(self, field.property_name):
                    result.append('None')
                    continue
                value = getattr(self, field.property_name)
                result.append(value)

        add_fields(self.table_fields)
        if wide:
            add_fields(self.wide_table_extra_fields)

        return result
