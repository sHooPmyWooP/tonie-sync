#!/bin/sh

: "${TONIE_USERNAME:?Environment variable TONIE_USERNAME is required}"
: "${TONIE_PASSWORD:?Environment variable TONIE_PASSWORD is required}"
: "${TONIE_HOUSEHOLD:?Environment variable TONIE_HOUSEHOLD is required}"

exec python -m tonie_sync
