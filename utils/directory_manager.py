import os
from pathlib import Path


def get_project_root():
    """Get the path of the project master directory."""
    return Path(__file__).parent.parent


def get_app_dir():
    app_dir = os.path.join(os.path.expanduser('~'), 'Flow')
    if not os.path.exists(app_dir):
        os.mkdir(app_dir)
    return app_dir


def get_storage_dir():
    storage_dir = os.path.join(get_app_dir(), 'Storage')
    if not os.path.exists(storage_dir):
        os.mkdir(storage_dir)
    return storage_dir


def get_icon_dir():
    return os.path.join(get_project_root(), 'icons')


if __name__ == '__main__':
    print(get_project_root())
    print(get_app_dir())
    print(get_storage_dir())
