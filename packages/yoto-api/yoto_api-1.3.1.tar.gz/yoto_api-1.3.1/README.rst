Introduction
============

Early days of this API. Plan is to use this for home assistant. Basics are only item build for auth so far.

To run this code for test I am doing::

    from pathlib import Path
    import logging
    import sys
    import os

    path_root = r"C:path to files GitHub\main\yoto_api"
    sys.path.append(str(path_root))
    from yoto_api import *

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)

    ym = YotoManager(username="username", password="password")
    ym.check_and_refresh_token()
    ym.update_player_status()
    print (ym.players)
