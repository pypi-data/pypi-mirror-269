from typing import Dict

import logging
logger = logging.getLogger(__name__)

def get_gates_formatted(snapshot : Dict) -> Dict:
    gates_dic = None
    try:
        gates = snapshot['station']['instruments']['gates']['parameters']
        gates_dic = {name: f"{g['value']} {g['unit']}" for name, g in gates.items() if name!='IDN'}
    except Exception:
        logger.exception("Error while parsing gates from snapshot")
    return gates_dic