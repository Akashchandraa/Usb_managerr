Secure USB Manager
Secure USB Manager is a Python-based desktop application that allows users to block or unblock USB storage devices on their Windows system securely. The application uses an OTP (One-Time Password) verification system to ensure that only authorized users can manage USB devices. Additionally, it captures a photo via a webcam if multiple incorrect OTP attempts are made.

Features:
 OTP Verification: Sends a one-time password to a pre-defined email address for authentication before allowing USB control.
 Block/Unblock USB Drives: Block or unblock USB storage devices on the system after successful OTP verification.
 Capture Image on Failed Attempts: Captures an image using the webcam if there are multiple failed OTP verification attempts.
 User Interface: A user-friendly graphical interface built with Tkinter.
 
Admin Check: Ensures that the application is run with administrative privileges for necessary registry modifications.

Prerequisites:
 Windows Operating System
 Python 3.x
 A Gmail account to send OTP emails
 
Required Python packages (listed below):
 opencv-python
 smtplib
 tkinter
 ctypes

Usage
Run the Application:
Make sure to run the application with administrative privileges.
Execute the following command in your terminal or command prompt:
#bash (Copy code)
python secure_usb_manager.py

User Interface:
 Send OTP: Click the "Send OTP" button to receive a one-time password via email.
 Verify OTP: Enter the OTP in the provided field and click "Verify OTP".
 Block/Unblock USB: After successful OTP verification, the "Block USB" and "Unblock USB" buttons will be enabled. Click to manage USB storage devices.
 
Failed OTP Attempts:
 If the wrong OTP is entered more than twice, an image will be captured using the webcam, and the application will disable further attempts.

Project Structure:
bash (Copy code)
secure-usb-manager/
│
├── email_cred.py         # Contains email credentials (not included in the repo)
├── secure_usb_manager.py # Main application file
└── CapturedImages/       # Directory to store captured images (created automatically)

Disclaimer:
 This software is provided "as-is" without any warranty. Use it at your own risk. The author is not responsible for any damage caused by using this software.

Contributing:
 Contributions are welcome! Please fork the repository and submit a pull request with your improvements.
