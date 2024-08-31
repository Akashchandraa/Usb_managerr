import ctypes
import os
import random
import smtplib
import string
import time
import tkinter as tk
import winreg as reg
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import messagebox

import cv2

from email_cred import gmail, password

# Global variables
generated_otp = ""
wrong_attempts = 0
max_attempts = 2

# Function to send OTP to email
def send_otp():
    global generated_otp
    email_address = "receiver mail"  # Hardcoded receiver email address
    generated_otp = ''.join(random.choices(string.digits, k=6))
    
    # Email details
    sender_email = gmail
    sender_password = password
    subject = "Your OTP Code"
    message = f"Your OTP code is {generated_otp}"

    try:
        # Set up the MIME
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email_address
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email_address, msg.as_string())
        server.quit()
        
        print("OTP sent successfully!")
        messagebox.showinfo("Success", "OTP sent successfully!")
    except Exception as e:
        print(f"Failed to send OTP: {e}")
        messagebox.showerror("Error", f"Failed to send OTP: {e}")

# Function to block USB drives
def block_usb():
    try:
        key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, r"SYSTEM\\CurrentControlSet\\Services\\USBSTOR", 0, reg.KEY_SET_VALUE)
        reg.SetValueEx(key, "Start", 0, reg.REG_DWORD, 4)
        reg.CloseKey(key)
        print("USB storage devices should be blocked.")
        messagebox.showinfo("Success", "USB storage devices are blocked.")
    except Exception as e:
        print(f"Failed to block USB storage: {e}")
        messagebox.showerror("Error", f"Failed to block USB storage: {e}")

# Function to unblock USB drives
def unblock_usb():
    try:
        key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, r"SYSTEM\\CurrentControlSet\\Services\\USBSTOR", 0, reg.KEY_SET_VALUE)
        reg.SetValueEx(key, "Start", 0, reg.REG_DWORD, 3)
        reg.CloseKey(key)
        print("USB storage devices should be unblocked.")
        messagebox.showinfo("Success", "USB storage devices are unblocked.")
    except Exception as e:
        print(f"Failed to unblock USB storage: {e}")
        messagebox.showerror("Error", f"Failed to unblock USB storage: {e}")

# Check if running as admin
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Function to capture an image from the webcam
def capture_image():
    # Create the directory if it doesn't exist
    save_dir = 'CapturedImages'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Initialize the camera
    cap = cv2.VideoCapture(0)
    time.sleep(2)  # Allow the camera to warm up

    # Capture an image
    ret, frame = cap.read()
    if ret:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = os.path.join(save_dir, f"attempt_{timestamp}.png")
        cv2.imwrite(filename, frame)
        print(f"Image saved as {filename}")
    else:
        print("Failed to capture image")

    # Release the camera
    cap.release()
    cv2.destroyAllWindows()

# Function to verify OTP
def verify_otp(entered_otp):
    global wrong_attempts

    if not entered_otp:
        messagebox.showerror("Error", "OTP field cannot be empty. Please enter the OTP.")
    elif entered_otp == generated_otp:
        otp_entry.config(state='disabled')
        block_button.config(state='normal')
        unblock_button.config(state='normal')
        messagebox.showinfo("Success", "OTP verified. You can now block or unblock USB drives.")
        wrong_attempts = 0  # Reset wrong attempts on successful verification
    else:
        wrong_attempts += 1
        if wrong_attempts >= max_attempts:
            capture_image()
            messagebox.showerror("Error", "Too many wrong attempts. Your image has been captured.")
            otp_entry.config(state='disabled')
            block_button.config(state='disabled')
            unblock_button.config(state='disabled')
        else:
            messagebox.showerror("Error", "Invalid OTP. Please try again.")

# Main application function
def main_app():
    if is_admin():
        # Setup the Tkinter window
        window = tk.Tk()
        window.title("USB Control Panel")
        window.geometry("400x350")
        window.configure(bg="#f5f5f5")

        # Create top frame with background
        top_frame = tk.Frame(window, bg="#2196F3", padx=20, pady=10)
        top_frame.pack(fill='x', pady=10)

        # Title label
        title_label = tk.Label(top_frame, text="Secure USB_Manager By Akash", bg="#2196F3", fg="white", font=('Arial', 18, 'bold'))
        title_label.pack(pady=5)

        # Create frames for main content
        content_frame = tk.Frame(window, bg="#f5f5f5", padx=20, pady=10)
        content_frame.pack(fill='both', expand=True)

        otp_frame = tk.Frame(content_frame, bg="#ffffff", padx=20, pady=10, bd=2, relief="solid")
        otp_frame.pack(fill='x', pady=10)

        buttons_frame = tk.Frame(content_frame, bg="#ffffff", padx=20, pady=10, bd=2, relief="solid")
        buttons_frame.pack(fill='x', pady=10)

        # OTP input field
        otp_label = tk.Label(otp_frame, text="Enter OTP:", bg="#ffffff", font=('Arial', 12, 'bold'))
        otp_label.pack(pady=5, anchor='w')
        
        global otp_entry
        otp_entry = tk.Entry(otp_frame, font=('Arial', 12), bd=2, relief="sunken")
        otp_entry.pack(pady=5, fill='x')

        # OTP verify button
        verify_button = tk.Button(otp_frame, text="Verify OTP", command=lambda: verify_otp(otp_entry.get()), bg="#4CAF50", fg="white", font=('Arial', 12, 'bold'), relief="raised")
        verify_button.pack(pady=10)

        # Block button
        global block_button
        block_button = tk.Button(buttons_frame, text="Block USB", state='disabled', command=block_usb, bg="#f44336", fg="white", font=('Arial', 12, 'bold'), relief="raised")
        block_button.pack(pady=10, fill='x')

        # Unblock button
        global unblock_button
        unblock_button = tk.Button(buttons_frame, text="Unblock USB", state='disabled', command=unblock_usb, bg="#4CAF50", fg="white", font=('Arial', 12, 'bold'), relief="raised")
        unblock_button.pack(pady=10, fill='x')

        # Send OTP button
        send_otp_button = tk.Button(buttons_frame, text="Send OTP", command=send_otp, bg="#2196F3", fg="white", font=('Arial', 12, 'bold'), relief="raised")
        send_otp_button.pack(pady=10, fill='x')

        # Run the Tkinter main loop
        window.mainloop()
    else:
        messagebox.showerror("Error", "This application requires administrative privileges. Please run it as an administrator.")

if __name__ == "__main__":
    main_app()
