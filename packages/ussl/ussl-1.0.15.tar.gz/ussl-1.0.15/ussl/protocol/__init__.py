import logging
import sys

from .winrm import WinRMProtocol
from .ssh import SSHProtocol

try:
    from .ldap import LDAPProtocol
except ImportError:
    logging.warning('For the LDAP protocol to work correctly, install the dependency:')
    if 'win' in sys.platform.lower():
        logging.warning('\tpip install https://github.com/cgohlke/python-ldap-build/releases/download/v3.4.4/python_ldap-3.4.4-cp38-cp38-win_amd64.whl')
    else:
        logging.warning('\tpip install python-ldap==3.4.4')

INTERFACES = {
    'ssh': SSHProtocol,
    # 'winexe': WinexeProtocol,
    # 'wmi': WMIProtocol,
    'winrm': WinRMProtocol,
    'ldap': LDAPProtocol,
}