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
from sleekxmpp.xmlstream.stanzabase import JID
import json
import hashlib
import datetime
from optparse import OptionParser
import base64
import copy
import traceback
from datetime import datetime
import time
import uuid
import zlib


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


class configuration:
    def __init__(self):
        self.Password = "dede"
        self.Port = 5222
        self.Server = "192.168.56.2"
        if os.path.exists("/etc/mmc/plugins/xmppmaster.ini"):
            Config = ConfigParser.ConfigParser()
            Config.read("/etc/mmc/plugins/xmppmaster.ini")
            if os.path.exists("/etc/mmc/plugins/xmppmaster.ini.local"):
                Config.read("/etc/mmc/plugins/xmppmaster.ini.local")

            if  Config.has_option("connection", "password"):
                self.Password=Config.get('connection', 'password')


            if  Config.has_option("connection", "port"):
                self.Port = Config.get('connection', 'port')
            else :
                self.Port = 5222

            if  Config.has_option("connection", "Server"):
                self.Server=Config.get('connection', 'Server')

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


def generate_json_register(mac_shortened, hostname):
    mac = ':'.join([mac_shortened.upper()[i : i + 2] for i in range(0, len(mac_shortened), 2)])

    if not os.path.isfile('template_registration_b64decoded.json'):
        sys.exit('template_registration_b64decoded.json does not exist')
    elif not os.path.isfile('template_registration.json'):
        sys.exit('template_registration.json does not exist')
    else:
        regb64dec_file = open("template_registration_b64decoded.json","r")
        b64dec_data = regb64dec_file.read().replace('@@@MACADDRESS@@@', mac).replace('@@@HOSTNAME@@@', hostname).replace('@@@MACADDRESS_SHORT@@@', mac_shortened)
        b64enc_data = base64.b64encode(b64dec_data)
        reg_file = open("template_registration.json","r")
        registration_data = reg_file.read().replace('@@@MACADDRESS@@@', mac).replace('@@@HOSTNAME@@@', hostname).replace('@@@MACADDRESS_SHORT@@@', mac_shortened).replace('@@@B64ENCODED_DATAMACHINE@@@', b64enc_data)

    machine_info = json.loads(registration_data)
    machine_info['action'] = 'infomachine'

    return json.dumps(machine_info)


def generate_json_inventory(mac_shortened, hostname):
    mac = ':'.join([mac_shortened.upper()[i : i + 2] for i in range(0, len(mac_shortened), 2)])

    if not os.path.isfile('template_inventory.xml'):
        sys.exit('template_inventory.xml does not exist')
    else:
        inv_file = open("template_inventory.xml","r")
        inventory_data = inv_file.read().replace('@@@MACADDRESS@@@', mac).replace('@@@HOSTNAME@@@', hostname).replace('@@@SERIAL@@@', getRandomName(15)).replace('@@@UUID@@@', str(uuid.uuid4()))

    inventory_info = {}
    inventory_info['action'] = 'resultinventory'
    inventory_info['sessionid'] = getRandomName(6, "inventory")
    inventory_info['base64'] = False
    inventory_info['data'] = {}
    inventory_info['data']['inventory'] = base64.b64encode(zlib.compress(inventory_data, 9))
    inventory_info['ret'] = 0

    return json.dumps(inventory_info)


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

        if conf.Msgjson != "":
            self.msg = conf.Msgjson

        elif conf.tailleoctet != 0:
                self.text = getRandomName(conf.tailleoctet, "text")
                self.msg = {
                            "action": "testcharge",
                            "sessionid" : getRandomName(6, "testcharge"),
                            "ret" : 0,
                            "base64" : False,
                            'data' : { "nb" : 1,
                                    "text" : self.text}
                }
        else:
            self.text = getRandomName(12000, "text")
            self.msg ={
                        "action": "testcharge",
                        "sessionid" : getRandomName(6, "testcharge"),
                        "ret" : 0,
                        "base64" : False,
                        'data' : { "nb" : 1,
                                "text" : base64.b64encode(self.text)}
            }

    def start(self, event):
        self.get_roster()
        self.send_presence()
        print self.boundjid
        for i in range(conf.nbmessage):
            if i == 0:
                file_put_contents(self.config.fileout, "%s : %s\n"%(str(datetime.now()),str(i) ) )
            else:
                file_put_contents_w_a(self.config.fileout,
                                      "%s : %s\n"%(str(datetime.now()),str(i) ),
                                      "a")

            if conf.action == "register":
                mac_shortened = str(uuid.uuid4())[-12:]
                hostname = 'SIVEOTEST-' + str(i + conf.offset)
                msg_json = generate_json_register(mac_shortened, hostname)
                self.msg = json.loads(msg_json)
            elif conf.action == "inventory":
                mac_shortened = str(uuid.uuid4())[-12:]
                hostname = 'SIVEOTEST-' + str(i + conf.offset)
                msg_json = generate_json_inventory(mac_shortened, hostname)
                self.msg = json.loads(msg_json)
            elif conf.Msgjson == "":
                print "send message %s"%i
                self.msg['data']['nb'] = i
                self.msg['data']['user'] = self.config.user
            else:
                self.msg = self.msg.replace('\n',"")
                self.msg = json.loads(self.msg)
            self.send_message_to_master(self.msg)
            if self.config.nbmicro != 0.0:
                time.sleep(self.config.nbmicro)

        self.disconnect()
        sys.exit(0)


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

    def send_message_to_master(self , msg):
        self.send_message(  mbody = json.dumps(msg),
                            mto = self.config.master,
                            mtype ='chat')

    def message(self, msg):
        #save log message
        print "recois message"
        # creation du message



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
    #print "##############################"
    #print "##############################"
    #print conf.Server,conf.Port
    #print "##############################"
    #print "##############################"
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
        print "Agent can only run on Linux systems"


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

    optp.add_option("-n", "--nbsend",
                dest="nbsend", default="1",
                help="Number of messages to be sent")
    optp.add_option("-o", "--offset",
                dest="offset", default="0",
                help="The inventory number starts at the specified offset")

    optp.add_option("-t", "--tailleoctet",
                dest="tailleoctet", default="0",
                help="Size of message sent in bytes")

    optp.add_option("-j", "--jiddestinataire",
                dest="jiddestinataire",
                default="master@pulse/MASTER",
                help="Recipient jid. default: master@pulse")

    optp.add_option("-s", "--nbmicroseconde",
                dest="nbmicro", default="0",
                help="Number of seconds between 2 messages")

    optp.add_option("-M", "--Msgjson",
                dest="Msgjson", default="",
                help="JSON message to be sent")

    optp.add_option("-S", "--Serverip",
                dest="Server",
                action = "store" , type = "string",
                help="Server address")

    optp.add_option("-P", "--password",
                dest="Password",
                help="Password of user account")

    optp.add_option("-p", "--port",
                dest="port",
                help="Server port")

    optp.add_option("-N", "--jidname",
                dest="Jid", default="testcharge@pulse/testcharge",
                help="Sender agent Jid")

    optp.add_option("-a", "--action",
                dest="action",
                help="Action to be done. eg. register")

    opts, args = optp.parse_args()

    # Setup the command line arguments.
    conf  = configuration()
    conf.nbmessage = int(opts.nbsend)
    conf.nbmicro = float(opts.nbmicro)
    conf.offset = int(opts.offset)
    conf.master = opts.jiddestinataire
    conf.tailleoctet  = int(opts.tailleoctet)
    conf.Msgjson = opts.Msgjson
    if opts.Password  is not None :
        conf.Password = opts.Password
    if opts.Server is not None :
        conf.Server = opts.Server
    if opts.port is not None :
        conf.Port = opts.port
    conf.Jid = opts.Jid
    conf.action = opts.action

    print "Number of messages: %s"%conf.nbmessage
    print "Time between messages: %s"%conf.nbmicro
    print "Inventory offset: %s"%conf.offset
    print "Recipient: %s"%conf.master
    print "Message size: %s"%conf.tailleoctet
    print "Message JSON: %s"%conf.Msgjson
    print "Server ip: %s"%conf.Server
    print "Server port: %s"%conf.Port
    print "Agent JID: %s"%conf.Jid
    print "password %s"%conf.Password
    conf.user = JID(conf.Jid).user
    conf.fileout = os.path.join("/","tmp", "%s_send.txt"%conf.user)
    print "Output file: %s"%conf.fileout
    print "Action: %s"%conf.action

    if conf.action == "register":
        if not os.path.isfile('register_machines.sql'):
            sys.exit('register_machines.sql does not exist')
        else:
            command = 'mysql xmppmaster < register_machines.sql'
            print command
            os.system(command)
    elif conf.action == "inventory":
        if not os.path.isfile('inventory_machines.sql'):
            sys.exit('inventory_machines.sql does not exist')
        else:
            command = 'mysql glpi < inventory_machines.sql'
            print command
            os.system(command)


    if not opts.deamon :
        doTask(opts, conf)
    else:
        createDaemon(opts, conf)
