from pathlib import Path, PurePath
import yaml

class Configuration:
    config = {}

    @staticmethod
    def get_config_path(project, env):
        # env is a dict, if OS_CONFIG_DIR is exist;
        # return env.get("OS_CONFIG_DIR")；else return PurePath()
        config_dir_path = env.get("OS_CONFIG_DIR", PurePath("D:\\cq\\openlava-python", project).as_posix())
        config_file_path = PurePath(config_dir_path).joinpath(f"{project}.yaml").as_posix()
        return config_dir_path.strip(), config_file_path.strip()

    def setup(self, project, env):
        config_dir_path, config_file_path = self.get_config_path(project, env)
        if not Path(config_file_path).exists():
            raise ValueError(f"Not found config file: {config_file_path}")

        with open(config_file_path, 'r', encoding='utf-8') as f:
            try:
                object.__setattr__(self, "config", yaml.safe_load(f))
            except Exception as e:
                print(e)
                raise ValueError("Load config file error")

__all__ = ('Configuration',)