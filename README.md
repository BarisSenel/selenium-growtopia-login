# Growtopia Google Login Script

This script automates the process of logging into a Growtopia Google account using Selenium and undetected-chromedriver. It includes CAPTCHA verification handling and token extraction for further processing.

## Features

- Automated Google login
- CAPTCHA handling with CapSolver extension
- Token extraction for post-login processing
- Proxy support

## Requirements

- Python 3.x
- [Selenium](https://pypi.org/project/selenium/)
- [undetected-chromedriver](https://pypi.org/project/undetected-chromedriver/)
- [fake-useragent](https://pypi.org/project/fake-useragent/)
- [requests](https://pypi.org/project/requests/)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/BarisSenel/selenium-growtopia-login.git
    cd selenium-growtopia-login
    ```

2. Install the required Python packages:
    ```sh
    pip install selenium undetected-chromedriver fake-useragent requests
    ```

3. Download the CapSolver extension and place it in the project directory. Ensure the folder name is `Capsolver`.

## Usage

Run the script with the required arguments:
```sh
python getToken.py -mail your-email@gmail.com -password your-password -recoverymail your-recovery-email -proxy socks5://your-proxy
