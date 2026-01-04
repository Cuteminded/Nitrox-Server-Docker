# Nitrox Server Docker

A docker image that runs the Nitrox server software for the game Subnautica.

Visit the official Nitrox website [here](https://nitrox.rux.gg/download).
You can find the original repository for this project [here](https://github.com/Cuteminded/Nitrox-Server-Docker).

## Disclaimer
This project is not affiliated with either the Nitrox or the Subnautica developers.

## Usage
To run this image, you can either simply use docker or use docker-compose.

### Docker
To run the image using docker, use the following command:

```shell
docker run --name "nitrox" --volume "nitrox-data:/app/config/Nitrox" --volume "/path/to/subnautica:/mnt/subnautica" --publish 11000:11000/udp cuteminded/nitrox-server
```

### Docker-Compose

To run the image using docker-compose, adjust this docker-compose file to your needs:

```yaml
services:
  nitrox:
    image: "cuteminded/nitrox-server:latest"
    restart: "unless-stopped"
    ports:
      - "11000:11000/udp"
    volumes:
      - "nitrox-data:/app/config/Nitrox"
      - "/path/to/subnautica:/mnt/subnautica"
volumes:
  nitrox-data: 
```

Place the `docker-compose.yml` file somewhere on your server and run `docker-compose up` in the same directory to start the server.

Replace `/path/to/subnautica` with the path to the Subnautica installation directory, for Steam this will be something like: `/path/to/steam/steamapps/common/Subnautica`.
Replace the group ID and user ID with your own if needed, this will change the ownership permissions of the server data folder.
Set the timezone to your own for proper timestamps in the logs.

### Server Configuration

You can find your server files including the configuration files in the `nitrox-data` volume.
Docker volumes are usually stored in `/var/docker/volumes`.
