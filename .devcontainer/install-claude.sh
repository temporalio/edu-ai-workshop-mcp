#!/bin/bash
echo "Installing Claude Desktop (this takes 2-3 minutes)..."
cd /tmp
wget --show-progress -O claude.deb \
    "https://storage.googleapis.com/osprey-downloads-c02f6a0d-347c-492b-a752-3e0651722e97/claude-desktop-linux-x64-latest.deb"
sudo apt-get install -y ./claude.deb
rm claude.deb
echo "Claude Desktop installed!"
echo "   Access it at port 6080 - it should already be available"