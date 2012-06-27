#!/usr/bin/python
#
# The SkyLines daemon, responsible for live tracking (and maybe other
# Twisted applications).
#

import sys
sys.path.append('/opt/skylines/src')

from paste.deploy.loadwsgi import appconfig
from skylines.config.environment import load_environment

conf = appconfig('config:/etc/skylines/production.ini')
load_environment(conf.global_conf, conf.local_conf)

if __name__ == '__main__':
    from twisted.internet import reactor
    from skylines.tracking.server import TrackingServer
    reactor.listenUDP(5597, TrackingServer())
    reactor.run()