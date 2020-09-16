# Lian_Yu

_14th September 2020_

## Host enumeration

The initial Nmap scan reports the following.

```
21/tcp  open  ftp     vsftpd 3.0.2
22/tcp  open  ssh     OpenSSH 6.7p1 Debian 5+deb8u8 (protocol 2.0)
80/tcp  open  http    Apache httpd
111/tcp open  rpcbind 2-4 (RPC #100000)
```

### Analysis

The webpage running on port 80 does not seem to provide any extra clues. We can proceed to web enumeration.

## Web enumeration

A web directory called `island` is found with a scan using `gobuster`.

```
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.193.213/
[+] Threads:        10
[+] Wordlist:       ../../Wordlists/directory-list-medium.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Timeout:        10s
===============================================================
2020/09/15 11:15:23 Starting gobuster
===============================================================
/island (Status: 301)
Progress: 18180 / 220560 (8.24%)^C
[!] Keyboard interrupt detected, terminating.
===============================================================
2020/09/15 11:20:32 Finished
===============================================================
```

Navigating to this page shows us this piece of code.

```html
<p>You should find a way to <b> Lian_Yu</b> as we are planed. The Code Word is: </p><h2 style="color:white"> vigilante</style></h2>
```

Running `gobuster` on the subdirectory gives us a 4 digit number which is the first answer.
The source hints that there could be a file with a `.ticket` extension on the server. We can run gobuster again on the subdirectory and check for this extension. As a result we do find a .ticket file.

### Analysis

The obtained string is base58 encoded. We can decode it to obtain an FTP login.

## FTP

There are 3 pictures and a file called `.other_user` on the server. We can download the same with the following example command.

```
get Queen's_Gambit.png
```

### Analysis

The pictures seem to be broken. On examining the picture using `xxd`, we can see that the PNG header is missing. We replace the corrupted bits with the correct PNG header i.e, `89 50 4E 47 0D 0A` at the top using <https://hexed.it>.
The picture now discloses a password.

## Steganography

Since the .jpg file shows no information, we can use the previously obtained password and try tp extract any hidden information using `steghide`.

### Analysis

We find a file called `ss.zip` with a file called `password.txt`. This file seems to contain a password. Trying to login with the user (slade) and the obtained password gives us a successful connection. The current directory contains the user flag.

## Privilege escalation

Checking user privileges with `sudo -l` reveals the following.

```
User slade may run the following commands on LianYu:
    (root) PASSWD: /usr/bin/pkexec
```

This means the current user (slade) can execute `usr/bin/pkexec` without a password as root. On checking [GTFOBins](https://gtfobins.github.io/gtfobins/pkexec/) for the exploit, we find that upon executing the following, we can become (root).

```sh
sudo pkexec /bin/sh
```

### Analysis

We find a file called `root.txt` in the current directory with the root flag.
