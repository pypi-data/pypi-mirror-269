from everai.configmap.configmap import ConfigMap
import typing
from everai.api import API


class ConfigMapManager:
    def __init__(self):
        self.api = API()

    def create(self, name: str, data: typing.Dict[str, str]) -> ConfigMap:
        configmap = ConfigMap(name=name, data=data)
        v1secret = configmap.to_proto()
        resp = self.api.create_configmap(v1secret)
        return ConfigMap.from_proto(resp)

    def create_from_lines(self, name: str, lines: typing.List[str]) -> ConfigMap:
        data: typing.Dict[str, str] = {}

        for line in lines:
            key_value = line.split('=', 1)

            if len(key_value) == 2:
                data[key_value[0]] = key_value[1]
            else:
                data[key_value[0]] = ''
        return self.create(name, data)

    def create_from_file(self, name: str, file: str) -> ConfigMap:
        lines: typing.List[str] = []

        with open(file, "r") as f:
            lines = f.readlines()
            return self.create_from_lines(name, lines)

    def delete(self, name: str):
        self.api.delete_secret(name)

    def list(self) -> typing.List[ConfigMap]:
        resp = self.api.list_configmaps()
        list_secrets = [ConfigMap.from_proto(configmap) for configmap in resp]

        return list_secrets

    def get(self, name: str) -> ConfigMap:
        resp = self.api.get_configmap(name)
        return ConfigMap.from_proto(resp)
