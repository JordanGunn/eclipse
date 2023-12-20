#!/bin/bash

# source in files
chmod a+x "./nfs-client-config" && . "./nfs-client-config"

# Install NFS Client if it's not already installed
if ! command -v nfs-common > /dev/null 2>&1; then
    echo "Installing NFS Client..."
    sudo apt-get update
    sudo apt-get install -y nfs-common
else
    echo "NFS Client is already installed."
fi

# Create local mount point directory if it doesn't exist
if [ ! -d "${MNT_POINT}" ]; then
    echo "Creating local mount point at ${MNT_POINT}"
    sudo mkdir -p "${MNT_POINT}"
fi

# Mount the NFS share to the local mount point
echo "Mounting NFS share..."
sudo mkdir -p "${MNT_POINT}" && sudo mount -t nfs "${NFS_ADDR}" "${MNT_POINT}"

echo "NFS share mounted at ${MNT_POINT}"
