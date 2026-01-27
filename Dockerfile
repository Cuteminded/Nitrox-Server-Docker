FROM mcr.microsoft.com/dotnet/runtime:9.0
ARG TARGETARCH
ENV TZ=Etc/UTC
ENV NITROX_VERSION=1.8.1.0
ENV SUBNAUTICA_INSTALLATION_PATH=/mnt/subnautica
ENV CONFIG_EDITOR=false
ENV CONFIG_EDITOR_USER=nitrox
ENV CONFIG_EDITOR_PASS=nitrox
EXPOSE 5000
EXPOSE 11000/udp
WORKDIR /app
RUN mkdir -p /app/config/Nitrox
VOLUME [ "/app/config/Nitrox" ]
RUN mkdir -p /app/config/configEditor
COPY config_editor.py /app/config/configEditor/
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y --no-install-recommends ca-certificates curl unzip python3 python3-flask python3-waitress
RUN rm -rf /var/lib/apt/lists/*

# download + extract Nitrox Linux release
RUN set -eux; \
    if [ "$TARGETARCH" = "arm64" ]; then \
        curl -fL -o /tmp/nitrox.zip "https://github.com/SubnauticaNitrox/Nitrox/releases/download/${NITROX_VERSION}/Nitrox_${NITROX_VERSION}_linux_arm64.zip"; \
    elif [ "$TARGETARCH" = "amd64" ]; then \
        curl -fL -o /tmp/nitrox.zip "https://github.com/SubnauticaNitrox/Nitrox/releases/download/${NITROX_VERSION}/Nitrox_${NITROX_VERSION}_linux_x64.zip"; \
    else \
        echo "Unsupported architecture: $TARGETARCH" && exit 1; \
    fi
RUN unzip /tmp/nitrox.zip -d /app/Nitrox
RUN rm /tmp/nitrox.zip
WORKDIR /app/Nitrox

# setup boot script
COPY boot.sh /usr/bin/CMBoot
RUN chmod +x /usr/bin/CMBoot
RUN chmod +x /app/Nitrox/Nitrox.Server.Subnautica
CMD ["CMBoot"]

