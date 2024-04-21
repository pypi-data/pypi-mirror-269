import os
from os.path import expanduser

# create paths
user_ssh_config = expanduser("~/.ssh/config")
easy_ec2_ssh_config = expanduser("~/.easy_ec2/ssh/config")
include_line = f'Include {easy_ec2_ssh_config}'

# create easy_ec2 directory at ~/.easy_ec2 if does not exist
if not os.path.exists(expanduser("~/.easy_ec2")):
    os.makedirs(expanduser("~/.easy_ec2"))

# create easy_ec2/ssh subdirectory at ~/.easy_ec2/ssh if does not exist
if not os.path.exists(expanduser("~/.easy_ec2/ssh")):
    os.makedirs(expanduser("~/.easy_ec2/ssh"))

# create config file in ~/.easy_ec2 if does not exist
if not os.path.exists(expanduser("~/.easy_ec2/ssh/config")):
    open(expanduser("~/.easy_ec2/ssh/config"), 'a').close()

# if include_line not in user_ssh_config then add at top of file
if include_line not in open(user_ssh_config).read():
    with open(user_ssh_config, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(include_line.rstrip('\r\n') + '\n' + content)
