"""
Direct server startup script for phone connectivity.
This bypasses the config file and directly specifies host and port.
"""
from typing import Final
from backend.app import create_app
from quart import Quart
import socket

def get_local_ip() -> str:
    """Get the local IP address of the computer on the WiFi network"""
    try:
        # Connect to an external server to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "192.168.1.13"  # Fallback IP

def main() -> None:
    local_ip = get_local_ip()

    print("=" * 60)
    print("Starting Skin Disease Detection Backend")
    print("=" * 60)
    print()
    print("🌐 Server will be accessible at:")
    print("   - From this computer: http://127.0.0.1:5000/")
    print(f"   - From your phone:    http://{local_ip}:5000/")
    print()
    print("📱 Make sure your phone is on the SAME WiFi network!")
    print("=" * 60)
    print()

    app: Final[Quart] = create_app()

    # Force the server to listen on all network interfaces
    # This overrides any config file settings
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    main()
