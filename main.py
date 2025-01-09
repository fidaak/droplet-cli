import argparse
import yaml
import subprocess
import os
import time
import digitalocean
from paramiko import SSHClient, AutoAddPolicy
from droplet_setup import load_yaml_config, create_droplet, setup_ssh_keys, configure_port_tunneling

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
    
    print("Creating droplet...")
    droplet = create_droplet(api_token, droplet_name, region, size, image)

    print("Droplet created successfully!")
    print(f"Droplet IP Address: {droplet.ip_address}")

    # Wait for SSH to be available
    time.sleep(30)

    print("Setting up SSH connection...")
    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    
    # Use the first SSH key for initial connection if provided
    key_filename = args.ssh_keys[0] if args.ssh_keys else None
    ssh.connect(droplet.ip_address, username='root', key_filename=key_filename)

    if args.ssh_keys:
        print("Copying SSH keys to droplet...")
        setup_ssh_keys(ssh, args.ssh_keys)

    if args.ports:
        print("Setting up port tunneling...")
        configure_port_tunneling(ssh, args.ports)
    
    ssh.close()

if __name__ == "__main__":
    cli_entry()
