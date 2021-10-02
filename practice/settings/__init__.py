from pathlib import Path

import environ

from split_settings.tools import include

# https://github.com/joke2k/django-environ
env_file = Path(__file__).parent.parent.parent.joinpath("config", ".env")
environ.Env.read_env(env_file=env_file.as_posix())

env = environ.Env(DJANGO_DEBUG=bool)

ENVIRONMENT = env("DJANGO_ENV")

base_settings = [
    "components/base.py",  # standard django settings
    "components/database.py",  # databases
    "components/static.py",
    "components/email.py",  # smtp
    "components/cache.py",
    "components/background.py",

    # Select the right env:
    "environments/%s.py" % ENVIRONMENT,

]

# Include settings:
include(*base_settings)
