# Multipass user-data generator for CTE

This project provides files to aid in generating a `user-data.yml` file for multipass that can initialize a new VM with a user account for the current user.

This project consists of three core components:

- The `cte-multipass.py` python script
- The `main.yaml` variables file
- The `cte-user-data.yaml.j2` jinja2 template file

The python script will read in the template and the variables, verify files, read in the current users account data and then generate a `user-data.yaml` file for use when running multipass to launch a new VM.

## Prerequisites

You'll need at least one ssh key to use with the project.  Preferably, you should have an RSA key and a ECDSA key.  You can create those with the following two commands.

```bash
ssh-keygen -t rsa -b 2048
ssh-keygen -t ecdsa -b 521
```

## Installation
To install the project, just clone the project to a local directory, then change the mode of the script to an executable file and run it.

For example, from a Linux terminal:

```bash
$ git clone https://github.com/chuck650/cte-multipass.git
$ cd cte-multipass
multipass$ ./cte-multipass.py
```

This will generate the user-data.yaml file for multipass.  Then to launch a new VM using this cloud-init file:

```bash
$ multipass launch -n cte -c 2 -d 40G -m 16G --cloud-init user-data.yaml Eoan
```

Once the VM instance is running, you can retrieve the IPv4 address like this:

```bash
$ multipass info cte | awk '$1=="IPv4:" {print $2}'
```

Then add a section for the instance in your `.ssh/config` file that looks like this.  Remember to replace `${USER}` with your user name.

```
Host cte
    HostName 10.223.79.250
    User ${USER}
    IdentityFile ~/.ssh/id_ecdsa
    IdentitiesOnly yes
```

Now you should be able to ssh into the instance using your own login information
