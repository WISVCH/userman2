import paramiko
import base64

from userman2.settings import SSH_ANK_PRIVKEY_FILE, SSH_ANK_HOSTKEY

hostkey = paramiko.Ed25519Key(data=base64.b64decode(SSH_ANK_HOSTKEY))
privkey = paramiko.Ed25519Key.from_private_key_file(SSH_ANK_PRIVKEY_FILE)
client = paramiko.SSHClient()
client.get_host_keys().add("ank.chnet", "ssh-ed25519", hostkey)
client.set_missing_host_key_policy(paramiko.RejectPolicy())


def execute_script(script):
    client.connect(hostname="ank.chnet", username="userman2", pkey=privkey)
    _, stdout, stderr = client.exec_command(script)
    status = stdout.channel.recv_exit_status()
    if status != 0:
        raise ScriptError("Script \"%s\" failed with exit code %d\n---stdout:\n%s\n---stderr:\n%s" %
                          (script, status, stdout.read(), stderr.read()))


class ScriptError(Exception):
    pass
