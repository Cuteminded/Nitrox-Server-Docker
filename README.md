# Nitrox Server Docker
A docker image that runs the Nitrox server software for the game Subnautica.
> Works with Nitrox `1.8.1.0` on `x64` and `ARM64`.

## Links
Visit the official Nitrox website [here](https://nitrox.rux.gg/download).<br>
You can find the original repository for this project [here](https://github.com/Cuteminded/Nitrox-Server-Docker).

### Docker
To run the image using docker, use the following command:

```bash
docker run --name "nitrox" --volume "nitrox-data:/app/config/Nitrox" --volume "/path/to/subnautica:/mnt/subnautica" --publish 11000:11000/udp cuteminded/nitrox-server
```

### Docker-Compose
To run the image using docker-compose, adjust this docker-compose file to your needs:

```yaml
services:
  nitrox:
    image: "cuteminded/nitrox-server:latest"
    restart: "unless-stopped"
    tty: true
    stdin_open: true
    ports:
      - "11000:11000/udp" # Nitrox Game Port
      - "50000:50000" # GUI Config Editor Port (if enabled)
    environment:
      TZ: "Etc/UTC"
      SUBNAUTICA_INSTALLATION_PATH: "/mnt/subnautica"
    volumes:
      - "nitrox-data:/app/config/Nitrox"
      - "/path/to/subnautica:/mnt/subnautica"
volumes:
  nitrox-data: 
```

Place the `docker-compose.yml` file somewhere on your server and run `docker-compose up` in the same directory to start the server.<br>
Replace `/path/to/subnautica` with the path to the Subnautica installation directory, for Steam this will be something like: `/path/to/steam/steamapps/common/Subnautica`.<br>
Set the timezone to your own for proper timestamps in the logs.

### Server Configuration
You can find your server files including the configuration files in the `nitrox-data` volume.<br>
Docker volumes are usually stored in `/var/lib/docker/volumes`.

### GUI Config Editor
The image includes a web-based GUI config editor for editing the server configuration file.

#### Enabling the Config Editor
```bash
-e CONFIG_EDITOR=true -e CONFIG_EDITOR_USER=yourusername -e CONFIG_EDITOR_PASS=yourpassword
```

## Disclaimer
This project is not affiliated with either the Nitrox or the Subnautica developers.
