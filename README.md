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
- [Bill of Materials](#bom)
- [Client Hardware Setup](#hw-setup)
- [Server and Client Software Setup](#server-setup)
- [First-Time Software Setup](#first-time)
- [Software Run](#software-run)
- [License](#license)

## Installation <a name="installation"></a>

This repository is intended to be installed within a virtual environment. This is intended to be performed both on client and server hardware.

- `git clone https://github.com/rothej/jh_facial_recog_lock.git` to clone the repository.
- `cd jh_facial_recog_lock`.
- `sudo apt-get install -y python3-venv` (if needed).
- `python3 -m venv frlock_venv` to create a virtual environment named frlock_venv.
- `source frlock_venv/bin/activate` to enter this newly created environment (note: `frlock_venv\Scripts\activate` for Windows, no `source`).
- `sudo apt-get -y install libsasl2-dev python3-dev libldap2-dev libssl-dev build-essential python2.7-dev slapd ldap-utils tox lcov valgrind` to install library dependencies.
- `pip3 install -r requirements.txt` to install python dependencies.

## File Structure <a name="file-structure"></a>

- `.ref/` contains images used in this README file.
- `docs/` contains the Makefile and relevant files.
- `examples\` contains examples of additional clients.
- `src\` contains all source files for this project - server and client scripts.
    - `src\jh_facial_recog_lock\frserver.py` is the server python code.
    - `src\jh_facial_recog_lock\frclient.py` is the client python code.
- `requirements.txt` contains environment dependencies to be installed upon venv creation.
- `tests\` contains test scripts to verify certain functionalities.

## Dependencies <a name="dependencies"></a>

This repository requires the following dependencies to function:

### Twilio <a name="twilio"></a>

Set up a Twilio account by following [these instructions](https://www.twilio.com/docs/sms/quickstart/python). For sending texts within the U.S., a free trial account will not suffice - you will need to load money onto your account to use the texting functionality (minimum of $20, however each text costs significantly less). The values for your `.env` variables (`TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN`) will be provided and need to be added to `.env` manually. You will also need to fill in `TWILIO_USR_PHONE_NUMBER` with the appropriate user phone number (in format `+18005555555`) and then do the same for `TWILIO_FROM_PHONE_NUMBER` (this will be the Twilio-created phone number you will receive alerts from). 

Note: Service now needs to be paid to send texts in the US.

Example format for the .env file (place this in the top-level directory):

```
TWILIO_ACCOUNT_SID=1234567890
TWILIO_AUTH_TOKEN=1234567890
TWILIO_USR_PHONE_NUMBER=+18005555555
TWILIO_FROM_PHONE_NUMBER=+18005555555
```

Next you will need to install Twilio CLI (Server Only):

```
wget -qO- https://twilio-cli-prod.s3.amazonaws.com/twilio_pub.asc | sudo apt-key add -
sudo touch /etc/apt/sources.list.d/twilio.list
echo 'deb https://twilio-cli-prod.s3.amazonaws.com/apt/ /' | sudo tee /etc/apt/sources.list.d/twilio.list
sudo apt update
sudo apt install -y twilio
```

With this complete, run `twilio login` and input your credentials from your Twilio account.

### Python Libraries <a name="python-libraries"></a>

The following libraries will be stored in `requirements.txt` using `pip3 freeze > requirements.txt`, and installed during the Installation step. They are listed here for user reference.

- `dotenv`, install using `pip3 install python-dotenv`.
- `twilio`, install using `pip3 install twilio`.
- `zmq`, install using `pip3 install pyzmq`.
- `blobconverter`, install using `pip3 install blobconverter`.
- `cv`, install using `pip3 install opencv-python`.
- `depthai`, install using `sudo wget -qO- https://docs.luxonis.com/install_depthai.sh | bash` and also `pip3 install depthai`
- `OpenLDAP`, install using `pip3 install python-ldap`.
- `MultiMsgSync`, install using `pip3 install multisync`.

Note: for Windows testing, use `python3 -m pip install <package>`. DepthAI will need to be installed using a [Windows Installer](https://docs.luxonis.com/en/latest/pages/tutorials/first_steps/#first-steps-with-depthai). You will also have to install this manually on ubuntu systems as well.

## Bill of Materials <a name="bom"></a>

The following lists the hardware used for this project. Feel free to deviate from this list, but you may need to adjust the wiring diagram as necessary. Please note that server and client hardware needs to have at least 4 GB memory to run Ubuntu and not a Raspbian OS, which this software had trouble running on. Additionally, the performance of this system relies on a decent client to handle the image recognition script.

| Item                  | Qty | Source | Cost (ea.) |
| --------------------- | --- | ------ | --------- |
| OpenCW Ai Kit - Oak-1 | 1   | [OpenAI](https://store.opencv.ai/products/oak-1) | $149       |
| 5v 1-ch Relay Module  | 1   | [Amazon](https://www.amazon.com/dp/B00LW15A4W?psc=1&ref=ppx_yo2ov_dt_b_product_details) | $7.39      |
| Jumper Wires          | 1   | [Amazon](https://www.amazon.com/dp/B07GD2BWPY?psc=1&ref=ppx_yo2ov_dt_b_product_details) | $6.99      |
| Solenoid Lock         | 1   | [Amazon](https://www.amazon.com/dp/B0125VGLT0?psc=1&ref=ppx_yo2ov_dt_b_product_details) | $8.49      |
| DC 12V 1A PSUP        | 1   | [Amazon](https://www.amazon.com/dp/B07VQHYGRD?psc=1&ref=ppx_yo2ov_dt_b_product_details) | $6.99      |
| Raspberry Pi 4B Wifi  | 2   | [Amazon](https://www.amazon.com/dp/B07TC2BK1X?psc=1&ref=ppx_yo2ov_dt_b_product_details) | $147.50 ea |
| USB-C Charger 2 pcs   | 1   | [Amazon](https://www.amazon.com/dp/B0BQ1GFQVJ?psc=1&ref=ppx_yo2ov_dt_b_product_details) | $14.99     |

Due to supply chain issues with Raspberry Pi hardware, these prices are inflated versus their typical pricing, but are listed here as-purchased.

Total cost of this project was $361.35, with $20 being required for the Twilio account (due to U.S. regulations, the free trial of Twilio was not allowed to send texts, so a paid account was necessary to enable text functionality).

## Client Hardware Setup <a name="hw-setup"></a>

The Raspberry Pi client-side hardware should be connected as follows:

![Raspberry Pi Client Picture](.ref/rpi-client.png)

| Raspberry Pi Pins  | Relay Pins | DC Power Pins | Door Lock Pins | Color |
| ------------------ | ---------- | ------------- | -------------- | ----- |
| J8 Pin 2 (5VDC)    | DC+        |               |                | Red   |
| J8 Pin 6 (Gnd)     | DC-        |               |                | Black |
| J8 Pin 11 (GPIO17) | IN         |               |                | Brown |
|                    | NO         | -             | +              | Black |
|                    |            | +             | +              | Red   |
|                    | COM        |               | -              | Brown |

Connect the Oak-CV1 camera to any USB3 (blue) slot on the board, and connect Power In on the Raspberry Pi to a wall outlet or other power source (this will obviously also apply to the server hardware).

Colors are obviously optional, and provided as a reference along with the picture.

![Raspberry Pi Client Picture](.ref/rpi-pinouts.png)

## Server and Client Software Setup <a name="server-setup"></a>

Follow [this](https://ubuntu.com/tutorials/how-to-install-ubuntu-desktop-on-raspberry-pi-4#1-overview) guide to set up Ubuntu on the SD card for the raspberry pi. Once complete, do the following:

- Modify `/etc/ssh/sshd_config` to allow PasswordAuthentication (uncomment PasswordAuthentication and set to yes).
- Run `systemctl restart ssh` to restart the ssh service. 
- With passwords temporarily authorized, you can use `ssh-keygen` on any client machines (including the Raspberry Pi) and copy them to the server to allow for remote login. This can be done using `ssh-copy-id`, or paste the text manually into the `~/.ssh/authorized_keys` file.
- It is recommended that once SSH keys are set up, PasswordAuthentication should be changed back to “no”. Setting up port forwarding on port 22 will allow the user to SSH in externally from outside the network (port forwarding is beyond the scope of this guide, but a search for the topic as well as the router being used for the network should suffice).

Recommended steps for SSH-ing into the Raspberry Pi server or client is to use -X to enable GUI forwarding, and to SSH from a debian/linux environment. For Windows PC users, it is easy to set up an [Ubuntu WSL](https://learn.microsoft.com/en-us/windows/wsl/install) and SSH from there.

### First-Time Software Setup <a name="first-time"></a>

Run the following to set yourself up as an authorized user, replacing JohnDoe with your name.

```
python3 frclient.py --name JohnDoe
```

Repeat the above for any other authorized users you want to add. After running for 10 seconds or so, you will need to use Cntrl+C to kill the process – don’t worry, the image data will save properly. A longer run will add more images to the database, improving accuracy but potentially slowing down the python script.

### Software Run <a name="software-run"></a>

Activate the environment using `cd ~/jh_facial_recog_lock && source frlock_venv/bin/activate`

On the server, run `python3 frserver.py`

On the client, run `python3 frclient.py`

## License <a name="license"></a>

[MIT © Joshua Rothe.](../LICENSE)
