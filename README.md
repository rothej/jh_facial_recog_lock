# Facial Recognition Lock Using OpenCV

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

#### Facial Recognition Lock/Alert System for Embedded Systems Development Lab, Johns Hopkins University. 

This repository contains the necessary files and information to setup and deploy a scalable number of OpenCV Oak-1 AI facial recognition cameras that control door access locks, and log and alert the sysadmin to potential unauthorized entry attempts.

## Table of Contents

- [File Structure](#file-structure)
- [Installation](#installation)
- [Dependencies](#depedencies)
    - [Twilio](#twilio)
    - [Python Libraries](#python-libraries)
- [Server Setup](#server-setup)
- [Client Setup](#client-setup)
    - [Raspberry Pi Zero W](#r-pi-zero-w)
    - [OpenCV Oak-1 Camera Setup](#camera-setup)
- [License](#license)

## Installation <a name="installation"></a>

This repository is intended to be installed within a virtual environment. This is intended to be performed both on client and server hardware.

- `git clone https://github.com/rothej/jh_facial_recog_lock.git` to clone the repository.
- `cd jh_facial_recog_lock`.
- `sudo apt-get install -y python3-venv` (if needed).
- `python3 -m venv frlock_venv` to create a virtual environment named frlock_venv.
- `source frlock_venv/bin/activate` to enter this newly created environment (note: `frlock_venv\Scripts\activate` for Windows, no `source`).
- `pip3 install -r requirements.txt` to install python dependencies.

## File Structure <a name="file-structure"></a>

- `.ref/` contains images used in this README file.
- `docs/` contains the Makefile and relevant files.
- `examples\` contains examples of additional clients.
- `src\` contains all source files for this project - server and client scripts.
    - `src\jh_facial_recog_lock\frserver.py` is the server python code.
- `requirements.txt` contains environment dependencies to be installed upon venv creation.
- `tests\` contains test scripts to verify certain functionalities.

## Dependencies <a name="dependencies"></a>

This repository requires the following dependencies to function:

### Twilio <a name="twilio"></a>

Set up a Twilio account by following [these instructions](https://www.twilio.com/docs/sms/quickstart/python). If using a free trial, be aware that it can only send texts to verified phone numbers (which will initially be the phone number you use to set up the account). The values for your `.env` variables (`TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN`) will be provided and need to be added to `.env` manually. You will also need to fill in `TWILIO_USR_PHONE_NUMBER` with the appropriate user phone number (in format `+18005555555`) and then do the same for `TWILIO_FROM_PHONE_NUMBER` (this will be the Twilio-created phone number you will receive alerts from).

Example format for the .env file (place this in the top level directory):

````
TWILIO_ACCOUNT_SID=1234567890
TWILIO_AUTH_TOKEN=1234567890
TWILIO_USR_PHONE_NUMBER=+18005555555
TWILIO_FROM_PHONE_NUMBER=+18005555555
````

Next you will need to install Twilio CLI (Server Only):

> `wget -qO- https://twilio-cli-prod.s3.amazonaws.com/twilio_pub.asc | sudo apt-key add -`
> `sudo touch /etc/apt/sources.list.d/twilio.list`
> `echo 'deb https://twilio-cli-prod.s3.amazonaws.com/apt/ /' | sudo tee /etc/apt/sources.list.d/twilio.list`
> `sudo apt update`
> `sudo apt install -y twilio`

With this complete, run `twilio login` and input your credentials from your Twilio account.

### Python Libraries <a name="python-libraries"></a>

The following libraries will be stored in `requirements.txt` using `pip3 freeze > requirements.txt`, and installed during the Installation step. They are listed here for user reference.

- `dotenv`, install using `pip3 install python-dotenv`.
- `twilio`, install using `pip3 install twilio`.
- `zmq`, install using `pip3 install pyzmq`.

Note: for Windows testing, use `python3 -m pip install <package>`.

## Server Setup <a name="server-setup"></a>

The machine you may use as a server can vary, but this walkthrough is written for Ubuntu (and should hold for any other Debian-based system). Basic setup suggestions are as follows, but if you know what you are doing feel free to deviate:

- Modify `/etc/ssh/sshd_config` to allow PasswordAuthentication (uncomment PasswordAuthentication and set to yes).
- Run `systemctl restart ssh` to restart the ssh service. 
- With passwords temporarily authorized, you can use `ssh-keygen` on any client machines (including the Raspberry Pi) and copy them to the server to allow for remote login. This can be done using `ssh-copy-id`, or paste the text manually into the `~/.ssh/authorized_keys` file.
- It is recommended that once SSH keys are set up, PasswordAuthentication should be changed back to ???no???. Setting up port forwarding on port 22 will allow the user to SSH in externally from outside the network (port forwarding is beyond the scope of this guide, but a search for the topic as well as the router being used for the network should suffice).

## Client Setup <a name="client-setup"></a>

### Raspberry Pi Zero W <a name="r-pi-zero-w"></a>

Follow [this](https://cdn-learn.adafruit.com/downloads/pdf/raspberry-pi-zero-creation.pdf) guide to set up the Raspberry Pi OS (skip to the bottom of page 12, and don't forget to do UART enabling when complete). Use the standard Raspberry Pi OS (32-bit) during image write, and click the gear icon to configure initial settings.

### OpenCV Oak-1 Camera Setup <a name="camera-setup"></a>

Follow the install instructions [here](https://docs.luxonis.com/en/latest/pages/tutorials/first_steps/#first-steps-with-depthai) to set up the DepthAI program on the Raspberry Pi client.

## License <a name="license"></a>

[MIT ?? Joshua Rothe.](../LICENSE)
