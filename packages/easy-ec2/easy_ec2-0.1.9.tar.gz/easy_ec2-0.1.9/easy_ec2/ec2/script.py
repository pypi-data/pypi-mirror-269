
# read in startup script
def read_startup_script(startup_script_path):
    with open(startup_script_path, 'r') as file:
        startup_script = file.read()
    return startup_script


# inject aws creds into base script
def inject_aws_creds(startup_script: str,
                     aws_metadata: dict) -> str:
    # replace aws_account_id and aws_access_key_id
    startup_script = startup_script.replace('$aws_access_key_id',
                                            aws_metadata['aws_access_key_id'])
    startup_script = startup_script.replace('$aws_secret_access_key',
                                            aws_metadata['aws_secret_access_key'])
    return startup_script


# turn on ssh forwarding on remote server at startup
def add_ssh_forwarding(startup_script: str) -> str:
    ssh_forwarding_command_block = '''
### setup ssh agent forwarding on remote server ###
# make sure ssh agent is running
eval "$(ssh-agent -s)"

# if "$SSH_AUTH_SOCK" is not set, then report error
if [ -z "$SSH_AUTH_SOCK" ] ; then
    echo "ERROR: SSH_AUTH_SOCK not set"
fi

# Enable SSH agent forwarding in the SSH server configuration
sudo sed -i 's/^#AllowAgentForwarding/AllowAgentForwarding/' /etc/ssh/sshd_config

# Restart the SSH server
sudo systemctl restart sshd
    '''

    # append ssh_forwarding_command_block to startup_script with newline
    startup_script += '\n' + ssh_forwarding_command_block

    return startup_script


# add github host to startup script
def add_github_host(startup_script: str) -> str:
    github_host_command_block = '''
### add github ssh key to server ###
# Run ssh-keyscan for github.com
ssh-keyscan github.com >> /home/ubuntu/.ssh/known_hosts

# Run ssh-keyscan for any additional known hosts associated with git@github.com
known_hosts=$(ssh -T git@github.com 2>&1 | awk '/Offending/ {print $2}')
for host in $known_hosts; do
    ssh-keyscan -t rsa "$host" >> ~/.ssh/known_hosts
done
    '''

    # append github_host_command_block to startup_script with newline
    startup_script += '\n' + github_host_command_block

    return startup_script
