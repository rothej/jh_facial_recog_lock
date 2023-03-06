# Facial Recognition Lock Using OpenCV

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Facial Recognition Lock/Alert System for Embedded Systems Development Lab, Johns Hopkins University. 

This repository contains the necessary files and descriptiosn to setup and deploy a scalable number of OpenCV Oak-1 AI facial recognition cameras that control door access locks, and log and alert the sysadmin to potential unauthorized entry attempts.

## Table of Contents

- [File Structure](#file-structure)
- [Dependencies](#depedencies)
    - [Twilio](#twilio)
- [Server Setup](#server-setup)
- [License](#license)

## File Structure <a name="file-structure"></a>

- `.ref/` contains images used in this README file.

## Dependencies <a name="dependencies"></a>

This repository requires the following dependencies to function:

### Twilio <a name="twilio"></a>

Set up a Twilio account by following [these instructions](https://www.twilio.com/docs/sms/quickstart/python). If using a free trial, be aware that it can only send texts to verified phone numbers (which will initially be the phone number you use to set up the account). The values for 

- `dotenv`, install using `pip3 install python-dotenv`

## Server Setup <a name="server-setup"></a>

The machine you may use as a server can vary, but this walkthrough is written for Ubuntu (and should hold for any other Debian-based system). Basic server/client setup suggestions are as follows:

- Modify `/etc/ssh/sshd_config` to allow PasswordAuthentication (uncomment PasswordAuthentication and set to yes).
- Run `systemctl restart ssh` to restart the ssh service. 
- With passwords temporarily authorized, you can use `ssh-keygen` on any client machines (including the Raspberry Pi) and copy them to the server to allow for remote login. This can be done using `ssh-copy-id`, or paste the text manually into the `~/.ssh/authorized_keys` file.
- It is recommended that once SSH keys are set up, PasswordAuthentication should be changed back to “no”. Setting up port forwarding on port 22 will allow the user to SSH in externally from outside the network (port forwarding is beyond the scope of this guide, but a search for the topic as well as the router being used for the network should suffice).

## License <a name="license"></a>

[MIT © Joshua Rothe.](../LICENSE)