#!/bin/bash

# This shell script is intended for testing purposes only.
#
# Install an NFS server, configures it, and mounts the
# shared path defined by ${SHARE_DIR}.

# read config vars
chmod a+x "./nfs-server-config" && . "nfs-server-config"

# Install NFS Kernel Server if it's not already installed
if ! command -v nfs-kernel-server > /dev/null 2>&1; then
    echo "Installing NFS Kernel Server..."
    sudo apt-get update
    sudo apt-get install -y nfs-kernel-server
else
    echo "NFS Kernel Server is already installed."
fi

# Create the shared directory if it doesn't exist
if [ ! -d "$SHARE_DIR" ]; then
    echo "Creating shared directory at $SHARE_DIR"
    sudo mkdir -p "$SHARE_DIR"
fi

# Update NFS exports file
echo "  Updating NFS exports..."
echo "${SHARE_DIR} ${IP_USE}(rw,sync,no_subtree_check)" | sudo tee -a /etc/exports

# Restart NFS service to apply changes
echo "  Restarting NFS service..."
sudo systemctl restart nfs-kernel-server

echo "  Mounting NFS drive..."
sudo mkdir -p "${MNT_POINT}" && sudo mount -t nfs "${NFS_ADDR}" "${MNT_POINT}"

echo ""
echo "NFS server setup complete. Shared directory: $SHARE_DIR"
