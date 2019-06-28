# IoT Camera Hack | Exercise 00

## Summary

Welcome to the first steps of the IoT Camera Hack lab exercise. First, we must configure your local lab environment to ensure your success. Follow the steps described below to begin the process and if you have any questions, don't hesitate to ask. Note, you may configure the lab environment on any computer with Administrator access.

There are no learning objectives for completing this exercise and merely focuses on preparation of the lab environment.

## Instructions

### Windows Virtual Machine [Home Computer (Victim)]

This exercise requires a Windows Virtual Machine (VM) to mimic a personal home computer. If you have a Windows VM, you may skip to step 4 otherwise, proceed with the instruction set.

1. Download and install [VirtualBox](https://www.virtualbox.org/) on your lab computer

2. Download and install the [Microsoft Edge VM](https://developer.microsoft.com/en-us/microsoft-edge/tools/vms/) by selecting _MSEdge on Win 10 (x64)_ and _VirtualBox_ from the provided link. The remainder of the instruction set refers this VM as the _Windows VM_

3. Set the network configuration of the _Windows VM_ to _Bridged Adapter_ in _Virtual Box_

4. Launch _VirtualBox_ and start the _Windows VM_

5. Having a functional _Windows VM_ at this point demonstrates that we have established a target system for the exercise however, the VM doesn't contain anything valuable. Lets change that by creating a folder on the _Windows VM's Desktop_ called _Share_

6. Find your favorite picture or random text document and place the file inside the _Share_ folder.

7. _Right click_ on the _Share_ folder and click _Properties_

8. Click on the _Sharing_ tab

9. Click on the _Advanced Sharing_ button and check the _Share this folder_ checkbox

10. Set the _Permission_ for the shared folder to allow _Everyone_ with _Full Control_.

11. _Apply_ the change and click _Ok_

12. At this point of the instruction set, we have configured a targeted system with an accessible file, we now must configure another VM that we will use for launching an attack

### Kali Virtual Machine (The Attacker)

Previously, we created a targeted system for the lab environment however, we need a threat actor or an attacker in the exercise. If you have a preferred machine that runs on a *nix environment such as Mac OS X or Linux and the system has the ability to run `Python`, `nc`, and `curl`--you may skip this section of the instruction set.

1. Download and install a [Kali Linux VM](https://www.offensive-security.com/kali-linux-vm-vmware-virtualbox-image-download/)

2. Set the network configuration of the _Kali VM_ to _Bridged Adapter_ in _Virtual Box_

3. The GitHub repository provided a series of scripts for the Kali VM that the team developed for this exercise. Copy the scripts into the Kali VM by either browsing to the GitHub repository in the _Kali VM_ or by _drag and drop_ the files from your _base machine_.

### GeoVision Camera

Configuring the camera for this exercise may be a bit tricker in comparison to the other steps in this setup guide as the firmware (software) version of the camera may differ at the time of purchase. We provide the firmware (software), tools, and the manufacture guide this exercise uses for the camera to assist with the configuration. The following are items that must be verify/validate against the camera to insure the configuration matches the exercise.

1. Camera firmware version must be v3.12

2. The web interface of the camera must be reachable from both the _Kali_ and _Windows VM_. See provided manufacture guide on accessing the web interface.

**Question:** What is the IP Address of the camera? Write it down for later use: ________________________________________

### VM Credentials

|            | Username | Password  |
|-----------:|----------|-----------|
|    Kali VM |   root   |    toor   |
| Windows VM |  ieuser  | Passw0rd! |