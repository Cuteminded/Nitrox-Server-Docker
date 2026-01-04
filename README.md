# Nitrox Server Docker

A docker image that runs the Nitrox server software for the game Subnautica.

Visit the official Nitrox website [here](https://nitrox.rux.gg/download).
You can find the original repository for this project [here](https://gitlab.qub1.com/multimedia/games/subnautica/nitrox-server-docker).

## Disclaimer

This project is not affiliated with either the Nitrox or the Subnautica developers.

## Usage

To run this image, you can either simply use docker or use docker-compose.

### Docker

To run the image using docker, use the following command:

```shell
docker run \
	--name "nitrox" \
	--volume "nitrox-data:/software/nitrox" \
	--volume "/path/to/subnautica:/software/subnautica" \
	--env "GROUP_ID=1000" \
	--env "USER_ID=1000" \
	--env "TIMEZONE=Etc/GMT" \
	--publish 11000:11000/udp \
	qub1/nitrox-server:latest
```

Replace `/path/to/subnautica` with the path to the Subnautica installation directory, for Steam this will be something like: `/path/to/steam/steamapps/common/Subnautica`.
Replace the group ID and user ID with your own if needed, this will change the ownership permissions of the server data folder.
Set the timezone to your own for proper timestamps in the logs.

### Docker-Compose

To run the image using docker-compose, adjust this docker-compose file to your needs:

```docker
version: "3.4"
services:
  nitrox:
    image: "qub1/nitrox-server:latest"
    restart: "unless-stopped"
    ports:
      - "11000:11000/udp" # Nitrox
    volumes:
      - "nitrox-data:/software/nitrox" # Stores your server data, such as the configuration and world data
      - "/path/to/subnautica:/software/subnautica" # Stores Subnautica's game files - you will need to copy your own game directory here by moving the contents of your Subnautica installation directory to this volume
    environment:
      - "GROUP_ID=1000" # The ID of the group to run Nitrox as (default=1000)
      - "USER_ID=1000" # The ID of the user to run Nitrox as (default=1000)
      - "TIMEZONE=Etc/GMT" # The timezone to run Nitrox with (default=Etc/GMT)
volumes:
  nitrox-data: 
```

Place the `docker-compose.yml` file somewhere on your server and run `docker-compose up` in the same directory to start the server.

### Server Configuration

You can find your server files including the configuration files in the `nitrox-data` volume.
Docker volumes are usually stored in `/var/docker/volumes`.
