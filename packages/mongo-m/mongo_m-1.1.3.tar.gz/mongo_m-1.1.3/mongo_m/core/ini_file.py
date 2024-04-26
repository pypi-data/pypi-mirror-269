import configparser, os

__all__ = ['create_file_ini', 'get_config']

FILE = f"{os.getcwd()}/migration/config.ini"

def create_file_ini():
    config = configparser.ConfigParser()
    config['MONGO'] = {
        'host': 'localhost',
        'port': 27020,
        'user': 'devUser',
        'password': 'nbgfre736251',
        'database': 'queue_service',
        'module_path': 'migration'
    }
    with open(FILE, 'w') as f:
        config.write(f)

def get_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(FILE)
    return config