# DigitalOcean Droplet CLI

This lightweight Python CLI tool simplifies the process of creating and configuring DigitalOcean droplets. It supports automation for:

- Creating droplets using a YAML configuration file.
- Adding SSH keys to the droplet.
- Setting up port tunneling for tools like Jupyter Notebook and remote VSCode.

---

## Features

1. Automates droplet creation with user-defined settings.
2. Configures SSH keys for secure access.
3. Supports port tunneling for remote applications.
4. Outputs the public IP address of the droplet upon successful creation.

---

## Installation

### Prerequisites

1. Python 3.8 or later installed.
2. A DigitalOcean account and API token.
3. SSH keys for accessing your droplets.

### Install Dependencies

1. Clone the repository:

   ```bash
   git clone <repo_url>
   cd droplet-cli
   ```

2. Install required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

Prepare a `config.yaml` file with the following structure:

```yaml
api_token: "your_digitalocean_api_token"
droplet_name: "example-droplet"
region: "nyc3"
size: "s-1vcpu-1gb"
image: "ubuntu-20-04-x64"
```

- **api\_token**: Your DigitalOcean API token.
- **droplet\_name**: A name for your droplet.
- **region**: DigitalOcean region (e.g., `nyc3`, `sfo3`).
- **size**: Droplet size slug (e.g., `s-1vcpu-1gb`).
- **image**: Image slug (e.g., `ubuntu-20-04-x64`).

---

## Usage

### Command-Line Arguments

Run the tool with the following options:

```bash
python main.py --config config.yaml [OPTIONS]
```

| Argument     | Description                                                          |
| ------------ | -------------------------------------------------------------------- |
| `--config`   | Path to the YAML configuration file (required).                      |
| `--ssh-keys` | List of SSH key file paths to add to the droplet.                    |
| `--ports`    | List of ports to set up tunneling (e.g., 8888 for Jupyter Notebook). |

### Example Commands

1. **Create a droplet with SSH keys:**

   ```bash
   python main.py --config config.yaml --ssh-keys ~/.ssh/id_rsa ~/.ssh/other_key
   ```

2. **Set up port tunneling:**

   ```bash
   python main.py --config config.yaml --ports 8888 9000
   ```

---

## Outputs

- The script prints the droplet's public IP address upon successful creation.
- Logs any issues encountered during the process.

---

## Dependencies

Install the dependencies using `requirements.txt`:

```plaintext
pyyaml
python-digitalocean
paramiko
```

---

## License

This project is licensed under the MIT License.

