"""
Handles file transfer via `cp`
"""

from remotemanager.transport.transport import Transport

import logging

logger = logging.getLogger(__name__)


class cp(Transport):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        logger.info("created new cp transport")

    def cmd(self, primary, secondary):
        cmd = "mkdir -p {secondary} ; cp -r --preserve {primary} {secondary}"
        base = cmd.format(primary=primary, secondary=secondary)
        logger.debug(f'returning formatted cmd: "{base}"')
        return base
