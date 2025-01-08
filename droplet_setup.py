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

def cli_entry():
    parser = argparse.ArgumentParser(description="DigitalOcean Droplet Setup CLI")
    parser.add_argument("--config", required=True, help="Path to YAML configuration file")
    parser.add_argument("--ssh-keys", nargs='+', help="Paths to SSH key files to add to the droplet")
    parser.add_argument("--ports", nargs='+', type=int, help="Ports to tunnel from the droplet")

    args = parser.parse_args()

    config = load_yaml_config(args.config)
    
    api_token = config['api_token']
    droplet_name = config['droplet_name']
    region = config['region']
    size = config['size']
    image = config['image']
    
    ssh_keys = setup_ssh_keys(args.ssh_keys) if args.ssh_keys else []

    print("Creating droplet...")
    droplet = create_droplet(api_token, droplet_name, region, size, image, ssh_keys)

    print("Droplet created successfully!")
    print(f"Droplet IP Address: {droplet.ip_address}")

    if args.ports:
        print("Setting up SSH and port tunneling...")
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(droplet.ip_address, username='root', key_filename=args.ssh_keys[0])
        configure_port_tunneling(ssh, args.ports)
        ssh.close()

def main():
    cli_entry()

if __name__ == "__main__":
    main()
