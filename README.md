
# iTermoxyl

iTermoxyl is command line tool to automatically open multiple ssh connections in [iTerm2](https://iterm2.com/) by directly querying `~/.ssh/config` using regular expressions.

It is a slightly different medicine for a slightly different problem. iTermoxyl was inspired by [itermocil](https://github.com/TomAnthony/itermocil), which was inspired by [teamocil](https://github.com/remiprev/teamocil).

iTermoxyl is designed to be simple to use, with minimal interaction needed to get it running.

Features:

- directly learns about existing hosts by reading `~/.ssh/config`
- doesn't require any configuration files (tools like `itermocil` and `i2cssh` require you to manually create YAML descriptions of your environments)
- regexp support: no need to type in the name of each machine you want to connect to
- supports [ssh config Include directives](https://man.openbsd.org/ssh_config#Include)
- supports loose searches (see below)

## How to install

`cd` to the destination directory and:

    curl -O https://raw.githubusercontent.com/luciopaiva/itermoxyl/master/itermoxyl
    chmod u+x itermoxyl

You need to have iTerm2 installed (obviously), but nothing else. The script is written in Python 2.7 and your macOS already comes bundled with it.

## How to use

Considering the following sample `~/.ssh/config` file:

```
Host foo-1
    HostName 10.0.0.1
Host foo-2
    HostName 10.0.0.2
Host foo-3
    HostName 10.0.0.3
Host foo-4
    HostName 10.0.0.4

Host bar-1
    HostName 10.0.1.1
Host bar-2
    HostName 10.0.1.2

Host server-1-a
    HostName 192.168.0.1
Host server-1-b
    HostName 192.168.0.2
Host server-2-a
    HostName 192.168.1.1
Host server-2-b
    HostName 192.168.1.2
```

You could run the following command:

    itermoxyl foo

Which will open a new tab in the current window and then spawn 4 panes in it. Each pane will automatically open a connection to one of the hosts matching `foo`.

You could also:

    itermoxyl '2$'

Which will open a new tab, but this time with 2 panes, one for `foo-2` and another for `bar-2`. It won't match neither `server-2-a` nor `server-2-b`.

Another possibility:

    itermoxyl 'server.*?a'

Will match `server-1-a` and `server-2-a`. Even simpler, iTermoxyl automatically adds the `.*?` part if you provide the terms separated by spaces, like so:

    itermoxyl server a

This has the exact same effect as the regexp construction above.

The script will show you all hosts matching your query and ask for confirmation before connecting to them.

