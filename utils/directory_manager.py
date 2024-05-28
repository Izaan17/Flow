from pathlib import Path


def get_project_root():
    """Get the path of the project master directory."""
    return Path(__file__).parent.parent


def create_dir_if_not_exists(dir_path: Path):
    """Create directory if it does not exist."""
    dir_path.mkdir(parents=True, exist_ok=True)


def get_app_dir():
    app_dir = Path.home() / 'Flow'
    create_dir_if_not_exists(app_dir)
    return app_dir


def get_storage_dir():
    storage_dir = get_app_dir() / 'Storage'
    create_dir_if_not_exists(storage_dir)
    return storage_dir


def get_icon_dir():
    return get_project_root() / 'icons'


def get_notes_dir():
    notes_dir = get_app_dir() / 'Notes'
    create_dir_if_not_exists(notes_dir)
    return notes_dir


if __name__ == '__main__':
    print(get_project_root())
    print(get_app_dir())
    print(get_storage_dir())
    print(get_icon_dir())
    print(get_notes_dir())
