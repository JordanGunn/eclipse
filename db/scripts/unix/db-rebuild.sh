#!/usr/bin/bash

# enable executable permissions
chmod a+x ./db-setup.sh
chmod a+x ./db-purge.sh

# run purge then setup
./db-purge.sh && ./db-setup.sh
