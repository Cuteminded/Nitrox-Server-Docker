#!/bin/bash
cat << "EOF"
 ██████╗██╗   ██╗████████╗███████╗███╗   ███╗██╗███╗   ██╗██████╗ ███████╗██████╗ 
██╔════╝██║   ██║╚══██╔══╝██╔════╝████╗ ████║██║████╗  ██║██╔══██╗██╔════╝██╔══██╗
██║     ██║   ██║   ██║   █████╗  ██╔████╔██║██║██╔██╗ ██║██║  ██║█████╗  ██║  ██║
██║     ██║   ██║   ██║   ██╔══╝  ██║╚██╔╝██║██║██║╚██╗██║██║  ██║██╔══╝  ██║  ██║
╚██████╗╚██████╔╝   ██║   ███████╗██║ ╚═╝ ██║██║██║ ╚████║██████╔╝███████╗██████╔╝
 ╚═════╝ ╚═════╝    ╚═╝   ╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═════╝ 
EOF
echo "[CM] Nitrox Version: ${NITROX_VERSION}"
echo "[CM] Subnautica Installation Path: ${SUBNAUTICA_INSTALLATION_PATH}"
echo "[CM] Starting Nitrox Services..."
export HOME=/app
export XDG_CONFIG_HOME=/app/config

if [ "${CONFIG_EDITOR}" = "true" ]; then
    echo "[CM] Starting Configuration Editor..."
    python3 /app/config/configEditor/config_editor.py &
fi
/app/Nitrox/Nitrox.Server.Subnautica --game-path ${SUBNAUTICA_INSTALLATION_PATH}

