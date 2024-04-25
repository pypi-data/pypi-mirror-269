import yaml

from everai.configmap.configmap import ConfigMap
import typing
from everai.api import API
from .utils import literals_to_dict, file_to_dict

class ConfigMapManager:
    def __init__(self):
        self.api = API()

    def create(self, name: str, data: typing.Dict[str, str]) -> ConfigMap:
        configmap = ConfigMap(name=name, data=data)
        v1configmap = configmap.to_proto()
        resp = self.api.create_configmap(v1configmap)
        return ConfigMap.from_proto(resp)

    def update(self, name: str, data: typing.Dict[str, str]) -> ConfigMap:
        configmap = ConfigMap(name=name, data=data)
        v1configmap = configmap.to_proto()
        resp = self.api.update_configmap(v1configmap)
        return ConfigMap.from_proto(resp)

    def create_from_literal(self, name: str, literals: typing.List[str]) -> ConfigMap:
        data = literals_to_dict(literals=literals)
        return self.create(name, data)

    def update_from_literal(self, name: str, literals: typing.List[str]) -> ConfigMap:
        data = literals_to_dict(literals=literals)
        return self.update(name, data)

    def create_from_file(self, name: str, file: str) -> ConfigMap:
        data = file_to_dict(file)
        return self.create(name, data)

    def update_from_file(self, name: str, file: str) -> ConfigMap:
        data = file_to_dict(file)
        return self.update(name, data)

    def delete(self, name: str):
        self.api.delete_secret(name)

    def list(self) -> typing.List[ConfigMap]:
        resp = self.api.list_configmaps()
        list_secrets = [ConfigMap.from_proto(configmap) for configmap in resp]

        return list_secrets

    def get(self, name: str) -> ConfigMap:
        resp = self.api.get_configmap(name)
        return ConfigMap.from_proto(resp)
