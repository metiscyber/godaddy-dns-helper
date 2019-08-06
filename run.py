#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import dns
import argparse
from termcolor import cprint


def main():
    options = dns.get_arguments()

    dns.config()

    if options.create is '' and options.delete is '' and options.update is '' and options.reset is ''and options.list is '':
        cprint('Not enough arguments. Requires [--create, --update, --delete, --reset, --list]', 'yellow')
        exit()

    if options.create is not '':
        if options.host is '':
            cprint('Host is required', 'red')
            exit()

        if options.ipaddress is '':
            cprint('IP Address is required', 'red')
            exit()

        record = options.record
        host = options.host
        ipaddress = options.ipaddress
        dns.create(record, host, ipaddress)

    if options.delete is not '':
        if options.host is '':
            cprint('Host is required', 'yellow')
            exit()

        host = options.host
        dns.delete(host)

    if options.update is None:
        if options.host is '' or options.ipaddress is '':
            cprint('Host and ipaddress required', 'yellow')
            exit()

        record = options.record
        host = options.host
        ipaddress = options.ipaddress
        dns.update(host, ipaddress, record)

    if options.reset is not '':
        os.remove('config.json')
        dns.config()

    if options.list is None:
        domains = dns.get_domains()
        for i in domains:
            try:
                items = dns.get_domain_items(i)
                cprint(i, 'green')
                for json_dict in items:
                    name = ''
                    data = ''
                    base = False
                    for key, value in json_dict.iteritems():
                        #print("key: {key} | value: {value}".format(key=key, value=value))
                        if base == False:
                            if key == 'name':
                                name = value
                            #cprint(value, 'green')
                            if key == 'data':
                                data = value
                    cprint('%-35s %s' % (name, data), 'green')
                    #cprint("[{name} \t => \t {data}]".format(name = name, data = data), 'green')
            except:
                pass


if __name__ == "__main__":
    main()
