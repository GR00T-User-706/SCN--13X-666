
### install.sh (Unix/Linux/macOS)

```bash
#!/bin/bash
# ShadowVeil Installation Script (Unix/Linux/macOS)

# Check for root privileges
if [ "$EUID" -ne 0 ]; then
  echo "⚠️  Please run as root for full functionality"
  read -p "Continue without root? [y/N] " -n 1 -r
  echo
  [[ $REPLY =~ ^[Yy]$ ]] || exit 1
fi

# Check dependencies
command -v python3 >/dev/null 2>&1 || {
  echo >&2 "❌ Python 3 not found. Please install:"
  echo "   Linux: sudo apt install python3 python3-pip"
  echo "   macOS: brew install python"
  exit 1
}

# Create virtual environment
VENV_DIR="${HOME}/.shadowveil_venv"
echo "🔧 Creating virtual environment..."
python3 -m venv "$VENV_DIR"
source "${VENV_DIR}/bin/activate"

# Install package
echo "⬇️  Installing ShadowVeil..."
pip install git+https://github.com/your-username/shadowveil.git

# Create symbolic link
echo "🔗 Creating system link..."
ln -sf "${VENV_DIR}/bin/shadowveil" /usr/local/bin/shadowveil

# Verify installation
if command -v shadowveil &> /dev/null; then
  echo -e "\n✅ Installation complete!"
  echo -e "Run 'shadowveil --help' to get started\n"
else
  echo -e "\n❌ Installation failed!"
  echo "Try manual installation:"
  echo "1. source ${VENV_DIR}/bin/activate"
  echo "2. shadowveil --help"
fi

# Post-install message
echo "For dashboard integration:"
echo "1. Place virtual environment path in hub config:"
echo "   ${VENV_DIR}/lib/python*/site-packages/shadowveil"
echo "2. Restart your cybersecurity hub"