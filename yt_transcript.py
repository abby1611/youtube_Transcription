import re, webvtt, os, youtube_dl, spacy
# import webvtt
from gensim.summarization.summarizer import summarize as gensim_based
from tkinter import *
from tkinter import filedialog
nlp = spacy.load("en_core_web_sm")

def get_caption(url):
    global video_title
    ydl_opts = {
        'skip_download': True,        # Skipping the download of actual file
        'writesubtitles': True,       # Uploaded Subtitles
        "writeautomaticsub": True,    # Auto generated Subtitles
        "subtitleslangs": ['en'],     # Language Needed "en"-->English
        'outtmpl': 'test.%(ext)s',    # Saving downloaded file as 'test.en.vtt'
        'nooverwrites': False,        # Overwrite if the file exists
        'quiet': True                # Printing progress
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None)
        except:
            print("Try with a YouTube URL")
    corpus = []
    for caption in webvtt.read('test.en.vtt'):
        corpus.append(caption.text)
    corpus = "".join(corpus)
    corpus = corpus.replace('\n', ' ')

    return corpus


def summarizer(text, frac):
    # if option == "TfIdf-Based":
    #     return tfidf_based(text, frac)
    # if option == "Frequency-Based":
    #     return freq_based(text, frac)
    # if option == "Gensim-Based":
        doc=nlp(text)
        text="\n".join([sent.text for sent in doc.sents])
        return gensim_based(text=text, ratio=frac)


root = Tk(baseName="Video Summarizer")
root.title("Caption Based Video Summarizer")
root.configure(background='#abc')
root.geometry("600x400+400+200")
root.resizable(0, 0)

# Main Title Label
title = Label(root, text="YT Transcript Summarizer", font="bold 24",
              bg="#abd", padx=140, pady=10).grid(row=0, column=0)

# URL Label
url_label = Label(root, text="URL:", font="bold",
                  bg='#abc', justify="right", bd=1)
url_label.place(height=50, x=100, y=70)

# Fraction Label
fraction_label = Label(root, text="Fraction:", font="bold",
                       bg='#abc', justify="right", bd=1)
fraction_label.place(height=50, x=80, y=140)

# Folder Label
folder_label = Label(root, text="Location:", font="bold",
                     bg='#abc', justify="right", bd=1)
folder_label.place(height=50, x=75, y=210)

# Entry --> String
get_url = Entry(root, width=40)
get_url.place(width=300, height=30, x=160, y=80)

# Entry --> Float
get_fraction = Entry(root, width=40)
get_fraction.place(width=300, height=30, x=160, y=150)

# Ask folder path
get_folder = Entry(root, width=40)
get_folder.place(width=300, height=30, x=160, y=220)

# Button --> Browse
folder = StringVar(root)


def browse():
    global folder
    folder = filedialog.askdirectory(initialdir='/')
    get_folder.insert(0, folder)


browse = Button(root, text="Browse", command=browse)
browse.place(height=30, x=475, y=220)


# Button Clear --> Reset all settings to default
def on_clear():
    get_url.delete(0, END)
    get_folder.delete(0, END)
    get_fraction.delete(0, END)


clear = Button(root, text="Clear", command=on_clear)
clear.place(width=100, x=200, y=300)
# Function on Submit


def on_submit():
    global url, choice, frac, current, folder
    url = get_url.get()
    frac = float(get_fraction.get())
    current = os.getcwd()
    folder = get_folder.get()
    os.chdir(folder)
    print(url,frac,folder)
    corpus = get_caption(url)
    with open("corpus.txt",'w+') as c:
        print(corpus,file=c)

    summary = summarizer(corpus, frac)
    filename = video_title+" gensim.txt"
    filename = re.sub(r'[\/:*?<>|]', ' ', filename)
    with open(filename, 'w+') as f:
        print(summary, file=f)
    os.remove(os.getcwd()+'\\test.en.vtt')
    os.chdir(current)
    openpath = Button(root, text="Open Folder",
                      command=lambda: os.startfile(get_folder.get()))
    openpath.place(x=360, y=350)


# Button -->Submit
submit = Button(root, text="Submit", command=on_submit)
submit.place(width=100, x=320, y=300)

# Button Open Folder to view Saved files

root.mainloop()
