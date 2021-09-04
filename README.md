# Synology Certificate Import #

[![Source](https://badgen.net/badge/icon/Source?icon=github&label)](https://github.com/jan-di/syno-cert-import)
[![Checks](https://badgen.net/github/checks/jan-di/syno-cert-import)](https://github.com/jan-di/syno-cert-import/actions/workflows/build-docker-image.yml)
[![Release](https://badgen.net/github/release/jan-di/syno-cert-import/stable)](https://github.com/jan-di/syno-cert-import/releases)
[![Last Commit](https://badgen.net/github/last-commit/jan-di/syno-cert-import/main)](https://github.com/jan-di/syno-cert-import/commits/main)
[![License](https://badgen.net/github/license/jan-di/syno-cert-import)](https://github.com/jan-di/syno-cert-import/blob/main/LICENSE)

Python script to automatically import a certificate to a synology and set it as default certificate.

Docker Image Tags:

- `jandi/syno-cert-import` [Docker Hub](https://hub.docker.com/r/jandi/syno-cert-import)
- `ghcr.io/jan-di/syno-cert-import` [GitHub Container Registry](https://github.com/jan-di/syno-cert-import/pkgs/container/syno-cert-import)

## Configuration ##

The script is configured via enviroment variables:

Name | Default | Description
--- | --- | ---
`SYNO_SCHEME` | `https` | http/https
`SYNO_HOST` | - | IP-Adress or hostname of synology
`SYNO_PORT` | `5001` | Port of Web API
`SYNO_USERNAME` | - | User with administrative permissions
`SYNO_PASSWORD` | - | Password
`VERIFY_SSL` | `true` | Verify SSL Certificate
`KEY_FILE` | - | Path to key file
`CERT_FILE` | - | Path to cert file
`CHAIN_FILE` | - | Path to chain file

## Example ##

Sample script to use the image as a command:

```shell
DIR=$(pwd)

docker run \
    -v $DIR/cache:/cache:ro \
    -e SYNO_SCHEME="http" \
    -e SYNO_HOST="localhost" \
    -e SYNO_PORT="5000" \
    -e SYNO_USERNAME="<administrative user>" \
    -e SYNO_PASSWORD="<password>" \
    -e KEY_FILE="/cache/privkey.key" \
    -e CERT_FILE="/cache/cert.crt" \
    -e CHAIN_FILE="/cache/chain.crt" \
    --network host \
    jandi/syno-cert-import
```
- `--network host` is required, to let the script reach the Synology API via localhost. Otherwise the default gateway of the docker network must be used - this address could change, when the network is recreated.
- You could connect via `https/5001`, but the script will fail if the current certificate is not valid. When the script runs locally on the synology, http is recommended. Alternatively, you could disable ssl verification with `SSL_VERIFY=false`
