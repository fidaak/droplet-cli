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

def create_droplet(api_token, droplet_name, region, size, image, ssh_keys):
    manager = digitalocean.Manager(token=api_token)
    ssh_key_ids = [key.id for key in manager.get_all_sshkeys() if key.name in ssh_keys]

    droplet = digitalocean.Droplet(
        token=api_token,
        name=droplet_name,
        region=region,
        size_slug=size,
        image=image,
        ssh_keys=ssh_key_ids,
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

def setup_ssh_keys(ssh_key_paths):
    ssh_keys = []
    for key_path in ssh_key_paths:
        if os.path.isfile(key_path):
            with open(key_path, 'r') as key_file:
                ssh_keys.append(key_file.read().strip())
        else:
            print(f"SSH key file not found: {key_path}")
    return ssh_keys

def configure_port_tunneling(client, ports):
    for port in ports:
        print(f"Setting up port forwarding for port {port}")
        # Add commands for port forwarding setup if needed
