import os
import tkinter as tk
from tkinter import ttk
import PIL.Image as PilImage
import PIL.ImageTk as PilImageTk
import requests
from io import BytesIO
import spotipy
import pyperclip
import threading
from spotipy.oauth2 import SpotifyOAuth
from lyricsgenius import Genius
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from dotenv import load_dotenv
from googletrans import Translator


load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('CLIENT_ID'), client_secret=os.getenv('CLIENT_SECRET'), redirect_uri=os.getenv('REDIRECT_URL'), scope="user-read-currently-playing"))

root = tk.Tk()
root.iconbitmap("C:\PR\GetLyrics\logo.ico")
root.configure(bg="#2b2b2b")

LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'he': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
    }

translator = Translator()

lang_list = []
for key,value in LANGUAGES.items():
    lang_list.append(value)


    labelArtistName = tk.Label(root, bg="#2b2b2b", fg="white", font=('Consolas',13,'bold'))
    labelSongName = tk.Label(root, bg="#2b2b2b", fg="white", font=('Consolas',13,'bold'))

def getSongImg(artist, songName, song):

    response = requests.get(song.header_image_url)
    img_data = response.content

    img = PilImage.open(BytesIO(img_data))

    img = img.resize((120,120))

    tk_img = PilImageTk.PhotoImage(img)
    labelImg = tk.Label(root, image=tk_img)
    labelImg.image = tk_img
    labelImg.place(x=70, y=650)


    labelArtistName.config(text=artist)
    labelArtistName.place(x=65, y=780)

    labelSongName.config(text=songName)
    labelSongName.place(x=65, y=805)


def get_lyrics(artist, songName):
    try:
        lyrics_textbox.configure(state="normal")
        lyrics_textbox.delete("1.0", END)
        lyrics_translate.delete("1.0", END)
        genius = Genius(os.getenv("GENIUS_TOKEN"))
        song = genius.search_song(artist, songName)
        if song is None:
            messagebox.showerror("Get Lyrics","No results found!")
            return
        getSongImg(song.artist, song.title, song)
        lyrics_textbox.insert(END,song.lyrics)
        lyrics_textbox.configure(state="disabled")
    except:
        messagebox.showerror("Get Lyrics","No results found! (Make sure you are not connected to a VPN.)")
        


def setCenter(window, width, height):

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2 
    y = (screen_height - height) //2 
    
    window.geometry(f"{width}x{height}+{x}+{y}")


def getManuelLyrics(artist, song):
    try:
        def getManuelLyrics():
            getLoadingWindow(root)
            get_lyrics(artist, song)
            removeLoadingWindow()

    except:
        messagebox.showerror("Get Lyrics","No results found! (Make sure you are not connected to a VPN.)")

    threading.Thread(target=getManuelLyrics).start()

def manuel_get_lyrics():
    manuel = Toplevel(root)
    setCenter(manuel, width=240, height=180)
    manuel.iconbitmap("C:\PR\GetLyrics\logo.ico")
    manuel.grab_set()
    manuel.config(bg="#2b2b2b")
    manuel.resizable(False,False)

    tk.Label(manuel, text="", height=1, bg="#2b2b2b").pack()

    artist_label = tk.Label(manuel, text="Artist", bg="#2b2b2b", fg="white")
    artist_entry = tk.Entry(manuel, width=30)

    artist_label.pack()
    artist_entry.pack()

    song_name_label = tk.Label(manuel, text="Song Name", bg="#2b2b2b", fg="white")
    song_name_entry = tk.Entry(manuel, width=30)

    song_name_label.pack()
    song_name_entry.pack() 

    search_button = tk.Button(manuel, font=('Ebrima',10), padx=10, pady=10, text="Search", relief="flat", bg="#1c1c1c", fg="white", bd=0, highlightthickness=0, command= lambda: getManuelLyrics(artist_entry.get(), song_name_entry.get()))
    search_button.pack(pady=10)

    search_button.bind("<Enter>", lambda e: search_button.config(bg="white", fg="#1c1c1c"))
    search_button.bind("<Leave>", lambda e: search_button.config(bg="#1c1c1c", fg="white"))

loading = None

def getLoadingWindow(window):
    def getLoading():       
        global loading
        loading = Toplevel(window)
        setCenter(loading, width=240, height=180)
        loading.overrideredirect(True)
        loading.grab_set()
        loading.config(bg="#2b2b2b")
        loading.resizable(False,False)
        loading_label = tk.Label(loading, text="Loading...", bg="#2b2b2b", fg="white", pady=70, font=('Consolas',12,'bold'))
        loading_label.pack()
    window.after(50, getLoading)

def removeLoadingWindow():
    global loading
    if loading is not None:
        loading.destroy()
        loading = None

def get_spotify_current_song():
    artist = sp.currently_playing()["item"]["album"]["artists"][0]["name"]
    song_name = sp.currently_playing()["item"]["name"]
    return artist, song_name

def get_spotify_lyrics():
    try:
        def getLyrics():
            getLoadingWindow(root)
            get_lyrics(get_spotify_current_song()[0], get_spotify_current_song()[1])
            removeLoadingWindow()

    except:
        messagebox.showerror("Get Lyrics","No results found! (Make sure you are not connected to a VPN.)")

    threading.Thread(target=getLyrics).start()

        

def scroll1(first, last):
    lyrics_translate.yview_moveto(first)

def scroll2(first, last):
    lyrics_textbox.yview_moveto(first)

def translate(lang):
    lyrics_translate.configure(state="normal")
    lyrics_translate.delete("1.0", END)
    for key, value in LANGUAGES.items():
        if lang == value:
            src = key
            break

    def translate_lyrics():
        getLoadingWindow(root)
        translated = translator.translate(lyrics_textbox.get("1.0",END), src=translator.detect(lyrics_textbox.get("1.0",END)).lang, dest=lang).text
        lyrics_translate.insert(END,translated)
        lyrics_translate.configure(state="disabled")
        removeLoadingWindow()


    threading.Thread(target=translate_lyrics).start()

textbox_frame = Frame(root, bg="#2b2b2b", cursor="arrow black")
textbox_frame.pack()
lyrics_textbox = tk.Text(textbox_frame, width=50, padx=10, pady=20, cursor="arrow")
lyrics_textbox.configure(state="disabled", bg="#444444", fg="white", bd=0, font=('Consolas',15,'bold'))
lyrics_textbox.grid(row=0, column=0, padx=15, pady=25)


def copy_text(text):
    pyperclip.copy(text)

popup_lyrics = Menu(root, tearoff = 0)
popup_lyrics.add_command(label ="Copy", command= lambda: copy_text(lyrics_textbox.get("1.0",END)))

  
def do_popup_lyrics(event):
    try:
        popup_lyrics.tk_popup(event.x_root, event.y_root)
    finally:
        popup_lyrics.grab_release()

lyrics_textbox.bind("<Button-3>", do_popup_lyrics)


lyrics_translate = tk.Text(textbox_frame, width=50, padx=20, pady=20, cursor="arrow")
lyrics_translate.configure(state="disabled", bg="#444444", fg="white", bd=0, font=('Consolas',15,'bold'))
lyrics_translate.grid(row=0, column=1)


popup_translated = Menu(root, tearoff = 0)
popup_translated.add_command(label ="Copy", command= lambda: copy_text(lyrics_translate.get("1.0",END)))

  
def do_popup_translated(event):
    try:
        popup_translated.tk_popup(event.x_root, event.y_root)
    finally:
        popup_translated.grab_release()

lyrics_translate.bind("<Button-3>", do_popup_translated)

button_frame = Frame(root, bg="#2b2b2b")
button_frame.pack()


manuel_search = tk.Button(button_frame, bd=0, font=('Ebrima',10), padx=10, pady=10, text="Manuel Search", relief="flat", bg="#1c1c1c", fg="white",  command=manuel_get_lyrics)
manuel_search.grid(row=1, column=0, padx=20)

manuel_search.bind("<Enter>", lambda e: manuel_search.config(bg="white", fg="#1c1c1c"))
manuel_search.bind("<Leave>", lambda e: manuel_search.config(bg="#1c1c1c", fg="white"))

get_spotify_song = tk.Button(button_frame, bd=0, font=('Ebrima',10), padx=10, pady=10, text="Get Current Track", relief="flat", bg="#1c1c1c", fg="white", command=get_spotify_lyrics)
get_spotify_song.grid(row=1, column=1)

get_spotify_song.bind("<Enter>", lambda e: get_spotify_song.config(bg="white", fg="#1c1c1c"))
get_spotify_song.bind("<Leave>", lambda e: get_spotify_song.config(bg="#1c1c1c", fg="white"))


translate_frame = Frame(root, pady=20, bg="#2b2b2b")
translate_frame.pack()

style = ttk.Style()

style.theme_use("clam")
style.configure("Lang.TCombobox", fieldbackground="#1c1c1c", background="#1c1c1c", foreground="black", borderwidth=0, padding=5)
style.map("Lang.TCombobox", fieldbackground=[("readonly", "#1c1c1c")], foreground=[("readonly", "white")])

lang = ttk.Combobox(translate_frame, font=('Ebrima',10), values=lang_list, state="readonly", style="Lang.TCombobox")
lang.current(0)
lang.grid(row=2, column=0)

translate_button = tk.Button(translate_frame, font=('Ebrima',10), bd=0, padx=5, pady=7, text="Translate", relief="flat", bg="#1c1c1c", fg="white", command= lambda: translate(lang.get()))
translate_button.grid(row=3, column=0, pady=8)

translate_button.bind("<Enter>", lambda e: translate_button.config(bg="white", fg="#1c1c1c"))
translate_button.bind("<Leave>", lambda e: translate_button.config(bg="#1c1c1c", fg="white"))




lyrics_textbox.configure(yscrollcommand=scroll1)
lyrics_translate.configure(yscrollcommand=scroll2)



setCenter(root, width=1300, height=850)
root.title("Get Lyrics")
root.resizable(False,False) 
root.mainloop()




