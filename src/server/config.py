# pip install python-decouple
from decouple import config as decouple_config, RepositoryEnv


DATABASE_URL = decouple_config("DATABASE_URL", default="")
