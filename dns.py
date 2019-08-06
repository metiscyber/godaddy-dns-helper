#!/usr/bin/python
# -*- coding: UTF-8 -*-


import os
import sys
import json
import argparse
from termcolor import cprint
from godaddypy import Client, Account


def get_arguments():
    parser = argparse.ArgumentParser(description="This is a Metis DNS script")
    parser.add_argument('--create', nargs='?', action="store", default='')
    parser.add_argument('--delete', nargs='?', action="store", default='')
    parser.add_argument('--update', nargs='?', action="store", default='')
    parser.add_argument('--reset', nargs='?', action="store", default='')
    parser.add_argument('--list', nargs='?', action="store", default='')
    parser.add_argument('-record', action="store", default="A")
    parser.add_argument('-host', action="store", default="")
    parser.add_argument('-ipaddress', action="store", default="")
    parser.add_argument('-v', action="version", version="%(prog)s " + get_version())

    return parser.parse_args()


def get_version():
    return '1.3'


def get_client():
    account = Account(get_json('config.json')['api_key'], get_json('config.json')['api_secret'])
    return Client(account)


def get_domains():
    client = get_client()
    domains = client.get_domains()
    return domains


def get_domain_items(domain):
    client = get_client()
    domain_items = client.get_records(domain)
    for i in domain_items:
        if not len(domain_items):
            domain_items.remove(i)
    return domain_items


def get_records(domain, record_type='A'):
    client = get_client()
    records = client.get_records(domain, record_type)
    return records


def delete(host=''):
    client = get_client()
    domains = client.get_domains()
    host = host.split('.')
    host = host[::-1]
    base = host[1]+'.'+host[0]
    subs = [e for e in host if e not in (host[0], host[1])][::-1]
    subs = '.'.join(subs)

    if base in domains:

        records = get_records(base)

        for json_dict in records:
            for key, value in json_dict.iteritems():
                if key == 'name':
                    if value == subs:

                        confirm = sinput("Are you sure you want to delete this record? [Yes/No]: ")
                        if confirm.capitalize() == 'Yes' or confirm.capitalize() == 'Y':
                            try:
                                client.delete_records(base, name=subs)
                                cprint('Record deleted successfully!', 'green')
                            except:
                                cprint('Unable to delete record', 'yellow')
                        else:
                            cprint('Record does not exist...', 'yellow')


def create(record='A', host='', ipaddress=''):
    client = get_client()
    domains = client.get_domains()

    host = host.split('.')
    host = host[::-1]
    base = host[1]+'.'+host[0]
    subs = [e for e in host if e not in (host[0], host[1])][::-1]
    subs = '.'.join(subs)

    if base in domains:
        new_record = "\nDomain: "+base+"\nSubdomain: "+ subs+"\nRecord Type: "+record+"\nIP Address: "+ipaddress+"\n"
        cprint(new_record, 'yellow')
        records = get_records(base)

        for json_dict in records:
            for key, value in json_dict.iteritems():
                if key == 'name':
                    if value == subs:
                        cprint('Record already exists...', 'yellow')
                        exit()

        confirm = sinput("Does this look correct? [Yes/No]: ")
        if confirm.capitalize() == 'Yes' or confirm.capitalize() == 'Y':
            try:
                client.add_record(base, {'data': ipaddress, 'name': subs, 'ttl':3600, 'type':record})
                cprint('Record added successfully!', 'green')
            except:
                cprint('Unable to add record...', 'yellow')


def update(host='', ipaddress='', record='A'):
    client = get_client()
    domains = client.get_domains()

    host = host.split('.')
    host = host[::-1]
    base = host[1]+'.'+host[0]
    subs = [e for e in host if e not in (host[0], host[1])][::-1]
    subs = '.'.join(subs)

    if base in domains:
        new_record = "\nDomain: "+base+"\nSubdomain: "+ subs+"\nRecord Type: "+record+"\nIP Address: "+ipaddress+"\n"
        cprint(new_record, 'yellow')
        records = get_records(base)

        for json_dict in records:
            for key, value in json_dict.iteritems():
                if key == 'name':
                    if value == subs:

                        confirm = sinput("Does this look correct? [Yes/No]: ")
                        if confirm.capitalize() == 'Yes' or confirm.capitalize() == 'Y':
                            try:
                                client.update_record_ip(ipaddress, base, subs, record)
                                cprint('Record updated successfully!', 'green')
                            except:
                                cprint('Unable to update record...', 'yellow')


def is_windows():
    if sys.platform == "win32":
        return True


def sinput(message):
    if is_windows():
        return input(message)
    else:
        return raw_input(message)


def file_exists(filename):
    if os.path.isfile(filename):
        return True


def filepath_exists(path):
    if os.path.exists(path):
        return True


def get_json(file_path):
    if file_exists(file_path):
        with open(file_path, 'r') as f:
            data = f.read()
            return json.loads(data)


def config():
    if not file_exists('config.json'):
        cprint('Config wizard')
        api_secret = sinput('Enter your Godaddy API secret: ')
        api_key = sinput('Enter your Godaddy API key: ')

        api = {
                'api_secret': api_secret,
                'api_key': api_key
        }

        s = json.dumps(api, indent=4, sort_keys=True)

        with open('config.json', 'w') as f:
            f.write(s)
            f.close()
