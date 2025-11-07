# Configuration Setup Guide

This guide will help you configure the app to connect to your backend server.

## Quick Setup

### Option 1: Use In-App Settings (Recommended)
1. Launch the app
2. Go to Settings
3. Click "Change Backend URL"
4. Enter your server address (e.g., `http://192.168.1.X:5000`)
5. Click "Test Connection" to verify
6. Start using the app!

### Option 2: Edit Source Code

#### For Android Emulator:
No changes needed! The app is already configured to use `http://10.0.2.2:5000/`

#### For Physical Android Device:

1. **Find your computer's local IP address:**
   ```cmd
   ipconfig
   ```
   Look for "IPv4 Address" under your Wi-Fi adapter (e.g., 192.168.1.X)

2. **Update the default URL in code:**
   
   Edit: `app/src/main/java/com/ahaanmehta/skin_disease/RetrofitClient.java`
   
   Find this line (around line 67):
   ```java
   return "http://YOUR_SERVER_IP:5000/";
   ```
   
   Replace with your actual IP:
   ```java
   return "http://192.168.1.13:5000/";  // Use YOUR IP here
   ```

3. **Add your IP to network security config (if needed):**
   
   Edit: `app/src/main/res/xml/network_security_config.xml`
   
   Add your IP address:
   ```xml
   <domain includeSubdomains="true">192.168.1.13</domain>
   ```

## Important Notes

- **Same Network:** Your phone and computer MUST be on the same Wi-Fi network
- **Firewall:** Make sure Python is allowed through Windows Firewall
- **Backend Running:** The backend server must be running before testing the app

## Troubleshooting

### Connection Failed
1. Verify backend is running (`python run_for_phone.py`)
2. Check that devices are on same Wi-Fi
3. Verify firewall settings
4. Try pinging the server IP from your phone's browser: `http://YOUR_IP:5000/`

### Wrong URL Format
The URL must be in this format:
- ✓ `http://192.168.1.13:5000`
- ✓ `http://10.0.2.2:5000`
- ✗ `192.168.1.13` (missing http://)
- ✗ `http://192.168.1.13` (missing port)

## Production Deployment

For production deployment with a public server:
1. Deploy the backend to a cloud service (AWS, Heroku, etc.)
2. Update the URL to your public server address
3. Consider using HTTPS for security
4. Update network security config accordingly

