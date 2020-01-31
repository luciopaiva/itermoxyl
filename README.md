
# itermonkey

Tool to automatically open several ssh connections in iTerm2 by directly querying `~/.ssh/config` using a regular expression.

Considering the following `config` file:

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

    ./itermonkey.py foo

Which will open a new tab in the current window and then spawn 4 panes in it, finally `ssh`ing to each `foo` host.

You could also:

    ./itermonkey.py '2$'

Which will open a new tab, but this time with 2 panes, one for `foo-2` and the other for `bar-2`. It won't bring `server-2-a` or `server-2-b`, though.

Another possibility:

    ./itermonkey.py 'server.*?a'

Will open `server-1-a` and `server-2-a`.

## How to install

`cd` to the destination directory and:

    curl -O https://raw.githubusercontent.com/luciopaiva/itermonkey/master/itermonkey.py
    chmod u+x itermonkey.py

You need to have iTerm2 installed (obviously), but nothing else. The script is written in Python 2.7 and your macOS already comes bundled with it.

---

Inspired by [itermocil](https://github.com/TomAnthony/itermocil), which was inspired by [teamocil](https://github.com/remiprev/teamocil).
