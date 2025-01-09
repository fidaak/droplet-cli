import argparse
import yaml
import subprocess
import os
import time
import digitalocean
from paramiko import SSHClient, AutoAddPolicy

def load_yaml_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def create_droplet(api_token, droplet_name, region, size, image):
    droplet = digitalocean.Droplet(
        token=api_token,
        name=droplet_name,
        region=region,
        size_slug=size,
        image=image,
        user_data=None
    )

    droplet.create()

    actions = droplet.get_actions()
    for action in actions:
        while action.status != "completed":
            time.sleep(5)
            action.load()
    
    while not droplet.ip_address:
        droplet.load()
        time.sleep(5)
    
    return droplet

def setup_ssh_keys(client, ssh_key_paths):
    """Copy SSH private keys to the droplet and set proper permissions"""
    if not ssh_key_paths:
        return
        
    # Create .ssh directory
    client.exec_command('mkdir -p ~/.ssh')
    client.exec_command('chmod 700 ~/.ssh')
    
    for key_path in ssh_key_paths:
        if not os.path.isfile(key_path):
            print(f"SSH key file not found: {key_path}")
            continue
            
        # Copy key file
        key_name = os.path.basename(key_path)
        with open(key_path, 'r') as key_file:
            key_content = key_file.read()
            
        sftp = client.open_sftp()
        remote_path = f'/root/.ssh/{key_name}'
        with sftp.file(remote_path, 'w') as remote_file:
            remote_file.write(key_content)
        sftp.close()
        
        # Set proper permissions
        client.exec_command(f'chmod 600 {remote_path}')

def configure_port_tunneling(client, ports):
    for port in ports:
        print(f"Setting up port forwarding for port {port}")
        # Add commands for port forwarding setup if needed
