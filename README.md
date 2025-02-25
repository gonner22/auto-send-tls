# Telestai Wallet Manager Script

This repository contains the Telestai Wallet Manager Script, developed by the Telestai Dev Team in 2025. The script provides a command-line interface for managing a Telestai wallet. It allows users to check their balance, list UTXOs, consolidate UTXOs, and automatically generate small transactions for testing purposes.

## Prerequisites

Before using this script, ensure that you have the following:

- **Telestai-qt Wallet**: The wallet must be installed and fully synchronized.
- **Python**: Ensure Python is installed on your system.
- **Dependencies**: Use `pip` to install required Python packages:
    - `python-dotenv`

## Installation

### Windows

1. **Download and Install Telestai Wallet**: Ensure the wallet is installed and synchronized.  
2. **Enable Server Mode in Telestai Wallet**: Open **Command Prompt** (`cmd.exe`) and run:  
   ```powershell
   telestai-qt -server
   ```  
   This ensures the wallet operates in server mode, allowing CLI tools to interact with it.  
3. **Place CLI Tools in System Path**: Ensure that `telestai-cli.exe`, `telestaid.exe`, and `telestai-qt.exe` are located in a directory like `C:\telestai\bin` and add it to the system `PATH`:  
   - Open the Start menu and search for **"Edit the system environment variables"**.  
   - In **System Variables**, find `Path`, edit it, and add `C:\telestai\bin`.  
4. **Install Python**: Ensure Python is installed on your system. You can download it from [python.org](https://www.python.org/downloads/) and check the **"Add Python to PATH"** option during installation.  
5. **Clone the Repository**: Open **Command Prompt** and run the following command to clone the repository and navigate into the directory:
   ```powershell
   git clone https://github.com/Telestai-Project/auto-send-tls
   cd auto-send-tls
   ```
6. **Create and Activate Virtual Environment**: Run the following commands to create a virtual environment and activate it:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
7. **Install Dependencies**: Use `pip` to install required Python packages:  
   ```powershell
   pip install python-dotenv
   ```  
8. **Configure .env File**: If necessary, edit the `.env` file to set up your environment variables. Use a text editor like Notepad to open and modify the file. Here are the variables you can configure:
   - `MIN_CONF=1`: Minimum confirmations required for UTXOs. Default is 1.
   - `MAX_UTXOS=500`: Maximum number of UTXOs to consolidate. Default is 500.
   - `CONSOLIDATION_THRESHOLD=118`: Only consolidate UTXOs below this value (TLS). Default is 118.
   - `WALLET_ADDRESS_INDEX=0`: This index contains wallet addresses that have received at least one payment. Addresses without any transactions are excluded. Default is 0.
9. **Run the Script**: Execute the script using Python:  
   ```powershell
   python auto-send.py
   ```  

**Note 1**: Be aware that transactions on the blockchain may take a few minutes to confirm. Therefore, the number of UTXOs will be updated once the transaction is confirmed.

**Note 2**: The script generates two log files:
- `consolidation.log`: This file logs the details of UTXO consolidation operations, including timestamps and any relevant messages or errors.
- `split.log`: This file logs the details of UTXO splitting operations, providing similar information as the consolidation log.

### macOS

1. **Download and Install Telestai Wallet**: Ensure the wallet is installed and synchronized.  
2. **Enable Server Mode in Telestai Wallet**: Open a **Terminal** and run:  
   ```bash
   telestai-qt -server
   ```  
   This ensures the wallet operates in server mode, allowing CLI tools to interact with it.  
3. **Place CLI Tools in System Path**: Ensure that `telestai-cli`, `telestaid`, and `telestai-qt` are located in `/usr/local/bin` so they are accessible system-wide:  
   ```bash
   sudo mv telestai-cli telestaid telestai-qt /usr/local/bin/
   ```  
4. **Install Python**: Ensure Python is installed on your system. If needed, install it using Homebrew:  
   ```bash
   brew install python
   ```  
5. **Clone the Repository**: Open a **Terminal** and run the following command to clone the repository and navigate into the directory:
   ```bash
   git clone https://github.com/Telestai-Project/auto-send-tls
   cd auto-send-tls
   ```
6. **Create and Activate Virtual Environment**: Run the following commands to create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
7. **Install Dependencies**: Use `pip` to install required Python packages:  
   ```bash
   pip install python-dotenv
   ```  
8. **Configure .env File**: If necessary, edit the `.env` file to set up your environment variables. Use a text editor like nano or vim to open and modify the file. Here are the variables you can configure:
   - `MIN_CONF=1`: Minimum confirmations required for UTXOs. Default is 1.
   - `MAX_UTXOS=500`: Maximum number of UTXOs to consolidate. Default is 500.
   - `CONSOLIDATION_THRESHOLD=118`: Only consolidate UTXOs below this value (TLS). Default is 118.
   - `WALLET_ADDRESS_INDEX=0`: This index contains wallet addresses that have received at least one payment. Addresses without any transactions are excluded. Default is 0.
9. **Run the Script**: Execute the script using Python:  
   ```bash
   python auto-send.py
   ```  

**Note 1**: Be aware that transactions on the blockchain may take a few minutes to confirm. Therefore, the number of UTXOs will be updated once the transaction is confirmed.

**Note 2**: The script generates two log files:
- `consolidation.log`: This file logs the details of UTXO consolidation operations, including timestamps and any relevant messages or errors.
- `split.log`: This file logs the details of UTXO splitting operations, providing similar information as the consolidation log.

### Linux

1. **Download and Install Telestai Wallet**: Ensure the wallet is installed and synchronized.  
2. **Enable Server Mode in Telestai Wallet**: Open a **Terminal** and run:  
   ```bash
   telestai-qt -server
   ```  
   This ensures the wallet operates in server mode, allowing CLI tools to interact with it.  
3. **Place CLI Tools in System Path**: Ensure that `telestai-cli`, `telestaid`, and `telestai-qt` are located in `/usr/local/bin` so they are accessible system-wide:  
   ```bash
   sudo mv telestai-cli telestaid telestai-qt /usr/local/bin/
   ```  
4. **Install Python**: Ensure Python is installed on your system. If needed, install it using your package manager:  
   ```bash
   sudo apt install python3  # Debian/Ubuntu  
   sudo dnf install python3  # Fedora  
   sudo pacman -S python     # Arch  
   ```  
5. **Clone the Repository**: Open a **Terminal** and run the following command to clone the repository and navigate into the directory:
   ```bash
   git clone https://github.com/Telestai-Project/auto-send-tls
   cd auto-send-tls
   ```
6. **Create and Activate Virtual Environment**: Run the following commands to create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
7. **Install Dependencies**: Use `pip` to install required Python packages:  
   ```bash
   pip install python-dotenv
   ```  
8. **Configure .env File**: If necessary, edit the `.env` file to set up your environment variables. Use a text editor like nano or vim to open and modify the file. Here are the variables you can configure:
   - `MIN_CONF=1`: Minimum confirmations required for UTXOs. Default is 1.
   - `MAX_UTXOS=500`: Maximum number of UTXOs to consolidate. Default is 500.
   - `CONSOLIDATION_THRESHOLD=118`: Only consolidate UTXOs below this value (TLS). Default is 118.
   - `WALLET_ADDRESS_INDEX=0`: This index contains wallet addresses that have received at least one payment. Addresses without any transactions are excluded. Default is 0.
9. **Run the Script**: Execute the script using Python:  
   ```bash
   python auto-send.py
   ```  

**Note 1**: Be aware that transactions on the blockchain may take a few minutes to confirm. Therefore, the number of UTXOs will be updated once the transaction is confirmed.

**Note 2**: The script generates two log files:
- `consolidation.log`: This file logs the details of UTXO consolidation operations, including timestamps and any relevant messages or errors.
- `split.log`: This file logs the details of UTXO splitting operations, providing similar information as the consolidation log.

## Usage

Once the script is running, you will be presented with a menu to perform various wallet management tasks such as checking balance, listing UTXOs, consolidating UTXOs, and generating small transactions for testing.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Developed by the Telestai Dev Team. 
