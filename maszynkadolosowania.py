import requests
import json
import random
import tkinter as tk
import pymongo
from tkinter import filedialog, Text

fg_color = "#FFFFFF"
bg_color = '#000000'


CHANNEL = 'lewus'
client = pymongo.MongoClient(
    f"")
db = client.twitchsubs.channels
subs = []
search = db.find({"name": CHANNEL})
for res in search:
    for x in res['subs']:
        subs.append(x['user_name'])


def get_all_chatters(channel):
    url = f'http://tmi.twitch.tv/group/user/{channel.lower()}/chatters'
    try:
        all_chatters = requests.get(url).json()['chatters']
        chatters = all_chatters['staff'] + all_chatters['global_mods'] + all_chatters['admins'] \
                   + all_chatters['moderators'] + all_chatters['vips'] + all_chatters['viewers']
        chatters = sorted(chatters)
        return chatters
    except:
        print(channel)


chatters = get_all_chatters(CHANNEL)
subs_in_chat = list(set(subs) & set(chatters))


def get_random_viewer(list):
    return list[random.randint(0, len(list) - 1)]


def raffle():
    winner = get_random_viewer(chatters)
    label = tk.Label(text=winner, bg=bg_color, fg=fg_color)
    label.place(relx=0.5, rely=0.2, anchor='center')
    label.config(width=20, font=("Arial", 35))


def subraffle():
    winner = get_random_viewer(subs_in_chat)
    label = tk.Label(text=winner, bg=bg_color, fg=fg_color)
    label.place(relx=0.5, rely=0.2, anchor='center')
    label.config(width=20, font=("Arial", 35))


def submit():
    luck = sub_luck.get()
    global chatters
    chatters = list(set(chatters))
    for y in range(luck):
        for x in subs_in_chat:
            chatters.append(x)


root = tk.Tk()
sub_luck = tk.IntVar()

root.title('Maszynka do losowania')
canvas = tk.Canvas(root, height=800, width=800, bg=bg_color)
canvas.pack()
filename = tk.PhotoImage(file='vvarion.png')
background_label = tk.Label(root, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

losowanie = tk.Button(root, text="Losuj dla każdego", padx=10,
                      pady=5, fg=fg_color, bg=bg_color, command=raffle)
losowanie.place(relx=0.5, rely=0.6, anchor='center')
losowanie.config(width=20, font=("Arial", 35))

sublosowanie = tk.Button(root, text="Losuj dla subów", padx=10,
                         pady=5, fg=fg_color, bg=bg_color, command=subraffle)
sublosowanie.place(relx=0.5, rely=0.8, anchor='center')
sublosowanie.config(width=20, font=("Arial", 35))

sub_luck_entry = tk.Entry(root, textvariable=sub_luck, font=("Arial", 35))
sub_luck_entry.place(relx=0.7, rely=0.4, anchor='center')
sub_luck_entry.config(width=5, font=("Arial", 35))
sub_btn = tk.Button(root, text='Sub-Luck', command=submit, bg=bg_color, fg=fg_color)
sub_btn.place(relx=0.3, rely=0.4, anchor='center')
sub_btn.config(width=10, font=("Arial", 35))

root.mainloop()
