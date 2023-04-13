
# Originally contributed by Check Point Software Technologies, Ltd.

from lib.common.results import NetlogFile

def send_file(name, data):
    """Send file to result server"""
    nf = NetlogFile(name)
    nf.sock.sendall(data)
    nf.close()
