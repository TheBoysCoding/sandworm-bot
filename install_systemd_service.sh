#!/bin/bash

BOT_PATH="$(pwd)"
CONFIG_PATH="${HOME}/sandworm.conf"
SYSTEMD_SERVICE_PATH="${HOME}/.config/systemd/user"

mkdir -p "${SYSTEMD_SERVICE_PATH}"
cat > "${SYSTEMD_SERVICE_PATH}/sandworm-bot.service" << EOF
#Systemd service file for Moonraker Telegram Bot
[Unit]
Description=Moonraker Telegram Bot
After=network-online.target moonraker.service

[Install]
WantedBy=multi-user.target

[Service]
Type=simple
WorkingDirectory=${BOT_PATH}
ExecStart=/usr/bin/env python3 -m app --config ${CONFIG_PATH}
Restart=always
RestartSec=5
StandardOutput=journal
EOF

if [ ! -f "${CONFIG_PATH}" ]; then
  echo "Config sample copied to ${CONFIG_PATH}"
  cp "${BOT_PATH}/sandworm.conf" "${CONFIG_PATH}"
fi
