---
title: Create your own local multimedia server
summary: Install the arrs stack and jellyfin on Ubuntu server
date: 2050-09-01
badge: code
image:
---

## Connect yo your sever locally

```powershell
ssh username@192.168.X.Y
```

## Install Docker

## NordVPN

### Install
From [VPN documentation](https://support.nordvpn.com/hc/en-us/articles/20196094470929-Installing-NordVPN-on-Linux-distributions)

```shell
sh <(curl -sSf https://downloads.nordcdn.com/apps/linux/install.sh)
```

### Connect 

Add your user to the nordvpn group
```shell
sudo usermod -aG nordvpn $USER
newgrp nordvpn
```
(Log out & back in, or newgrp nordvpn to apply immediately.)


Login : From [doc](https://support.nordvpn.com/hc/en-us/articles/20226600447633-How-to-log-in-to-NordVPN-on-Linux-devices-without-a-GUI)

Follow the token method : 
```shell
nordvpn login --token 3fe460ksdnf415e45908cec9f9bdbadf7a456a6dfb35dc2c58xxxxx
```

Connect and enforce “Kill Switch”
```shell
# Connect to a recommended server
nordvpn connect

# Make sure Kill Switch is enabled
nordvpn set killswitch on

# Force VPN for all traffic (this is default if killswitch is on)
nordvpn set firewall on

# Auto-connect on boot
nordvpn set autoconnect on
```

Doing all this, you should not be able to connect from you local network anymore. When you enable NordVPN with killswitch/firewall on, the server is told “send everything through the VPN tunnel, block all other inbound/outbound traffic.”
That means:
* ✅ The server can reach the internet via VPN.
* ❌ Other machines on your LAN can’t reach the server anymore (SSH, HTTP, etc.), because NordVPN blocks direct local connections unless you configure it.

The solution is to allow LAN access with NordVPN. NordVPN client has a setting for this:

```shell
nordvpn set lan-discovery on
```


This allows devices on your local network to see and connect to the server (while still tunneling internet traffic through VPN).


### Test
Both IPs should correspond
```shell
nordvpn status

curl ipinfo.io
```

If not that usually means one of these:
* DNS / caching issue: Sometimes when you just connected, curl still uses a cached DNS or old route.
* IPv6 leak: If your server has IPv6 enabled, some traffic may bypass NordVPN (NordVPN by default tunnels only IPv4 unless IPv6 leak protection is enabled).

Solution : Force disable IPv6 (common fix for mismatched IPs with NordVPN):

```shell
sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1
sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1
```
(To make it permanent, add these lines to /etc/sysctl.conf.)

Then reconnect:
```shell
nordvpn disconnect
nordvpn connect
```
Test again:
```shell
curl ifconfig.io
curl ipinfo.io
```
It should report the same IP as in `nordvpn status`



## Ubuntu server

Installation steps
- Version : Ubuntu Server
- Language: English
- Keyboard: French/French
- Network Configuration: Wifi
- Proxy configuration: leave blank
- Ubuntu archive mirror configuration: do nothing
- Guided Storage configuration: use entire disk, set disk as lvm group
- Storage configuration: keep defaults
- Profile
  - Your name : kenshuri
  - Your servers name : kenshuri-server
  - username : kenshuri
- Ubuntu Pro : Skip for now
- SSH Configuration : default (don't install openssh)
- Snaps : select nothing


## Accept SSH connection

1. If you want to connect from your PC to the Ubuntu server (locally in your home network)

You’ll need SSH:

On the Ubuntu server, check that SSH is installed and running:
```shell
sudo apt update
sudo apt install openssh-server -y
sudo systemctl enable ssh
sudo systemctl start ssh
sudo systemctl status ssh
```

UUID=f8ecc37b-7a82-4ea0-9e94-969631660757   /mediastack/media   ext4   defaults   0   2


## Test below
error for  whisparr readarr



gluetun
plex
postgresql
sabnzbd
valkey
authentik
huntarr
portainer
tailscale
unpackerr
whisparr
bazarr
guacamole
chromium
traefik
crowdsec
grafana
heimdall
jellyseerr
radarr
sonarr
traefik-certs-dumper
lidarr
tdarr-node
ddns-updater
flaresolverr
homepage
prometheus
readarr
tdarr
filebot
guacd
prowlarr
authentic-worker
jellyfin
qbittorrent
headplane
headscale
homarr
mylar

gluetun	plex	postgresql	sabnzbd	valkey	authentik	huntarr	portainer	tailscale	unpackerr	whisparr	bazarr	guacamole	chromium	traefik	crowdsec	grafana	heimdall	jellyseerr	radarr	sonarr	traefik-certs-dumper	lidarr	tdarr-node	ddns-updater	flaresolverr	homepage	prometheus	readarr	tdarr	filebot	guacd	prowlarr	authentic-worker	jellyfin	qbittorrent	headplane	headscale	homarr	mylar



