# Learn-Linux

_13th September 2020_

## [Task 43] Bonus Challenge - The True Ending

The flag is said to be in the `/root/root.txt` file but we as the user (shiba2) don't have the permissions to open it. Looking for all the files of (shiba2) using `find / -user <insert-username-here> -type f 2>>/dev/null`, we come across a file called `/var/log/test1234` which contains the credentials for a user called (nootnoot). We log in as this user using the `su` command and list the permissions using `sudo -l`. This tells us that the user (nootnoot) has permissions to read, write and execute all files. We can then open `/root/root.txt` to find the root flag.
