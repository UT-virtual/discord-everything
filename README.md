# discord-everything

## Setup

Create `.env` file.

```.env
DISCORD_TOKEN="<discord-token>"
EVERYTHING_CHANNEL_ID="<channel-id>"
```

## systemd

support for user-run systemd

```sh
cd <repository root>
poetry run python3 generate_systemd_conf.py
systemctl --user start discord_everything_job.service
```
