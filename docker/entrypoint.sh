#!/bin/sh

: "${tonie_username:?Environment variable tonie_username is required}"
: "${tonie_password:?Environment variable tonie_password is required}"
: "${tonie_household:?Environment variable tonie_household is required}"

exec python -m tonie_sync
