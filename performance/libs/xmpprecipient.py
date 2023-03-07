#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of Pulse 2, http://www.siveo.net
#
# Pulse 2 is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Pulse 2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pulse 2; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.
import sys, os
import logging
import ConfigParser
import sleekxmpp
import netifaces
import random
from sleekxmpp.exceptions import IqError, IqTimeout
import json
import hashlib
import datetime
from optparse import OptionParser
import base64
import copy
import traceback
from datetime import datetime
import time


def file_put_contents_w_a(filename, data, option = "w"):
    if option == "a" or  option == "w":
        f = open( filename, option )
        f.write(data)
        f.close()

def file_put_contents(filename,  data):
    """
    write content "data" to file "filename"
    """
    f = open(filename, 'w')
    f.write(data)
    f.close()

def add_coloring_to_emit_windows(fn):
        # add methods we need to the class
    # def _out_handle(self):
        #import ctypes
        # return ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)
    #out_handle = property(_out_handle)

    def _set_color(self, code):
        import ctypes
        # Constants from the Windows API
        self.STD_OUTPUT_HANDLE = -11
        hdl = ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)
        ctypes.windll.kernel32.SetConsoleTextAttribute(hdl, code)

    setattr(logging.StreamHandler, '_set_color', _set_color)

    def new(*args):
        FOREGROUND_BLUE = 0x0001  # text color contains blue.
        FOREGROUND_GREEN = 0x0002  # text color contains green.
        FOREGROUND_RED = 0x0004  # text color contains red.
        FOREGROUND_INTENSITY = 0x0008  # text color is intensified.
        FOREGROUND_WHITE = FOREGROUND_BLUE | FOREGROUND_GREEN | FOREGROUND_RED
       # winbase.h
        #STD_INPUT_HANDLE = -10
        #STD_OUTPUT_HANDLE = -11
        #STD_ERROR_HANDLE = -12

        # wincon.h
        #FOREGROUND_BLACK     = 0x0000
        FOREGROUND_BLUE = 0x0001
        FOREGROUND_GREEN = 0x0002
        #FOREGROUND_CYAN      = 0x0003
        FOREGROUND_RED = 0x0004
        FOREGROUND_MAGENTA = 0x0005
        FOREGROUND_YELLOW = 0x0006
        #FOREGROUND_GREY      = 0x0007
        FOREGROUND_INTENSITY = 0x0008  # foreground color is intensified.

        #BACKGROUND_BLACK     = 0x0000
        #BACKGROUND_BLUE      = 0x0010
        #BACKGROUND_GREEN     = 0x0020
        #BACKGROUND_CYAN      = 0x0030
        #BACKGROUND_RED       = 0x0040
        #BACKGROUND_MAGENTA   = 0x0050
        BACKGROUND_YELLOW = 0x0060
        #BACKGROUND_GREY      = 0x0070
        BACKGROUND_INTENSITY = 0x0080  # background color is intensified.

        levelno = args[1].levelno
        if(levelno >= 50):
            color = BACKGROUND_YELLOW | FOREGROUND_RED | FOREGROUND_INTENSITY | BACKGROUND_INTENSITY
        elif(levelno >= 40):
            color = FOREGROUND_RED | FOREGROUND_INTENSITY
        elif(levelno >= 30):
            color = FOREGROUND_YELLOW | FOREGROUND_INTENSITY
        elif(levelno >= 20):
            color = FOREGROUND_GREEN
        elif(levelno >= 10):
            color = FOREGROUND_MAGENTA
        else:
            color = FOREGROUND_WHITE
        args[0]._set_color(color)

        ret = fn(*args)
        args[0]._set_color(FOREGROUND_WHITE)
        # print "after"
        return ret
    return new


def add_coloring_to_emit_ansi(fn):
    # add methods we need to the class
    def new(*args):
        levelno = args[1].levelno
        if(levelno >= 50):
            color = '\x1b[31m'  # red
        elif(levelno >= 40):
            color = '\x1b[31m'  # red
        elif(levelno >= 30):
            color = '\x1b[33m'  # yellow
        elif(levelno >= 20):
            color = '\x1b[32m'  # green
        elif(levelno >= 10):
            color = '\x1b[35m'  # pink
        else:
            color = '\x1b[0m'  # normal
        args[1].msg = color + str(args[1].msg) + '\x1b[0m'  # normal
        # print "after"
        return fn(*args)
    return new

class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """

    def __init__(self, logger, debug=logging.INFO):
        self.logger = logger
        self.debug = debug
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.debug, line.rstrip())


class configuration(object):
    def __init__(self, relayserver):
        Config = ConfigParser.ConfigParser()
        if relayserver == True:
            Config.read("/etc/pulse-xmpp-agent/relayconf.ini")
            if os.path.exists("/etc/pulse-xmpp-agent/relayconf.ini.local"):
                Config.read("/etc/pulse-xmpp-agent/relayconf.ini.local")
        else:
            Config.read("/etc/mmc/plugins/xmppmaster.ini")
            if os.path.exists("/etc/mmc/plugins/xmppmaster.ini.local"):
                Config.read("/etc/mmc/plugins/xmppmaster.ini.local")


        if  Config.has_option("connection", "password"):
            self.Password = Config.get('connection', 'password')

        if  Config.has_option("connection", "port"):
            self.Port = Config.get('connection', 'port')
        else :
            self.Port = 5222

        if  Config.has_option("connection", "Server"):
            self.Server = Config.get('connection', 'Server')

        if  Config.has_option("chat", "domain"):
            self.Chatadress = Config.get('chat', 'domain')

        self.Jid = "recvcharge@%s/recvcharge"% self.Chatadress
        self.master = "master@%s/MASTER"%self.Chatadress

        if  Config.has_option("global", "log_level"):
            self.log_level = Config.get('global', 'log_level')
        else:
            self.log_level = "INFO"

#global
        if self.log_level == "INFO":
            self.debug = logging.INFO
        elif self.log_level == "DEBUG":
            self.debug = logging.DEBUG
        elif self.log_level == "ERROR":
            self.debug = logging.ERROR
        else:
            self.debug = 5


    def getRandomName(self, nb, pref=""):
        a="abcdefghijklnmopqrstuvwxyz"
        d=pref
        for t in range(nb):
            d=d+a[random.randint(0,25)]
        return d

    def getRandomNameID(self, nb, pref=""):
        a="0123456789"
        d=pref
        for t in range(nb):
            d=d+a[random.randint(0,9)]
        return d

    def get_local_ip_adresses(self):
        ip_addresses = list()
        interfaces = netifaces.interfaces()
        for i in interfaces:
            if i == 'lo':
                continue
            iface = netifaces.ifaddresses(i).get(netifaces.AF_INET)
            if iface:
                for j in iface:
                    addr = j['addr']
                    if addr != '127.0.0.1':
                        ip_addresses.append(addr)
        return ip_addresses

    #def __str__(self):
        #return str(self.re)

    def jsonobj(self):
        return json.dumps(self.re)

def getRandomName(nb, pref=""):
    a="abcdefghijklnmopqrstuvwxyz0123456789"
    d=pref
    for t in range(nb):
        d=d+a[random.randint(0,35)]
    return d


def md5(fname):
    hash = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    return hash.hexdigest()


if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


class MUCBot(sleekxmpp.ClientXMPP):
    def __init__(self,conf):#jid, password, room, nick):
        sleekxmpp.ClientXMPP.__init__(self, conf.Jid, conf.Password)
        self.config = conf
        self.add_event_handler("register", self.register, threaded=True)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler('message', self.message)
        print conf.nbmessage
        print conf.nbmicro

        self.msg = {
                    "action": "testcharge",
                    "sessionid" : getRandomName(6, "testcharge"),
                    "ret" : 0,
                    "base64" : False,
                    'data' : { "nb" : 1,
                               "text" : base64.b64encode("Et quoniam inedia gravi adflictabantur, locum petivere")}
        }

    def start(self, event):
        self.get_roster()
        self.send_presence()

    def register(self, iq):
        """ This function is called for automatic registration """
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password

        try:
            resp.send(now=True)
            logging.info("Account created for %s!" % self.boundjid)
        except IqError as e:
            logging.error("Could not register account: %s" %
                    e.iq['error']['text'])
            #self.disconnect()
        except IqTimeout:
            logging.error("No response from server.")
            self.disconnect()

    def message(self, msg):
        tmps1=time.time()
        print "message received size %s"%len(str(msg['body']))
        if not conf.noprocess:
            print "trying to decode message"
            try:
                try:
                    # data = json.loads(json.loads(msg['body']))
                    data = json.loads(msg['body'])
                except Exception as e:
                    print "Message cannot be processed as a JSON: [%s]"%str(e)
                    raise
                print "JSON message decoded"
                if "data" in data:
                    if 'action' in data:
                        print "Action: %s"%data['action']
                    if 'sessionid' in data:
                        print "Session ID: %s"%data['sessionid']
                try:
                    if "nb" in data['data']:
                        print data['data']['nb']
                        if data['data']['nb'] == 0:
                            file_put_contents("/tmp/testcharge_agenttest_recv.txt",
                                              "%s : %s\n"%(str(datetime.now()),str(data['data']['nb']) ) )
                        else:
                            tmps2=time.time()-tmps1
                            #file_put_contents_w_a("/tmp/testcharge_agenttest_recv.txt",
                            #                    "%s : message received  size : %s | num %s execution time %s \n"%(str(datetime.now()),len(str(msg['body'])), str(data['data']['nb']), tmps2),
                            #                    "a")
                            file_put_contents_w_a("/tmp/testcharge_agenttest_recv.txt",
                                                  "%s : %s\n"%(str(datetime.now()),str(data['data']['nb']) ),
                                                  "a")
                    else:
                        print json.dumps(data, indent=4)

                except Exception as e:
                    print ("Error in plugin %s : %s" % (action, str(e)))
                    pass
            except Exception as e:
                print "error : [%s]"%str(e)
                pass
        else:
            tmps2=time.time()-tmps1
            #file_put_contents_w_a("/tmp/agenttestRecv.txt",
            #                                    "%s : message received  size : %s execution time %s \n"%(str(datetime.now()), len(str(msg['body'])), tmps2),
            #                                    "a")
            file_put_contents_w_a("/tmp/testcharge_agenttest_recv.txt",
                                  "%s : %s\n"%(str(datetime.now()),str(data['data']['nb']) ),
                                  "a")

def createDaemon(opts,conf):
    """
        This function create a service/Daemon that will execute a det. task
    """
    try:
        pid = os.fork()
        if pid > 0:
            print 'PID: %d' % pid
            os._exit(0)
        doTask(opts,conf)
    except OSError, error:
        logging.error("Unable to fork. Error: %d (%s)" % (error.errno, error.strerror))
        traceback.print_exc(file=sys.stdout)
        os._exit(1)


def doTask(opts, conf):
    logging.StreamHandler.emit = add_coloring_to_emit_ansi(logging.StreamHandler.emit)
    #logging.basicConfig(level = logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


    if opts.consoledebug :
            logging.basicConfig(level = logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        stdout_logger = logging.getLogger('STDOUT')
        sl = StreamToLogger(stdout_logger, logging.INFO)
        sys.stdout = sl
        stderr_logger = logging.getLogger('STDERR')
        sl = StreamToLogger(stderr_logger, logging.INFO)
        sys.stderr = sl
        logging.basicConfig(level = logging.INFO,
                            format ='[%(name)s.%(funcName)s:%(lineno)d] %(message)s',
                            filename = "/var/log/pulse/xmpp-agent-log.log",
                            filemode = 'a')
    xmpp = MUCBot(conf)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0045') # Multi-User Chat
    xmpp.register_plugin('xep_0199', {'keepalive': True, 'frequency':600, 'interval' : 600, 'timeout' : 500  })
    xmpp.register_plugin('xep_0077') # In-band Registration
    xmpp['xep_0077'].force_registration = True

    # Connect to the XMPP server and start processing XMPP stanzas.address=(args.host, args.port)
    if xmpp.connect(address=(conf.Server,conf.Port)):
        # If you do not have the dnspython library installed, you will need
        # to manually specify the name of the server if it does not match
        # the one in the JID. For example, to use Google Talk you would
        # need to use:
        #
        # if xmpp.connect(('talk.google.com', 5222)):
        xmpp.process(block=True)
        print("Done")
    else:
        print("Unable to connect.")

if __name__ == '__main__':
    if not sys.platform.startswith('linux'):
        print "Agent log on systeme linux only"


    if os.getuid() != 0:
        print "Agent must be running as root"
        sys.exit(0)

    optp = OptionParser()
    optp.add_option("-d",
                    "--deamon",
                    action = "store_true",
                    dest = "deamon",
                    default = False,
                    help = "Deamonize process")

    optp.add_option("-c",
                    "--consoledebug",
                    action = "store_true",
                    dest = "consoledebug",
                    default = True,
                    help = "Debug console")

    optp.add_option("-p",
                    "--noprocess",
                    action = "store_true",
                    dest = "noprocess",
                    default = False,
                    help = "Do not decode or process JSON")

    optp.add_option("-n", "--nbsend",
                dest="nbsend", default="1000",
                help="Number of messages to be sent")

    optp.add_option("-s", "--nbmicroseconde",
                dest="nbmicro", default="0",
                help="Number of seconds between 2 messages")

    optp.add_option("-r", "--relayserver",
                action = "store_true",
                dest="relayserver",
                default = False,
                help="Run on relay server")

    opts, args = optp.parse_args()

    # Setup the command line arguments.
    conf  = configuration(opts.relayserver)
    conf.nbmessage = int(opts.nbsend)
    conf.nbmicro = float(opts.nbmicro)
    conf.noprocess = bool(opts.noprocess)
    if not opts.deamon :
        doTask(opts, conf)
    else:
        createDaemon(opts, conf)
