import typing

from everai.app.context import context


class Placeholder:
    def __init__(self, name: str, key: str,
                 kind: typing.Literal['ConfigMap', "Secret"] = 'Secret'):
        self.name = name
        self.key = key
        self.kind = kind

    def __call__(self) -> str:

        match self.kind:
            case 'ConfigMap':
                holder = context.get_configmap(self.name)
            case 'Secret':
                holder = context.get_secret(self.name)
            case _:
                raise ValueError(f'Unsupported placeholder kind {self.kind}')

        assert holder is not None

        value = holder.get(self.key)
        assert value is not None

        return value
