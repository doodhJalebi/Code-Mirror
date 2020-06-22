"""Starting point for the application. Hosts the GUI."""
import tkinter as tk
from PIL import Image, ImageTk

SCREEN_WIDTH = 650
SCREEN_HEIGHT = 400
BACKGROUND_COLOR = '#0f0f0f'
BUTTON_BACKGROUND = '#1c1c1c'
BUTTON_FOREGROUND = 'white'
listboxA_data = ['rida.py', 'niha.dhakkan', 'bahzad.docx', 'owais.txt']
listboxB_data = ['rida.py', 'niha.dhakkan', 'bahzad.docx']



##### BEGIN GUI

window = tk.Tk()
window.minsize(SCREEN_WIDTH, SCREEN_HEIGHT)
window.maxsize(SCREEN_WIDTH, SCREEN_HEIGHT)
window.title('Code Mirror')
#window.attributes('-transparentcolor', 'white')

# Menubar frame
menubar_frame = tk.Frame(window, height=25, width=650)
menubar_frame.pack()

main_frame = tk.Frame(window, height=400, width=600)
main_frame.pack(pady=10)

frameA = tk.Frame(main_frame, height=300, width=200)
frameB = tk.Frame(main_frame, height=300, width=200)
frameC = tk.Frame(main_frame, height=300, width=200)

frameA.pack(side=tk.LEFT, fill=tk.BOTH)
frameB.pack(side=tk.LEFT, fill=tk.BOTH)
frameC.pack(side=tk.LEFT, fill=tk.BOTH)


def showAbout():
    about_window = tk.Tk()
    about_window.minsize(300, 200)
    about_window.maxsize(300, 200)
    about_window.title('Settings')
    about_window.config(bg=BACKGROUND_COLOR)


src_button = tk.Button(frameC, text='Choose Source')
src_button.place(width=120, height=40, x=40, y=10)

dst_button = tk.Button(frameC, text='Choose Destination')
dst_button.place(width=120, height=40, x=40, y=70)

settings_button = tk.Button(menubar_frame, text='Settings')
settings_button.place(width=50, height=22, x=5, y=1)

about_button = tk.Button(menubar_frame, text='About', command=showAbout)
about_button.place(width=50, height=22, x=60, y=1)


sync_status_label = tk.Label(frameC, text='Sync Status:', anchor='w', padx=8)
sync_status_label.place(width=120, height=40, x=40, y=250)

sync_label_tick = Image.open("tick.png").resize((20, 20), Image.ANTIALIAS)
tick_image = ImageTk.PhotoImage(sync_label_tick)

sync_label_syncing = Image.open("syncing.png").resize((20, 20), Image.ANTIALIAS)
syncing_image = ImageTk.PhotoImage(sync_label_syncing)

sync_status_image = tk.Label(sync_status_label, image=syncing_image)
sync_status_image.place(width=20, height=20, x=90, y=7)


src_listbox = tk.Listbox(frameA)
src_listbox.place(width=180, height=250, x=10, y=10)
src_listbox.config(justify=tk.CENTER)

for item in listboxA_data:
    src_listbox.insert(tk.END, item)

src_label = tk.Label(frameA, text='Source Folder')
src_label.place(width=120, height=20, x=40, y=270)


dst_listbox = tk.Listbox(frameB)
dst_listbox.place(width=180, height=250, x=10, y=10)
dst_listbox.config(justify=tk.CENTER)

for item in listboxB_data:
    dst_listbox.insert(tk.END, item)

dst_label = tk.Label(frameB, text='Destination Folder')
dst_label.place(width=120, height=20, x=40, y=270)


############# COLORING ##############
window.config(bg=BACKGROUND_COLOR)
frameA.config(bg=BACKGROUND_COLOR)
frameB.config(bg=BACKGROUND_COLOR)
frameC.config(bg=BACKGROUND_COLOR)

src_button.config(bg=BUTTON_BACKGROUND, fg=BUTTON_FOREGROUND, activebackground=BUTTON_BACKGROUND, activeforeground=BUTTON_FOREGROUND, highlightbackground=BACKGROUND_COLOR, highlightcolor=BACKGROUND_COLOR)
dst_button.config(bg=BUTTON_BACKGROUND, fg=BUTTON_FOREGROUND, activebackground=BUTTON_BACKGROUND, activeforeground=BUTTON_FOREGROUND, highlightbackground=BACKGROUND_COLOR, highlightcolor=BACKGROUND_COLOR)

sync_status_label.config(bg=BUTTON_BACKGROUND, fg=BUTTON_FOREGROUND)

src_listbox.config(bg=BUTTON_BACKGROUND, fg=BUTTON_FOREGROUND, relief=tk.FLAT, highlightbackground=BACKGROUND_COLOR, highlightcolor=BACKGROUND_COLOR)
dst_listbox.config(bg=BUTTON_BACKGROUND, fg=BUTTON_FOREGROUND, relief=tk.FLAT, highlightbackground=BACKGROUND_COLOR, highlightcolor=BACKGROUND_COLOR)

menubar_frame.config(bg=BACKGROUND_COLOR)

settings_button.config(bg=BACKGROUND_COLOR, fg='white', relief=tk.FLAT, activebackground=BACKGROUND_COLOR, activeforeground='white')
about_button.config(bg=BACKGROUND_COLOR, fg='white', relief=tk.FLAT, activebackground=BACKGROUND_COLOR, activeforeground='white')

src_label.config(bg=BACKGROUND_COLOR, fg='white')
dst_label.config(bg=BACKGROUND_COLOR, fg='white')

window.mainloop()