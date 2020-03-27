# Multipass user-data generator for CTE

This project provides files to aid in generating a `user-data.yml` file for multipass that can initialize a new VM with a user account for the current user.

This project consists of three core components:

- The `cte-multipass.py` python script
- The `main.yaml` variables file
- The `cte-user-data.yaml.j2` jinja2 template file

The python script will read in the template and the variables, verify files, read in the current users account data and then generate a `user-data.yaml` file for use when running multipass to launch a new VM.

## Prerequisites

To use this project, you'll need to install git on you system.  For Ubuntu Linux, just install it from the repository.

```bash
$ sudo apt install git
```

You'll need at least one ssh key to use with the project.  Preferably, you should have an RSA key and a ECDSA key.  You can create those with the following two commands. Just hit enter when prompted to use the default file names, and no password if you do not want a password on your keys.

```bash
ssh-keygen -t rsa -b 2048
ssh-keygen -t ecdsa -b 521
```
Verify the files exist in the right locations.

```bash
$ ls -l ~/.ssh/id_{r,ecd}sa{,.pub}
-rw------- 1 chuck chuck  505 Feb 10 06:55 /home/chuck/.ssh/id_ecdsa
-rw-r--r-- 1 chuck chuck  172 Feb 10 06:55 /home/chuck/.ssh/id_ecdsa.pub
-rw------- 1 chuck chuck 1679 Aug 30  2018 /home/chuck/.ssh/id_rsa
-rw-r--r-- 1 chuck chuck  408 Aug 30  2018 /home/chuck/.ssh/id_rsa.pub
```

You'll also need a working Python3 environment.

```bash
$ sudo apt install python3 python3-pip python3-jinja2 python3-yaml
$ sudo pip3 install --ignore-installed PyYAML
```

## Installation
To install the project, just clone the project to a local directory, then run it.

For example, from a Linux terminal:

```bash
$ git clone https://github.com/chuck650/cte-multipass.git
$ cd cte-multipass
multipass$ python3 cte-multipass.py
```

This will generate the user-data.yaml file for multipass.  You can view this file with a text editor.

```bash
$ view user-data.yaml
```

To launch a new VM using this cloud-init file:

```bash
$ multipass launch -n cte -c 2 -d 40G -m 16G --cloud-init user-data.yaml eoan
```

Once the VM instance is running, you can retrieve the IPv4 address like this:

```bash
$ multipass info cte | awk '$1=="IPv4:" {print $2}'
```

To view the status of the running instance, use the `multipass info` command.  Here you see the effect of running this on an Ubuntu Linux host with 32 GB of Ram where the Guest VM is allocated 40GB of storage and 16GB of memory.  Notice the utilization of disk and memory is low for a freshly installed VM.

```bash
$ multipass info cte
Name:           cte
State:          Running
IPv4:           10.223.79.250
Release:        Ubuntu 19.10
Image hash:     e0aa0e03fe65 (Ubuntu 19.10)
Load:           0.62 0.16 0.05
Disk usage:     1.9G out of 38.6G
Memory usage:   211.8M out of 15.6G
```

Then add a section for the instance in your host's `~/.ssh/config` file that looks like this.  Remember to replace `${USER}` with your user name and `${IPv$_Address}` with your Multipass VM's IPv4 address.

```
Host cte
    HostName ${IPv4_Address}
    User ${USER}
    IdentityFile ~/.ssh/id_ecdsa
    IdentitiesOnly yes
```

Now you should be able to ssh from the host into the instance using your own login information.

```bash
$ ssh cte
```
