#!/usr/bin/env python2.7

import sys
import getopt
import argparse
import re
from os.path import expanduser

home = expanduser("~")
host_re = re.compile(r"host\s+(\S+)", re.IGNORECASE)
hostname_re = re.compile(r"hostname\s+(\S+)", re.IGNORECASE)

hostname_by_host = {}

SAFETY_THRESHOLD = 6

parser = argparse.ArgumentParser(
    description="Tool to automatically open several ssh connections in iTerm2 by querying ~/.ssh/config")
parser.add_argument("-r", "--run", dest="should_actually_run", action="store_true", default=False, 
    help="Must pass this to actually run, otherwise will just list matching hosts")
parser.add_argument("pattern", help="A regular expression used to select hosts by name")

def load_hosts():
    with open(home + "/.ssh/config") as f:
        current_host = None
        for line in f.readlines():
            result = host_re.search(line);
            if result:
                current_host = result.group(1)
            elif current_host is not None:
                result = hostname_re.search(line)
                if result:
                    hostname_by_host[current_host] = result.group(1)
                    current_host = None


def do_safety_check(hosts_count):
    if hosts_count > SAFETY_THRESHOLD:
        while True:
            sys.stdout.write("Will open %d hosts. Are you sure? [y/N] " % hosts_count)
            choice = raw_input().strip().lower()
            if choice in ["y", "n", ""]:
                return choice == "y"
    return True


def main():
    arguments = parser.parse_args()
    pat = re.compile(arguments.pattern, re.IGNORECASE)
    load_hosts()

    # get filtered list of hosts, each a tuple (name, address)
    selected_hosts = [(name, address) for (name, address) in hostname_by_host.items() if pat.search(name)]
    if do_safety_check(len(selected_hosts)):
        for (name, address) in sorted(selected_hosts, key=lambda tuple: tuple[0]):  # sort by host name
            print("%s: %s" % (name, address))

main()
