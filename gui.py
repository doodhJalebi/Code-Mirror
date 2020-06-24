"""Starting point for the application. Hosts the GUI."""
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
from os import listdir
import threading
from time import sleep

#----------------- GLOBAL VARIABLES ---------------------
SCREEN_WIDTH = 650
SCREEN_HEIGHT = 400
BACKGROUND_COLOR = '#0f0f0f'
BUTTON_BACKGROUND = '#1c1c1c'
BUTTON_FOREGROUND = 'white'



listboxA_data = ['rida.py', 'niha.dhakkan', 'bahzad.docx', 'owais.txt']
listboxB_data = ['rida.py', 'niha.dhakkan', 'bahzad.docx']

MIRRORING = False # False: program stopped | True: program running

global_settings = {
    'sync_frequency' : 5,
    'on_startup' : False,
    'src_folder' : '',
    'dst_folder' : ''
}

#--------------------- MIRROR LOGIC IN THREAD ------------------
def begin_mirror(global_settings, run):
    """Thread function that will start an event loop to check for changes in the MIRRORING flag and
    start/stop the process accordingly."""
    print(run())
    
    while True:
        
        if run():
            
            while True:
                sleep(1)
                print("Tick tock")
                
                if not run():
                    break
    

mirror_thread = threading.Thread(target=begin_mirror, args=(global_settings, (lambda : MIRRORING),), daemon=True)
mirror_thread.start()

#--------------------- BEGIN GUI -------------------------------

window = tk.Tk()
window.minsize(SCREEN_WIDTH, SCREEN_HEIGHT)
window.maxsize(SCREEN_WIDTH, SCREEN_HEIGHT)
window.title('Code Mirror')
window.iconphoto(True, tk.PhotoImage(file='icon2.png'))


#--------------- MAKESHIFT MENUBAR -----------------------
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

#---------------- BUTTON CALLBACK FUNCTIONS -----------------------------
def check_requirements():
    """Triggers the Mirroring process given all requirements have been fulfilled.
    
    Checks if all requirements for starting the mirroring process are present or not.
    If so, it will set the MIRRORING flag to true, indicating to an already running thread
    that it can begin the process in parallel to the GUI."""
    global MIRRORING

    if MIRRORING == False and global_settings['src_folder'] != '' and global_settings['dst_folder'] != '':
        # Mirroring isn't running. SRC and DST folders have been chosen. We can begin.
        start_stop_button.config(text='Stop')
        sync_status_image.config(image=syncing_image)
        src_button.config(state=tk.DISABLED)
        dst_button.config(state=tk.DISABLED)
        settings_button.config(state=tk.DISABLED)
        MIRRORING = True
        
        
    
    elif MIRRORING == True:
        # Stop mirroring.
        start_stop_button.config(text='Start')
        sync_status_image.config(image=stopped_image)
        src_button.config(state=tk.NORMAL)
        dst_button.config(state=tk.NORMAL)
        settings_button.config(state=tk.NORMAL)
        MIRRORING = False

def update_src_listbox():
    """Reads content of src folder and populates the listbox accordingly."""
    src_content = listdir(global_settings['src_folder'])
    
    for i in range(len(src_content)):
        if '.' not in src_content[i]:
            src_content[i] += '/'
        
        if len(src_content[i]) > 20:
            if '/' in src_content[i]:
                src_content[i] = src_content[i][:20]
                src_content[i] += '.../'
            
            elif '.' in src_content[i]:
                extension = src_content[i][src_content[i].index('.'):]
                src_content[i] = src_content[i][:20]
                src_content[i] += '...'
                src_content[i] += extension

    src_listbox.delete(0,tk.END)
    
    for item in src_content:
        src_listbox.insert(tk.END, item)

def update_dst_listbox():
    """Reads content of dst folder and populates the listbox accordingly."""
    dst_content = listdir(global_settings['dst_folder'])

    for i in range(len(dst_content)):
        if '.' not in dst_content[i]:
            dst_content[i] += '/'
        
        if len(dst_content[i]) > 20:
            if '/' in dst_content[i]:
                dst_content[i] = dst_content[i][:20]
                dst_content[i] += '.../'
            
            elif '.' in dst_content[i]:
                extension = dst_content[i][dst_content[i].index('.'):]
                dst_content[i] = dst_content[i][:20]
                dst_content[i] += '...'
                dst_content[i] += extension

    dst_listbox.delete(0,tk.END)
    for item in dst_content:
        dst_listbox.insert(tk.END, item)

def choose_src():
    """Opens the askdirectory dialog box to prompt the user to choose a src directory."""
    folder_selected = filedialog.askdirectory()
    global_settings['src_folder'] = folder_selected

    if folder_selected != '':
        update_src_listbox()

def choose_dst():
    """Opens the askdirectory dialog box to prompt the user to choose a dst directory."""
    folder_selected = filedialog.askdirectory()
    global_settings['dst_folder'] = folder_selected
    
    if folder_selected != '':
        update_dst_listbox()

def showAbout():
    """Initializes and sets up a new TopLevel widget with the 'About' information."""
    about_window = tk.Toplevel(window)
    about_window.minsize(300, 200)
    about_window.maxsize(300, 200)
    about_window.title('About')
    about_window.config(bg=BACKGROUND_COLOR)

    about_window.grab_set()

    heading_label = tk.Label(about_window, text='Code Mirror is a simple application that allows you to\nkeep two directories in sync!')
    heading_label.config(bg=BACKGROUND_COLOR, fg='white', font='Segoe 9 italic')
    heading_label.place(width=290, height=40, x=5, y=10)

    body_label = tk.Label(about_window, text="Designed & developed by:\n\nNiha Karim Momin\nOwais Bin Asad\nRida Zahid Khan\nBahzad Ahmed Badvi")
    body_label.config(bg=BACKGROUND_COLOR, fg='white', font='Segoe 9 italic')
    body_label.place(width=150, height=100, x=75, y=60)

def showSettings():
    """Initializes and sets up a new TopLevel widget prompting the user to change application settings."""
    settings_window = tk.Toplevel(window)
    settings_window.minsize(400, 200)
    settings_window.maxsize(400, 200)
    settings_window.title('Settings')
    settings_window.config(bg=BACKGROUND_COLOR)

    settings_window.grab_set()

    slider_label = tk.Label(settings_window, text='Sync after: (mins)')
    slider_label.place(width=100, height=15, x=10, y=60)
    slider_label.config(bg=BACKGROUND_COLOR, fg='white')

    slider = tk.Scale(settings_window, from_=1, to=30, orient=tk.HORIZONTAL)
    slider.place(width=200, height=50, x=190, y=40)
    slider.config(bg=BACKGROUND_COLOR, fg='white', highlightthickness=0, troughcolor=BUTTON_BACKGROUND, activebackground=BACKGROUND_COLOR)
    
    startup_label = tk.Label(settings_window, text='Run at startup:')
    startup_label.place(width=100, height=15, x=2, y=100)
    startup_label.config(bg=BACKGROUND_COLOR, fg='white')

    var1 = tk.IntVar()
    checkbox1 = tk.Checkbutton(settings_window, variable=var1)
    checkbox1.place(width=20, height=20, x=190, y=100)
    checkbox1.config(bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR)



    def settings_onclose():
        global_settings['sync_frequency'] = slider.get()
        global_settings['on_startup'] = bool(var1.get())
        settings_window.destroy()

    settings_window.protocol("WM_DELETE_WINDOW", settings_onclose)


#-----------------BUTTONS OF THE GUI-------------------------------------------------
src_button = tk.Button(frameC, text='Choose Source', command=choose_src)
src_button.place(width=120, height=40, x=40, y=10)

dst_button = tk.Button(frameC, text='Choose Destination', command=choose_dst)
dst_button.place(width=120, height=40, x=40, y=70)

settings_button = tk.Button(menubar_frame, text='Settings', command=showSettings)
settings_button.place(width=50, height=22, x=5, y=1)

about_button = tk.Button(menubar_frame, text='About', command=showAbout)
about_button.place(width=50, height=22, x=60, y=1)

start_stop_button = tk.Button(frameC, text='Start', command=check_requirements)
start_stop_button.place(width=120, height=40, x=40, y= 150)


#-------------------SYNC STATUS LABEL + IMAGE-------------------------------------
sync_status_label = tk.Label(frameC, text='Sync Status:', anchor='w', padx=8)
sync_status_label.place(width=120, height=25, x=40, y=235)

sync_label_tick = Image.open("tick.png").resize((20, 20), Image.ANTIALIAS)
tick_image = ImageTk.PhotoImage(sync_label_tick)

sync_label_syncing = Image.open("syncing.png").resize((20, 20), Image.ANTIALIAS)
syncing_image = ImageTk.PhotoImage(sync_label_syncing)

sync_label_stopped = Image.open("stopped.png").resize((20, 20), Image.ANTIALIAS)
stopped_image = ImageTk.PhotoImage(sync_label_stopped)

sync_status_image = tk.Label(sync_status_label, image=stopped_image)
sync_status_image.place(width=20, height=20, x=90, y=0)





#----------------------SOURCE AND DESTINATION FOLDER LISTBOXES-------------------------------
src_listbox = tk.Listbox(frameA)
src_listbox.place(width=180, height=250, x=10, y=10)
src_listbox.config(justify=tk.CENTER)


src_label = tk.Label(frameA, text='Source Folder')
src_label.place(width=120, height=20, x=40, y=270)


dst_listbox = tk.Listbox(frameB)
dst_listbox.place(width=180, height=250, x=10, y=10)
dst_listbox.config(justify=tk.CENTER)


dst_label = tk.Label(frameB, text='Destination Folder')
dst_label.place(width=120, height=20, x=40, y=270)


#----------------------------- COLORING ----------------------------------------#
window.config(bg=BACKGROUND_COLOR)
frameA.config(bg=BACKGROUND_COLOR)
frameB.config(bg=BACKGROUND_COLOR)
frameC.config(bg=BACKGROUND_COLOR)

src_button.config(bg=BUTTON_BACKGROUND, fg=BUTTON_FOREGROUND, activebackground=BUTTON_BACKGROUND, activeforeground=BUTTON_FOREGROUND, highlightbackground=BACKGROUND_COLOR, highlightcolor=BACKGROUND_COLOR)
dst_button.config(bg=BUTTON_BACKGROUND, fg=BUTTON_FOREGROUND, activebackground=BUTTON_BACKGROUND, activeforeground=BUTTON_FOREGROUND, highlightbackground=BACKGROUND_COLOR, highlightcolor=BACKGROUND_COLOR)

start_stop_button.config(bg=BUTTON_BACKGROUND, fg=BUTTON_FOREGROUND, activebackground=BUTTON_BACKGROUND, activeforeground=BUTTON_FOREGROUND, highlightbackground=BACKGROUND_COLOR, highlightcolor=BACKGROUND_COLOR)

sync_status_label.config(bg=BUTTON_BACKGROUND, fg=BUTTON_FOREGROUND)

src_listbox.config(bg=BUTTON_BACKGROUND, fg=BUTTON_FOREGROUND, relief=tk.FLAT, highlightbackground=BACKGROUND_COLOR, highlightcolor=BACKGROUND_COLOR)
dst_listbox.config(bg=BUTTON_BACKGROUND, fg=BUTTON_FOREGROUND, relief=tk.FLAT, highlightbackground=BACKGROUND_COLOR, highlightcolor=BACKGROUND_COLOR)

menubar_frame.config(bg=BACKGROUND_COLOR)

settings_button.config(bg=BACKGROUND_COLOR, fg='white', relief=tk.FLAT, activebackground=BACKGROUND_COLOR, activeforeground='white')
about_button.config(bg=BACKGROUND_COLOR, fg='white', relief=tk.FLAT, activebackground=BACKGROUND_COLOR, activeforeground='white')

src_label.config(bg=BACKGROUND_COLOR, fg='white')
dst_label.config(bg=BACKGROUND_COLOR, fg='white')


#----- Mainloop ------
window.mainloop()