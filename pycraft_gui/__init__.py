import os
install_path = os.path.dirname(__file__)
_data_dir = os.path.join(install_path, 'data')
def get_data_dir():
    return _data_dir if os.path.exists(_data_dir) else None

_themes_dir = os.path.join(_data_dir, 'themes')
def get_themes_dir():
    return _themes_dir if os.path.exists(_themes_dir) else None