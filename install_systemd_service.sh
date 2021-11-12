#!/bin/bash

BOT_PATH="$(pwd)"
CONFIG_PATH="${HOME}/sandworm.conf"
SYSTEMD_SERVICE_PATH="${HOME}/.config/systemd/user"

mkdir -p "${SYSTEMD_SERVICE_PATH}"
cat > "${SYSTEMD_SERVICE_PATH}/sandworm-bot.service" << EOF
[Unit]
Description=Sandworm telegram bot for Moonraker service
After=network-online.target

[Install]
WantedBy=default.target

[Service]
Type=simple
WorkingDirectory=${BOT_PATH}
ExecStart=/usr/bin/env python3 -m app --config ${CONFIG_PATH}
Restart=always
RestartSec=5
StandardOutput=journal
EOF

if [ ! -f "${CONFIG_PATH}" ]; then
  cp "${BOT_PATH}/sandworm.conf" "${CONFIG_PATH}"
fi

cat << EOF
config location
  "${CONFIG_PATH}"

systemd service location
  "${SYSTEMD_SERVICE_PATH}/sandworm-bot.service"

execute:

  $ systemctl --user daemon-reload
  $ sustemctl --user enable sandworm-bot.service
  $ sustemctl --user start sandworm-bot.service
  $ loginctl enable-linger ${USER}

EOF
