# Brooklyn-Nine-Nine

_20th September 2020_

## Host enumeration

### Analysis

Since there is a web service running on port 80, we can try to check out the webpage at `http://<IP>/`. We see a picture and a comment in the html.

```html
<!-- Have you ever heard of steganography? -->
```

This hints at steganography being used in the picture. We also have to keep in mind that there is an FTP service running on port 21 with anonymous login.

## Web enumeration

Nothing interesting comes up with `gobuster`.

## FTP

On logging in anonymously to the FTP service, we find a file called `note_to_jake.txt`.

### Analysis

Since it is a weak password, we can try to bruteforce the SSH login for the user (jake) using `hydra` as follows.

```bash
hydra -l <username> -P <wordlist> ssh://<IP>
```

We get the following credentials.

```bash
[22][ssh] host: 10.10.202.158   login: jake   password: 987654321
```

On basic searching, we can find the user flag in the directory `/home/holt`.

## Privilege escalation

Running `sudo -l` to check the permisssion's for the current user (jake), we find that `/usr/bin/less` can be executed as root without a password.

### Analysis

Checking on [GTFOBins](https://gtfobins.github.io/gtfobins/less/), we find a way to exploit the command using the following command.

```bash
sudo less /etc/profile
!/bin/sh
```

We are now the root user and we can change directory to `/root` for the root flag.
