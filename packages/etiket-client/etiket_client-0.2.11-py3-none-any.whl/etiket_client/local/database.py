from etiket_client.settings.folders import get_sql_url

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from etiket_client.local.model import Base
from etiket_client.sync.database.models_db import SyncBase
from etiket_client.sync.database.start_up import start_up

from alembic.config import Config
from alembic import command

import os, etiket_client

engine = create_engine(get_sql_url(), echo=False)
Session = sessionmaker(engine)

# TODO user resources lib!!
with engine.begin() as connection:
    etiket_client_directory = os.path.dirname(os.path.dirname(etiket_client.__file__))
    alembic_cfg = Config(os.path.join(etiket_client_directory, 'alembic.ini'))
    alembic_cfg.attributes['connection'] = connection
    alembic_cfg.set_main_option("script_location",
                f"{os.path.dirname(etiket_client.__file__)}/local/alembic")
    command.upgrade(alembic_cfg, "head")

with Session() as session:
    start_up(session)