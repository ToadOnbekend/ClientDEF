import requests
import os
from time import sleep
import threading
from getkey import keys, getkey
refresh = True
refresh_type = False
typed = ""
cursor = " "
chat_now = ""
id_m = "User"
c = lambda: print("\033c", end = "");c();print("\033[?25l")


def get_chat():
    param = {"id": id_m}
    response = requests.get('https://1ae9d23e-dad4-4a1a-b79e-30aceffac1d7-00-173gl8hww801.kirk.replit.dev/get_chat', json=param)
    content = response.json()['result']
    return content

def load_to_print(chat_content):
    global chat_now
    to_display = ""
    for i in range(len(chat_content["chat"]["messages"])):
       to_display += f"\033[1m{chat_content['chat']['senders'][i]:>5}\033[0m \033[34m——\033[0m \033[3m{chat_content['chat']['messages'][i]}\033[0m\n"
    if to_display == chat_now:
       return False
    else:
       chat_now = to_display
       return True

def send_to_server(message, id):
   global refresh
   global typed
   send_to_server = {"id": id, "message":message}
   response_s = requests.post('https://1ae9d23e-dad4-4a1a-b79e-30aceffac1d7-00-173gl8hww801.kirk.replit.dev/send_message', json=send_to_server)
   print("\n"+response_s.json()["result"])

def update_screen():
    global refresh, chat_now

    while True:
        try:
           update_ = load_to_print(get_chat())
        except:
           chat_now = "\033[31m  ! NOT able to retrive chat\033[0m" 
           update_ = True
        refresh = update_
        sleep(0.4)


try:
   load_to_print(get_chat())    
except:
   chat_now = "\033[31m  ! NOT able to retrive chat\033[0m" 

def get_input():
    global typed, refresh_type, chat_now
    while True:
        k = getkey();

        if k in [keys.UP, keys.DOWN, keys.LEFT, keys.RIGHT]:
            pass
        elif k in keys.BACKSPACE:
           refresh_type= True
           typed = typed[:-1]
        elif k in keys.ENTER:
            refresh_type= True
            try:
                 send_to_server(typed, id_m)
                 typed = ""
            except:
                typed = "\033[31m  ! NOT able to send message\033[0m" 

        else:
           typed += k 
           refresh_type= True



t1 = threading.Thread(target=get_input)
t2 = threading.Thread(target=update_screen)
t1.start()
t2.start()
while True:
    if refresh:
       c()
       print(chat_now+"\n\033[4m                                     \033[0m\n\033[1mType your message\033[0m \n"+typed+cursor, end = "\r")
       refresh = False 
    if refresh_type:
       print(typed + cursor, end = "\r")
       refresh_type = False
    else:
       sleep(0.001)

