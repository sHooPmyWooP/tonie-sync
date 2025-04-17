ARG DEBIAN_VERSION=bookworm
ARG VARIANT=3.13

FROM python:$VARIANT-slim-$DEBIAN_VERSION

WORKDIR /app

ENV SPOTIFY_CLIENT_ID=
ENV SPOTIFY_CLIENT_SECRET=
ENV TONIE_USERNAME=
ENV TONIE_PASSWORD=
ENV TONIE_HOUSEHOLD=
ENV CREATIVE_TONIE=
ENV QUERY=
ENV TARGET_DIRECTORY=

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    # For SpotDL
    git tini ffmpeg lame curl zlib1g \
    # To remove the image size, it is recommended refresh the package cache as follows
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

RUN pip install --no-cache-dir tonie_sync
# Use the entrypoint script as the container's entry point
ENTRYPOINT ["/app/entrypoint.sh"]
