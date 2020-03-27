#! /usr/bin/python3

from jinja2 import Environment, FileSystemLoader
import sys, yaml, os, pwd, pprint, crypt

# Check if displaying verbose information
if "-v" in sys.argv:
    verbose = True
else:
    verbose = False

# Get the absolute path to this executable file
pathname = os.path.dirname(sys.argv[0])
abspath = os.path.abspath(pathname)

# load the current users data from the OS
user = pwd.getpwuid(os.getuid())
username = user.pw_name
gecos = user.pw_gecos.split(',')[0]
home = user.pw_dir
key_files = []
ssh_keys = []


# Config the environment to load templates from the ./templates folder
env = Environment(
    loader=FileSystemLoader(abspath + '/templates'),
)

# Load the jinja2 template from the template file
template = env.get_template('cte-user-data.yaml.j2')

# load the variable data from the vars file
with open(abspath + '/vars/main.yaml') as file:
    data =  yaml.load(file, Loader=yaml.FullLoader)

# Set the passwd hash using sha-512 algorithm
if "password" in data:
    pword = data['password']
else:
    pword = "password"
    print("\033[0;31mUsing password: " + pword + "\033[0m\n")
passwd = crypt.crypt(pword, crypt.mksalt(crypt.METHOD_SHA512))

# Expand the aliased path to an absolute path
key_files.append(os.path.expanduser(data['rsa_pub_key_path']))
key_files.append(os.path.expanduser(data['ecdsa_pub_key_path']))

# if the key exists, add it to the list of ssh keys
for file in key_files:
    if os.path.isfile(file):
        key = open(file, 'r').read()
        ssh_keys.append(key)

if verbose:
    print("Executable Path:" + abspath, file=sys.stderr)
    print(passwd, file=sys.stderr)
    for key in ssh_keys:
        print("SSH Public Key: " + key, file=sys.stderr)
    print("Input Variables:", file=sys.stderr)
    pprint.pprint(data, stream=sys.stderr,indent=4)

user_data = template.render(data,
    username=username,
    password=passwd,
    ssh_keys=ssh_keys,
    gecos=gecos)

print("\n\033[0;36m" + user_data + "\033[0m")

print("\n\033[0;35mSaved to user-data.yaml\033[0m\n")

print("Multipass usage example:")
print("  multipass launch -n cte -c 2 -d 40G -m 16G --cloud-init user-data.yaml eoan")

f = open("user-data.yaml","w")
f.write(user_data + "\n")
f.close()
