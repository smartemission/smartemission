import os

# local config, change on server for real config
config = {
    'database': os.getenv('SOSEMU_DB_NAME', 'gis'),
    'host': os.getenv('SOSEMU_DB_HOST', 'postgis'),
    'port': os.getenv('SOSEMU_DB_PORT', '5432'),
    'schema': os.getenv('SOSEMU_DB_SCHEMA', 'smartem_rt'),
    'user': os.getenv('SOSEMU_DB_USER', 'the_user'),
    'password': os.getenv('SOSEMU_DB_PASSWORD', 'the_password')
}
