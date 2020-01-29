#!/usr/bin/env python2.7

import sys
import getopt
import argparse
import re
import subprocess
from os.path import expanduser

home = expanduser("~")
host_re = re.compile(r"host\s+(\S+)", re.IGNORECASE)
hostname_re = re.compile(r"hostname\s+(\S+)", re.IGNORECASE)

hostname_by_host = {}

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


def check_if_iterm_version_is_supported():
    osa = subprocess.Popen(['osascript', '-'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)

    version_script = 'set iterm_version to (get version of application "iTerm")'
    version = osa.communicate(version_script)[0].strip()

    match = re.search(r"^(\d+)\.(\d+)", version)
    if match:
        major = int(match.group(1))
        minor = int(match.group(2))
        return (major > 2) or (major == 2 and minor > 9)  # support only if greater than 2.9
    return False


def prompt_for_confirmation(hosts_count):
    print("\nNumber of panes to open: %d" % hosts_count)
    sys.stdout.write("Press 'y' to continue or anything else to abort: ")
    choice = raw_input().strip().lower()
    return choice == "y"


def prepare_and_run_applescript(selected_hosts):
    osa = subprocess.Popen(['osascript', '-'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)

    script_lines = """
        tell application "iTerm"
            activate
            tell current window
                create tab with default profile
            end tell

            set pane_1 to (current session of current window)

            tell pane_1
                write text "ssh {host}"
                set name to "this is me testing"
            end tell

        end tell
        """.format(host=selected_hosts[0])
    script = script_lines  # "\n".join(script_lines)
    output = osa.communicate(script)[0]
    print(output)


def main():
    if not check_if_iterm_version_is_supported():
        print("iTerm2 version not supported or iTerm2 is not installed")
        exit(1)

    arguments = parser.parse_args()
    pat = re.compile(arguments.pattern, re.IGNORECASE)
    load_hosts()

    # get filtered list of hosts, each a tuple (name, address)
    selected_hosts = [(name, address) for (name, address) in hostname_by_host.items() if pat.search(name)]
    print("Will open the following terminal panes:\n")
    for (name, address) in sorted(selected_hosts, key=lambda tuple: tuple[0]):  # sort by host name
        print("- %s (%s)" % (name, address))
    
    if prompt_for_confirmation(len(selected_hosts)):
        prepare_and_run_applescript([name for (name, address) in selected_hosts])


main()
