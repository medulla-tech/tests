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
import sys
from optparse import OptionParser
import datetime
import os


def parse_sender_log(sender_logfile):
    parsed_sender_log = {}
    with open(sender_logfile) as sender_log:
        for line in sender_log:
            (timestamp, message_number) = line.split(' : ')
            parsed_sender_log[int(message_number)] = timestamp
    return parsed_sender_log


def parse_recipient_log(recipient_logfile):
    parsed_recipient_log = {}
    with open(recipient_logfile) as recipient_log:
        for line in recipient_log:
            (timestamp, message_number) = line.split(' : ')
            parsed_recipient_log[int(message_number)] = timestamp
    return parsed_recipient_log

def prepare_logs(database, table, logfile):
    command = 'echo "select * from ' + table + ' INTO OUTFILE \'' + logfile + '\' FIELDS TERMINATED BY \'.999999 : \'" | mysql ' + database
    os.system(command)
    command = 'mv /tmp/systemd-private-*-mariadb.service*/' + logfile + ' /tmp'
    os.system(command)
    command = 'sed -i \'s.\\\\..g\' ' + logfile
    os.system(command)

def calculate_time_spent(sender_dict, recipient_dict):
    time_spent = {}
    messages_lost = []
    for message_number, timestamp in sender_dict.iteritems():
        start = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
        try:
            end = datetime.datetime.strptime(recipient_dict[message_number], '%Y-%m-%d %H:%M:%S.%f')
            time_delta = (end - start).seconds + (end - start).microseconds/1E6
            time_spent[int(message_number)] = time_delta
        except KeyError:
            messages_lost.append(message_number)

    print('Minimum time spent: %s seconds' % min(time_spent.values()))
    print('Maximum time spent: %s seconds' % max(time_spent.values()))
    mean_time = sum(time_spent.values()) / len(time_spent)
    print('Mean time spent: %s seconds' % mean_time)
    start = datetime.datetime.strptime(parsed_sender_log[1], '%Y-%m-%d %H:%M:%S.%f')
    end = datetime.datetime.strptime(parsed_recipient_log[max(parsed_recipient_log)], '%Y-%m-%d %H:%M:%S.%f')
    print('Total processing time: %s' % (end - start))
    print('Messages lost: %s' % messages_lost)


if __name__ == '__main__':

    optp = OptionParser()
    optp.add_option("-s",
                    "--sender-logfile",
                    dest = "sender_logfile",
                    default = "/tmp/testcharge_send.txt",
                    help = "Sender logfile")
    optp.add_option("-r",
                    "--recipient-logfile",
                    dest = "recipient_logfile",
                    default = "/tmp/testcharge_master_recv.txt",
                    help = "Recipient logfile")

    optp.add_option("-a",
                    "--action",
                    dest="action",
                    help="Action done. eg. register")
    opts, args = optp.parse_args()

    print('Sender log file: %s' % opts.sender_logfile)
    print('Recipient log file: %s' % opts.recipient_logfile)

    parsed_sender_log = parse_sender_log(opts.sender_logfile)
    if opts.action == "register":
        print('MMC processing')
        prepare_logs('xmppmaster', 'registermachines_sendbefore', opts.recipient_logfile)
        parsed_recipient_log = parse_recipient_log(opts.recipient_logfile)
        calculate_time_spent(parsed_sender_log, parsed_recipient_log)

        print('Total time')
        prepare_logs('xmppmaster', 'registermachines_sendafter', opts.recipient_logfile)
        parsed_recipient_log = parse_recipient_log(opts.recipient_logfile)
        calculate_time_spent(parsed_sender_log, parsed_recipient_log)

    elif opts.action == "inventory":
        print('MMC processing')
        prepare_logs('glpi', 'inventorymachines_sendbefore', opts.recipient_logfile)
        parsed_recipient_log = parse_recipient_log(opts.recipient_logfile)
        calculate_time_spent(parsed_sender_log, parsed_recipient_log)

        print('Total time')
        prepare_logs('glpi', 'inventorymachines_sendafter', opts.recipient_logfile)
        parsed_recipient_log = parse_recipient_log(opts.recipient_logfile)
        calculate_time_spent(parsed_sender_log, parsed_recipient_log)

    else:
        parsed_recipient_log = parse_recipient_log(opts.recipient_logfile)
        calculate_time_spent(parsed_sender_log, parsed_recipient_log)
