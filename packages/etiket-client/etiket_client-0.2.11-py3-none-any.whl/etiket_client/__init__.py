from etiket_client.settings.logging import set_up_logging
set_up_logging(__name__)

from etiket_client.sync.proc import start_sync_agent
from etiket_client.remote.authenticate import login, logout

start_sync_agent()