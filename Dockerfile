FROM mcr.microsoft.com/dotnet/runtime:9.0
ENV NITROX_VERSION=1.8.0.0
ENV SUBNAUTICA_INSTALLATION_PATH=/mnt/subnautica
EXPOSE 11000/udp
WORKDIR /app
RUN mkdir -p /app/config/Nitrox
VOLUME [ "/app/config/Nitrox" ]
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y --no-install-recommends ca-certificates curl unzip
RUN rm -rf /var/lib/apt/lists/*

# download + extract Nitrox Linux release
RUN curl -fL -o /tmp/nitrox.zip "https://github.com/SubnauticaNitrox/Nitrox/releases/download/${NITROX_VERSION}/Nitrox_${NITROX_VERSION}_linux_x64.zip"
RUN unzip /tmp/nitrox.zip -d /app/Nitrox
RUN mv /app/Nitrox/linux-x64/* /app/Nitrox/
RUN rmdir /app/Nitrox/linux-x64
RUN rm /tmp/nitrox.zip
WORKDIR /app/Nitrox

COPY boot.sh /usr/bin/CMBoot
RUN chmod +x /usr/bin/CMBoot
RUN chmod +x /app/Nitrox/NitroxServer-Subnautica
CMD ["CMBoot"]

