import json
import sys

import yaml


class Config:
    """
    环境配置，使用 yml 文件。
    例如:
    ```
    active: local
    school-server:
    local:
    shared:
    ```
    active 必需标识启用的环境。
    后续使用 key: 环境配置的方式可以定义多个环境。
    shared: 是共用的配置。
    """

    def __init__(self, config_file='config.yml'):
        """
        构造函数。
        Args:
            config_file: 配置文件所在位置，默认 config.yml。
        """
        self.config_file = config_file
        with open(config_file) as f:
            self.original = yaml.load(f, Loader=yaml.FullLoader)
            self.active_profile = self.original['active']
            if self.active_profile is None:
                raise ValueError("No active profile")

            shared_key = 'shared'

            if self.active_profile == shared_key:
                raise ValueError("[shared] is a shared configuration.")

            print(f"Active profile[{self.active_profile}].")
            sys.stdout.flush()

            self.configs = self.original[self.active_profile]  # type: dict
            if self.configs is None:
                print(f"Active profile[{self.active_profile}] has no arguments.", file=sys.stderr)
                sys.stderr.flush()
                self.configs = {}

            # 添加共用部分, 如果存在一样的 key, 则使用 active 激活的配置内的
            if shared_key in self.original:
                self.configs = self._merge_dicts(self.original[shared_key], self.configs)

    def __getitem__(self, item):
        if self.configs.__contains__(item):
            return self.configs[item]
        key = item.replace("_", "-")
        if self.configs.__contains__(key):
            return self.configs[key]
        return None

    def __str__(self):
        return json.dumps(self.original)

    def _merge_dicts(self, dict1: dict, dict2: dict, keys=None):
        """
        递归合并两个字典, 保证 dict1, dict2 字段合并, 如果同时存在则保留 dict2 的。
        Args:
            dict1 (dict): 合并的第一个词典.
            dict2 (dict): 合并的第二个词典, 里面的值会覆盖 dict1 的值。
        Returns:
            dict: 合并后的字典.
        """
        if keys is None:
            keys = []
        merged = dict1.copy()

        for key, value in dict2.items():
            keys.append(key)
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                # 合并子级
                merged[key] = self._merge_dicts(merged[key], value, keys)
            else:
                old_value = merged[key] if key in merged else None
                merged[key] = value
                if old_value is not None:
                    print(f"键 '{':'.join(keys)}' 存在于 [shared] 和 [{self.active_profile}] 中, "
                          f"值变换 {old_value} --> {value}, 只保留 {value}")
            keys.remove(key)

        return merged
