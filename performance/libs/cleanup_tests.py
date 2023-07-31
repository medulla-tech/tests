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
import os
import subprocess
import json
import base64
import requests
from mmc.plugins.glpi.config import GlpiConfig

config = GlpiConfig("glpi")

def delete_machine_from_glpi(machine_ids):
    authtoken =  base64.b64encode(config.webservices['glpi_username']+":"+config.webservices['glpi_password'])

    headers = {
        'content-type': 'application/json',
        'Authorization': f"Basic {authtoken}",
    }
    url = config.webservices['glpi_base_url'] + "initSession"
    print("Create session REST")
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        sessionwebservice =  str(json.loads(r.text)['session_token'])
        print(f"session {sessionwebservice}")
        for id in machine_ids:
            machine_id = id.strip('\n')
            url = config.webservices['glpi_base_url'] + "Computer/" + str(machine_id)
            headers = {'content-type': 'application/json',
                        'Session-Token': sessionwebservice
            }
            parameters = {'force_purge': '1'}
            r = requests.delete(url, headers=headers, params=parameters)
            if r.status_code == 200:
                print(f"Machine {str(machine_id)} deleted")

        url = config.webservices['glpi_base_url'] + "killSession"
        r = requests.get(url, headers=headers)
    if r.status_code == 200:
        print(f"Kill session REST: {sessionwebservice}")



command = 'echo "DROP TRIGGER IF EXISTS machines_before_insert;" | mysql xmppmaster'
print command
os.system(command)
command = 'echo "DROP TRIGGER IF EXISTS machines_after_insert;" | mysql xmppmaster'
print command
os.system(command)
command = 'echo "DROP TABLE IF EXISTS registermachines_sendbefore;" | mysql xmppmaster'
print command
os.system(command)
command = 'echo "DROP TABLE IF EXISTS registermachines_sendafter;" | mysql xmppmaster'
print command
os.system(command)
command = 'echo "DELETE FROM machines WHERE jid LIKE \'%SIVEOTEST-%\';" | mysql xmppmaster'
print command
os.system(command)

command = 'echo "DROP TRIGGER IF EXISTS glpi_computers_before_insert;" | mysql glpi'
print command
os.system(command)
command = 'echo "DROP TRIGGER IF EXISTS glpi_computers_after_insert;" | mysql glpi'
print command
os.system(command)
command = 'echo "DROP TABLE IF EXISTS inventorymachines_sendbefore;" | mysql glpi'
print command
os.system(command)
command = 'echo "DROP TABLE IF EXISTS inventorymachines_sendafter;" | mysql glpi'
print command
os.system(command)
command = 'echo "SELECT id FROM glpi_computers WHERE name LIKE \'%SIVEOTEST-%\';" | mysql -s glpi'
print command
p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
machines = p.stdout.readlines()
delete_machine_from_glpi(machines)
