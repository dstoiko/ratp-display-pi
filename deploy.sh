#!/bin/bash

# Install local dependencies
/usr/bin/python3 -m pip install -r requirements.txt

# Copy and change the system files.
# cmdline.txt cannot be pregenerated because it contains a partition UUID
# that is, by definition, unique
sudo cp -r root/* /
sudo sed -i 's/rootwait quiet splash/rootwait splash/' /boot/cmdline.txt

# Make sure all scripts are executable
sudo chmod a+x src/main.py

# Enable service
sudo systemctl start ratp.service
sudo systemctl enable ratp.service
echo "RATP service deployed"
