# syno-cert-import #

Python script to automatically import a certificate to a synology and set it as default certificate.

Image on Dockerhub: <https://hub.docker.com/r/jandi/syno-cert-import>

## Configuration ##

The script is configured via enviroment variables:

- `SYNO_SCHEME` http/https (optional, def. = https)
- `SYNO_HOST` IP-Adress or hostname of synology
- `SYNO_PORT` Port of Web API (optional, def. = 5001)
- `SYNO_USERNAME` User with administrative permissions
- `SYNO_PASSWORD` Password
- `KEY_FILE` Path to key file
- `CERT_FILE` Path to cert file
- `CHAIN_FILE` Path to chain file

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
- Network = Host is needed, so that the script can reach the Synology API via localhost. Otherwise the default gateway of the docker network must be used - this address could change, when the network is recreated.
- You could connect via https/5001, but the script will fail if the current certificate is not valid. When the script runs locally on the synology, http is recommended.
