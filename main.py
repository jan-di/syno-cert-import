import os
from datetime import datetime
from dotenv import load_dotenv

from src.util import Util
from src.synology import Synology

load_dotenv()

synoScheme = os.getenv("SYNO_SCHEME", "https")
synoHost = os.getenv("SYNO_HOST", None)
synoPort = os.getenv("SYNO_PORT", 5001)
synoUsername = os.getenv("SYNO_USERNAME", None)
synoPassword = os.getenv("SYNO_PASSWORD", None)
verifySsl = Util.strtobool(os.getenv("VERIFY_SSL", "true"))

if synoHost is None:
    raise Exception("Variable SYNO_HOST is not defined!")
if synoUsername is None:
    raise Exception("Variable SYNO_USERNAME is not defined!")
if synoPassword is None:
    raise Exception("Variable SYNO_PASSWORD is not defined!")

keyFile = os.getenv("KEY_FILE", None)
certFile = os.getenv("CERT_FILE", None)
chainFile = os.getenv("CHAIN_FILE", None)

if keyFile is None:
    raise Exception("Variable KEY_FILE is not defined!")
if certFile is None:
    raise Exception("Variable CERT_FILE is not defined!")
if chainFile is None:
    raise Exception("Variable CHAIN_FILE is not defined!")

syno = Synology(synoScheme, synoHost, synoPort, verifySsl)

print(
    "Connecting with {} to {}://{}:{}".format(
        synoUsername, synoScheme, synoHost, synoPort
    )
)
syno.login(synoUsername, synoPassword)
print("Logged in. SID: " + syno.sid)

oldCert = syno.getDefaultCert()
print(
    "Current default certificate: [{}] ({})".format(
        oldCert["id"], oldCert["subject"]["common_name"]
    )
)

desc = "Imported: {}".format(datetime.now().replace(microsecond=0).isoformat())
newCertId = syno.importDefaultCert(desc, certFile, chainFile, keyFile)
print("Imported new certificate [{}]".format(newCertId))

print(
    "Deleting previous default certificate [{}] (may take a while)..".format(
        oldCert["id"]
    )
)
deleteInfo = syno.deleteCert(oldCert["id"])
message = "Deleted certificate [{}].".format(oldCert["id"])
if deleteInfo["restart_httpd"]:
    message += " Restarting webserver.."
print(message)

syno.logout()
print("Logged out.")
