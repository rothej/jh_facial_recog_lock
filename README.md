# Facial Recognition Lock Using OpenCV

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Facial Recognition Lock/Alert System for Embedded Systems Development Lab, Johns Hopkins University. 

This repository contains the necessary files and information to setup and deploy a scalable number of OpenCV Oak-1 AI facial recognition cameras that control door access locks, and log and alert the sysadmin to potential unauthorized entry attempts.

## Table of Contents

- [File Structure](#file-structure)
- [Installation](#installation)
- [Dependencies](#depedencies)
    - [Twilio](#twilio)
    - [Python Libraries](#python-libraries)
- [Server Setup](#server-setup)
- [License](#license)

## Installation <a name="installation"></a>

This repository is intended to be installed within a virtual environment. This is intended to be performed both on client and server hardware.

- `git clone https://github.com/rothej/jh_facial_recog_lock.git` to clone the repository.
- `cd jh_facial_recog_lock`
- `pip3 install virtualenv` (if needed).
- `virtualenv venv` to create a virtual environment.
- `source venv/bin/activate` to enter this newly created environment.
- `pip3 install -r requirements.txt` to install python dependencies.

## File Structure <a name="file-structure"></a>

- `.ref/` contains images used in this README file.

## Dependencies <a name="dependencies"></a>

This repository requires the following dependencies to function:

### Twilio <a name="twilio"></a>

Set up a Twilio account by following [these instructions](https://www.twilio.com/docs/sms/quickstart/python). If using a free trial, be aware that it can only send texts to verified phone numbers (which will initially be the phone number you use to set up the account). The values for your `.env` variables (`TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN`) will be provided and need to be added to `.env` manually.

### Python Libraries <a name="python-libraries"></a>

The following libraries will be stored in `requirements.txt` using `pip3 freeze`, and installed during the Installation step. They are listed here for user reference.

- `dotenv`, install using `pip3 install python-dotenv`.
- `twilio`, install using `pip3 install twilio`.

## Server Setup <a name="server-setup"></a>

The machine you may use as a server can vary, but this walkthrough is written for Ubuntu (and should hold for any other Debian-based system). Basic server/client setup suggestions are as follows:

- Modify `/etc/ssh/sshd_config` to allow PasswordAuthentication (uncomment PasswordAuthentication and set to yes).
- Run `systemctl restart ssh` to restart the ssh service. 
- With passwords temporarily authorized, you can use `ssh-keygen` on any client machines (including the Raspberry Pi) and copy them to the server to allow for remote login. This can be done using `ssh-copy-id`, or paste the text manually into the `~/.ssh/authorized_keys` file.
- It is recommended that once SSH keys are set up, PasswordAuthentication should be changed back to “no”. Setting up port forwarding on port 22 will allow the user to SSH in externally from outside the network (port forwarding is beyond the scope of this guide, but a search for the topic as well as the router being used for the network should suffice).

## License <a name="license"></a>

[MIT © Joshua Rothe.](../LICENSE)