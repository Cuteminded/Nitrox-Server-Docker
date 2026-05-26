# Nitrox Server Docker
A docker image that runs the Nitrox server software for the game Subnautica.
> Works with Nitrox `1.8.1.0` on `x64` and `ARM64`.

## Links
Visit the official Nitrox website [here](https://nitrox.rux.gg/download).<br>
You can find the original repository for this project [here](https://github.com/Cuteminded/Nitrox-Server-Docker).

## Tested Environments

It may work on other environments as well, but these are the ones that have been tested:

- Ubuntu 24.04 **[x64]**
- MacOs Tahoe **[ARM64]**
- Windows 11 **[x64]**
- Raspberry Pi OS 13 (trixie) **[ARM64]**
  * Raspberry Pi 4 model B
  * External SSD for storage
  * 4GB RAM

### GUI Config Editor
The image includes a web-based GUI config editor for editing the server configuration file.
To enable the config editor, set the `CONFIG_EDITOR` environment variable to `true` when running the container.

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
      - "8080:8080" # GUI Config Editor Port (if enabled)
    environment:
      TZ: "Etc/UTC"
      NITROX_SAVE: "My World" # Optional, name of the save to use for the server, default is "My World"
      SUBNAUTICA_INSTALLATION_PATH: "/mnt/subnautica" # Optional, only needed if the folder is not mounted to the default path in the container
      CONFIG_EDITOR: true # Optional, set to "true" to enable the GUI config editor Default: false
      CONFIG_EDITOR_USER: "nitrox" # Optional, username for the GUI config editor   Default: nitrox
      CONFIG_EDITOR_PASS: "nitrox" # Optional, password for the GUI config editor   Default: nitrox Please change these for better security if you enable the config editor!
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

## Disclaimer
This project is not affiliated with either the Nitrox or the Subnautica developers.
