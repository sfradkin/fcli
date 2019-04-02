from .auth import Auth
from .envvarauth import EnvVarAuth
from .fileauth import FileAuth
from .keyboardauth import KeyboardAuth


class ComboAuth(Auth):
    def __init__(self, username):
        self._username = username

    def username(self):
        if self._username is not None:
            return self._username

        try:
            return EnvVarAuth().username()
        except Exception:
            try:
                return FileAuth().username()
            except Exception:
                return KeyboardAuth().username()

    def password(self):
        try:
            return EnvVarAuth().password()
        except Exception:
            try:
                return FileAuth().password()
            except Exception:
                return KeyboardAuth().password()

    def google_service_acct_creds(self):
        try:
            return EnvVarAuth().google_service_acct_creds()
        except Exception:
            try:
                return FileAuth().google_service_acct_creds()
            except Exception:
                return KeyboardAuth().google_service_acct_creds()

    def sheet_create_url(self):
        try:
            return EnvVarAuth().sheet_create_url()
        except Exception:
            try:
                return FileAuth().sheet_create_url()
            except Exception:
                return KeyboardAuth().sheet_create_url()
