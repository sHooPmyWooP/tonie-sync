ARG DEBIAN_VERSION=bookworm
ARG VARIANT=3.13

FROM python:$VARIANT-slim-$DEBIAN_VERSION

WORKDIR /app

ENV TONIE_SYNC_VERSION="0.1.11"


RUN apt-get update \
&& apt-get install -y --no-install-recommends \
# For SpotDL
    git tini ffmpeg lame curl zlib1g \
    # To remove the image size, it is recommended refresh the package cache as follows
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

    # Copy the entrypoint script into the container
    COPY entrypoint.sh /app/entrypoint.sh
    RUN chmod +x /app/entrypoint.sh

RUN pip install --no-cache-dir tonie_sync==$TONIE_SYNC_VERSION
# Use the entrypoint script as the container's entry point
ENTRYPOINT ["/app/entrypoint.sh"]
