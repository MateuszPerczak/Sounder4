from tkinter import Tk, Frame, Label, PhotoImage, Radiobutton, Button, StringVar, Canvas, Scrollbar, ttk, Entry, Toplevel
from tkinter.filedialog import askdirectory
from logging import basicConfig, error, ERROR, getLevelName, getLogger, shutdown
from typing import ClassVar
from os import getcwd, listdir, startfile
from os.path import basename, isfile, isdir, splitext, abspath, join
from PIL import Image, ImageTk
from json import dump, load
from mutagen.mp3 import MP3
from io import BytesIO
from random import shuffle
from datetime import timedelta
from re import findall
from pygame import mixer
from threading import Thread, active_count
from time import sleep
from webbrowser import open as open_browser

class App:
    def __init__(self):
        # logging error messages
        basicConfig(filename=f"{getcwd()}\\errors.log", level=ERROR)
        # create window
        self.main_window: ClassVar = Tk()
        # hide window
        self.main_window.withdraw()
        self.main_window.minsize(678, 500)
        self.main_window.iconbitmap('icons\\icon.ico')
        self.main_window.title('SOUNDER')
        self.main_window.configure(background='#212121')
        # app style
        self.main_theme: ClassVar = ttk.Style()
        self.main_theme.theme_use('clam')
        self.main_theme.configure('TButton', background='#111', relief='flat', font=('corbel', 20), foreground='#fff')
        self.main_theme.map('TButton', background=[('pressed', '!disabled', '#111'), ('active', '#151515')])
        self.main_theme.configure('error.TButton', background='#212121', relief='flat', font=('corbel', 20), foreground='#fff')
        self.main_theme.map('error.TButton', background=[('pressed', '!disabled', '#151515'), ('active', '#333')])
        self.main_theme.configure('folder.TButton', background='#111', relief='flat', font=('corbel', 12), foreground='#fff')
        self.main_theme.map('folder.TButton', background=[('pressed', '!disabled', '#111'), ('active', '#151515')])
        self.main_theme.configure('shuffle.TButton', background='#212121', relief='flat', font=('corbel', 12), foreground='#fff')
        self.main_theme.map('shuffle.TButton', background=[('pressed', '!disabled', '#151515'), ('active', '#212121')])
        self.main_theme.layout('Vertical.TScrollbar',[('Vertical.Scrollbar.trough', {'children': [('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})], 'sticky': 'ns'})])
        self.main_theme.configure('Vertical.TScrollbar', gripcount=0, relief='flat', background='#212121', darkcolor='#212121', lightcolor='#212121', troughcolor='#212121', bordercolor='#212121', arrowcolor='#212121')
        self.main_theme.map('Vertical.TScrollbar', background=[('pressed', '!disabled', '#333'), ('disabled', '#212121'), ('active', '#111'), ('!active', '#111')])
        self.main_theme.map('TScale', background=[('pressed', '!disabled', '#212121'), ('active', '#333')])
        self.main_theme.configure('TScale', troughcolor='#111', background='#212121', relief="flat", gripcount=0, darkcolor="#111", lightcolor="#111", bordercolor="#111")
        # end
        # frames
        self.error_frame: ClassVar = Frame(self.main_window, background='#212121')
        self.main_frame: ClassVar = Frame(self.main_window, background='#212121')
        self.select_frame: ClassVar = Frame(self.main_frame, background='#111')
        self.content_frame: ClassVar = Frame(self.main_frame, background='#212121')
        self.settings_frame: ClassVar = Frame(self.content_frame, background='#212121')
        self.playback_frame: ClassVar = Frame(self.content_frame, background='#212121')
        self.folder_frame: ClassVar = Frame(self.content_frame, background='#212121')
        self.playlist_frame: ClassVar = Frame(self.content_frame, background='#212121')
        self.error_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.main_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.select_frame.pack(side='top', fill='x', ipady=25)
        self.content_frame.pack(side='left', fill='both', expand=True)
        self.settings_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.playback_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.playlist_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.folder_frame.place(x=0, y=0, relwidth=1, relheight=1)
        # end
        # variables
        self.selected: StringVar = StringVar()
        self.settings: dict = {}
        self.songs: list = []
        self.playlist: list = []
        self.active_card: list = []
        self.volume: float = 0.0
        self.song: str = ""
        self.paused: bool = False
        # on load
        self.load_images()
        # error_frame
        Label(self.error_frame, image=self.warning_icon, text='Something went wrong', compound='top', font=('corbel', 35), background='#212121', foreground='#fff', anchor='center', justify='center').place(relx=0.5, rely=0.35, anchor='center', height=250)
        self.error_reason: ClassVar = Label(self.error_frame, text='', font=('corbel', 20), background='#212121', foreground='#e74c3c', anchor='center', justify='center')
        ttk.Button(self.error_frame, image=self.bug_icon, text=' Report a bug', compound='left', style='error.TButton', takefocus=False, command=lambda: open_browser('https://github.com/losek1/PySpec/issues', new=0, autoraise=True)).place(relx=0.7, rely=0.96, anchor='s')
        ttk.Button(self.error_frame, image=self.logs_icon, text=' Open logs', compound='left', style='error.TButton', takefocus=False, command=self.open_logs).place(relx=0.3, rely=0.96, anchor='s')
        self.error_reason.place(relx=0.5, rely=0.64, anchor='s')
        # end
        # load settings
        self.load_settings()
        # init player
        self.init_mixer()
        # select frame
        Radiobutton(self.select_frame, relief='flat', image=self.music_icon, indicatoron=False, bd=0, background='#111', selectcolor='#212121', takefocus=False,
                    highlightbackground='#222', activebackground='#222', variable=self.selected, value='playback', command=self.switch_frame).place(x=0, y=0, width=52, relheight=1)
        Radiobutton(self.select_frame, image=self.playlist_icon, relief='flat', indicatoron=False, bd=0, background='#111', selectcolor='#212121', takefocus=False,
                    highlightbackground='#222', activebackground='#222', variable=self.selected, value='playlist', command=self.switch_frame).place(x=52, y=0, width=52, relheight=1)
        Radiobutton(self.select_frame, image=self.music_folder_icon, relief='flat', indicatoron=False, bd=0, background='#111', selectcolor='#212121', takefocus=False,
                    highlightbackground='#222', activebackground='#222', variable=self.selected, value='folder', command=self.switch_frame).place(x=104, y=0, width=52, relheight=1)
        Radiobutton(self.select_frame, image=self.settings_icon, indicatoron=False, bd=0, background='#111', selectcolor='#212121', takefocus=False, highlightbackground='#222',
                    activebackground='#222', variable=self.selected, value='settings', command=self.switch_frame).place(relx=1, rely=1, width=52, relheight=1, anchor='se')
        # end
        # playback frame
        self.album_name: ClassVar = Label(self.playback_frame, text='ALBUM NAME', font=('Consolas', 15), compound='left', background='#212121', foreground='#fff', anchor='center', justify='center')
        self.cover_art: ClassVar = Label(self.playback_frame, image=self.cover_art_icon, background='#111')
        self.song_name: ClassVar = Label(self.playback_frame, text='SONG TITLE\nARTIST NAME', font=('Consolas', 15), background='#212121', foreground='#fff', anchor='center', justify='center')
        # bottom frame
        self.bottom_frame: ClassVar = Frame(self.playback_frame, background='#111')
        # buttons frame
        self.buttons_frame: ClassVar = Frame(self.bottom_frame, background='#111')
        # play button
        self.play_button: ClassVar = ttk.Button(self.buttons_frame, image=self.play_icon, takefocus=False, command=self.action_play)
        self.play_button.place(relx=0.5, rely=0.5, anchor='center')
        # next button
        self.next_button: ClassVar = ttk.Button(self.buttons_frame, image=self.next_icon, takefocus=False, command=self.action_next)
        self.next_button.place(relx=0.7, rely=0.5, anchor='center')
        # previous button
        self.previous_button: ClassVar = ttk.Button(self.buttons_frame, image=self.previous_icon, takefocus=False, command=self.action_prev)
        self.previous_button.place(relx=0.3, rely=0.5, anchor='center')
        # shuffle button
        self.shuffle_button: ClassVar = ttk.Button(self.buttons_frame, image=self.shuffle_icon, takefocus=False, command=self.toggle_shuffle)
        self.shuffle_button.place(relx=0.1, rely=0.5, anchor='center')
        # repeat button
        self.repeat_button: ClassVar = ttk.Button(self.buttons_frame, image=self.repeat_icon, takefocus=False, command=self.toggle_repeat)
        self.repeat_button.place(relx=0.9, rely=0.5, anchor='center')
        # scale frame
        self.scale_frame: ClassVar = Frame(self.bottom_frame, background='#111')
        # time passed
        self.time_passed: ClassVar = Label(self.scale_frame, text='--:--', font=('Consolas', 9), compound='left', background='#111', foreground='#fff', anchor='center', justify='center')
        self.time_passed.pack(side='left', ipadx=6)
        # scale bar
        self.scale_bar: ClassVar = ttk.Scale(self.scale_frame, orient='horizontal', from_=0, to=100)
        self.scale_bar.pack(side='left', fill='x', expand=True)
        # song length
        self.song_length: ClassVar = Label(self.scale_frame, text='--:--', font=('Consolas', 9), compound='left', background='#111', foreground='#fff', anchor='center', justify='center')
        self.song_length.pack(side='right', ipadx=6)
        # volume frame
        self.volume_frame: ClassVar = Frame(self.bottom_frame, background='#111')
        # volume button
        self.mute_button: ClassVar = ttk.Button(self.volume_frame, image=self.no_audio_icon, takefocus=False, command=self.toggle_volume)
        self.mute_button.pack(side='left', anchor='center', padx=5)
        # volume bar
        self.volume_bar: ClassVar = ttk.Scale(self.volume_frame, orient='horizontal', from_=0, to=1, command=self.change_volume)
        self.volume_bar.pack(side='left', anchor='center', padx=5, fill='x', expand=True)
        # place widgets
        self.scale_frame.place(relx=0.5, y=68, relwidth=0.9, height=20, anchor='n')
        self.buttons_frame.place(relx=0.5, y=10, width=350, height=48, anchor='n')
        self.volume_frame.place(relx=1, y=10, relwidth=0.22, height=48, anchor='ne')
        self.bottom_frame.place(relx=0.5, rely=1, relwidth=1, height=90, anchor='s')
        self.song_name.place(relx=0.5, rely=0.72, anchor='center')
        self.cover_art.place(relx=0.5, rely=0.4, anchor='center')
        self.album_name.place(relx=0.5, rely=0.08, anchor='center')
        # end
        # folder frame
        self.folder_top_frame: ClassVar = Frame(self.folder_frame, background='#212121')
        # top buttons
        ttk.Button(self.folder_top_frame, image=self.plus_icon, text='ADD FOLDER', style='folder.TButton', compound='left', takefocus=False, command=self.add_folder).place(x=10, rely=0.5, anchor='w')
        ttk.Button(self.folder_top_frame, image=self.refresh_icon, text='REFRESH', style='folder.TButton', compound='left', takefocus=False, command=self.refresh_folder).place(x=147, rely=0.5, anchor='w')
        ttk.Button(self.folder_top_frame, image=self.refresh_icon, text='START SCAN', style='folder.TButton', compound='left', takefocus=False, command=self.scan_for_songs).place(x=280, rely=0.5, anchor='w')
        #pack frame
        self.folder_top_frame.pack(side='top', fill='x', ipady=20, pady=10)
        # scrollbar
        self.folder_scrollbar: ClassVar = ttk.Scrollbar(self.folder_frame)
        # canvas
        self.folder_canvas: ClassVar = Canvas(self.folder_frame, borderwidth=0, highlightthickness=0, background='#212121', yscrollcommand=self.folder_scrollbar.set)
        self.folder_scrollbar.configure(command=self.folder_canvas.yview)
        # frame for items
        self.folder_cards: ClassVar = Frame(self.folder_canvas, background='#212121')
        # add folders
        self.scan_for_folders()
        # update canvas
        self.folder_cards.bind('<Configure>', lambda _: self.folder_canvas.configure(scrollregion=self.folder_canvas.bbox('all')))
        self.folder_window: ClassVar = self.folder_canvas.create_window((0, 0), window=self.folder_cards, anchor='nw')
        self.folder_canvas.bind('<Configure>', lambda _: self.folder_canvas.itemconfigure(self.folder_window, width=self.folder_canvas.winfo_width(), height=len(self.settings['folders']) * 70))
        # pack canvas
        self.folder_scrollbar.pack(side='right', fill='y', pady=(0, 10))
        self.folder_canvas.pack(side='left', fill='both',expand=True, padx=10, pady=(0, 10))
        # end
        # playlist
        self.playlist_top_frame: ClassVar = Frame(self.playlist_frame, background='#212121')
        # validate entry
        validator = (self.main_window.register(self.validate_entry), '%S', '%i')
        # entry
        self.search_box: ClassVar = Entry(self.playlist_top_frame, validate="key", validatecommand=validator, exportselection=0, border=0, insertbackground='#fff', selectbackground='#333', selectforeground='#fff', background='#111', foreground='#fff', font=('Consolas', 16))
        self.search_box.place(x=10, rely=0.5, height=35, width=230, anchor='w')
        # search button
        ttk.Button(self.playlist_top_frame, image=self.search_icon, style='folder.TButton', takefocus=False,command=self.search_song).place(x=240, rely=0.5, anchor='w', height=35, width=35)
        # play all button
        self.playlist_play: ClassVar = ttk.Button(self.playlist_top_frame, image=self.play_playlist, text='PLAY ALL', style='folder.TButton', takefocus=False, compound='left', command=self.action_all)
        # total play time
        self.playtime_label: ClassVar = Label(self.playlist_top_frame, image=self.clock_icon, text='00:00:00', compound='left', background='#111', foreground='#fff', font=('Consolas', 12))
        # number of songs
        self.num_of_songs = Label(self.playlist_top_frame, image=self.note_icon, text='', compound='left', background='#111', foreground='#fff', font=('Consolas', 12))
        # place widgets
        self.playlist_play.place(x=285, rely=0.5, anchor='w', height=35)
        self.playtime_label.place(x=418, rely=0.5, anchor='w', height=35, width=120)
        self.num_of_songs.place(x=548, rely=0.5, anchor='w', height=35, width=120)
        self.playlist_top_frame.pack(side='top', fill='x', ipady=20, pady=10)
        # scrollbar
        self.playlist_scrollbar: ClassVar = ttk.Scrollbar(self.playlist_frame)
        # playlist canvas
        self.playlist_canvas: ClassVar = Canvas(self.playlist_frame, borderwidth=0, highlightthickness=0, background='#212121', yscrollcommand=self.playlist_scrollbar.set)
        self.playlist_scrollbar.configure(command=self.playlist_canvas.yview)
        # frame for items
        self.playlist_cards: ClassVar = Frame(self.playlist_canvas, background='#212121')
        # scan for songs
        self.scan_for_songs()
        # update canvas
        self.playlist_cards.bind('<Configure>', lambda _: self.playlist_canvas.configure(scrollregion=self.playlist_canvas.bbox('all')))
        self.playlist_window: ClassVar = self.playlist_canvas.create_window((0, 0), window=self.playlist_cards, anchor='nw')
        self.playlist_canvas.bind('<Configure>', lambda _: self.playlist_canvas.itemconfigure(self.playlist_window, width=self.playlist_canvas.winfo_width(), height=len(self.playlist) * 71))
        # pack widgets
        self.playlist_scrollbar.pack(side='right', fill='y', pady=(0, 10))
        self.playlist_canvas.pack(side='left', fill='both', expand=True, padx=10, pady=(0, 10))
        # end
        # settings frame
        self.settings_top_frame: ClassVar = Frame(self.settings_frame, background='#212121')
        # save settings 
        ttk.Button(self.settings_top_frame, image=self.save_icon, text='SAVE SETTINGS', style='folder.TButton', takefocus=False, compound='left', command=self.save_settings).place(x=10, rely=0.5, anchor='w', height=35)
        # settings scrollbar
        self.settings_scrollbar: ClassVar = ttk.Scrollbar(self.settings_frame)
        # settings canvas
        self.settings_canvas: ClassVar = Canvas(self.settings_frame, borderwidth=0, highlightthickness=0, background='#212121', yscrollcommand=self.settings_scrollbar.set)
        self.settings_scrollbar.configure(command=self.settings_canvas.yview)
        # frame for items
        self.settings_cards: ClassVar = Frame(self.settings_canvas, background='#212121')
        # settings content
        # end
        # update canvas
        self.settings_cards.bind('<Configure>', lambda _: self.settings_canvas.configure(scrollregion=self.settings_canvas.bbox('all')))
        self.settings_window: ClassVar = self.settings_canvas.create_window((0, 0), window=self.settings_cards, anchor='nw')
        self.settings_canvas.bind('<Configure>', lambda _: self.settings_canvas.itemconfigure(self.settings_window, width=self.settings_canvas.winfo_width(), height=800))
        # place widgets
        self.settings_top_frame.pack(side='top', fill='x', ipady=20, pady=10)
        self.settings_scrollbar.pack(side='right', fill='y', pady=(0, 10))
        self.settings_canvas.pack(side='left', fill='both', expand=True, padx=10, pady=(0, 10))
        # end
        # main window stuff
        self.main_window.bind('<MouseWheel>', self.on_mouse)
        self.search_box.bind("<Return>", self.search_song)
        # change how the closing of the program works
        self.main_window.protocol("WM_DELETE_WINDOW", self.close)
        # load last frame that was selected by the user
        # apply settings
        self.apply_settings()
        # show window
        self.main_window.after(100, lambda: self.main_window.deiconify())
        self.main_window.mainloop()

    def on_mouse(self, event) -> None:
        SELECTED: str = self.selected.get()
        wheel_acceleration: int = int(-self.settings['wheel_acceleration']*(event.delta/120))
        if SELECTED == 'folder':
            self.folder_canvas.yview_scroll(wheel_acceleration, 'units')
        elif SELECTED == 'playlist':
            self.playlist_canvas.yview_scroll(wheel_acceleration, 'units')
        elif SELECTED == 'settings':
            self.settings_canvas.yview_scroll(wheel_acceleration, 'units')
        del SELECTED, wheel_acceleration

    def load_images(self) -> None:
        try:
            self.music_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\music.png').resize((35, 35)))
            self.cover_art_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\cover_art.png').resize((220, 220)))
            self.playlist_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\playlist.png').resize((35, 35)))
            self.settings_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\settings.png').resize((35, 35)))
            self.music_folder_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\music_folder.png').resize((35, 35)))
            self.folder_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\folder.png').resize((40, 40)))
            self.play_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\play.png').resize((30, 30)))
            self.pause_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\pause.png').resize((30, 30)))
            self.next_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\next.png').resize((30, 30)))
            self.previous_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\previous.png').resize((30, 30)))
            self.plus_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\plus.png').resize((15, 15)))
            self.refresh_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\refresh.png').resize((15, 15)))
            self.search_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\search.png').resize((20, 20)))
            self.close_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\close.png').resize((30, 30)))
            self.record_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\record.png').resize((40, 40)))
            self.note_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\record.png').resize((15, 15)))
            self.play_playlist: ClassVar = ImageTk.PhotoImage(Image.open('icons\\play.png').resize((15, 15)))
            self.shuffle_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\shuffle.png').resize((25, 25)))
            self.clock_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\clock.png').resize((15, 15)))
            self.repeat_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\repeat.png').resize((25, 25)))
            self.repeat_one_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\repeat_one.png').resize((25, 25)))
            self.warning_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\warning.png').resize((85, 85)))
            self.bug_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\bug.png').resize((35, 35)))
            self.logs_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\logs.png').resize((35, 35)))
            self.no_audio_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\no_audio.png').resize((25, 25)))
            self.audio_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\audio.png').resize((25, 25)))
            self.low_audio_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\low_audio.png').resize((25, 25)))
            self.med_audio_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\med_audio.png').resize((25, 25)))
            self.save_icon: ClassVar = ImageTk.PhotoImage(Image.open('icons\\save.png').resize((15, 15)))
        except Exception as err_obj:
            error(err_obj, exc_info=True)

    def music_card(self, song) -> None:
        title: str = splitext(basename(song))[0]
        artist: str = 'Unknown'
        length: str = '-:--:--'
        if self.songs_metadata[song][0] is not None:
            length = str(timedelta(seconds=int(self.songs_metadata[song][0].info.length)))
            if 'TIT2' in self.songs_metadata[song][0]:
                title = f'{self.songs_metadata[song][0]["TIT2"]}'
            if 'TPE1' in self.songs_metadata[song][0]:
                artist = f'{self.songs_metadata[song][0]["TPE1"]}'
        music_frame: ClassVar = Frame(self.playlist_cards, background='#111')
        Label(music_frame, image=self.record_icon, background='#333', foreground='#fff', font=('Consolas', 15)).place(x=0, y=0, width=50, relheight=1)
        Label(music_frame, text=f'{title}', background='#111', foreground='#fff', font=('Consolas', 14)).place(x=58, rely=0.28, anchor='w')
        Label(music_frame, text=f'{artist}', background='#333', foreground='#fff', font=('Consolas', 12)).place(x=58, rely=0.72, anchor='w')
        Label(music_frame, image=self.clock_icon, text=length, compound='left', background='#333', foreground='#fff', font=('Consolas', 12)).place(relx=0.9, rely=0.5, height=30, anchor='e')
        self.songs_metadata[song][1]: ClassVar = ttk.Button(music_frame, image=self.play_icon, style='folder.TButton', takefocus=False, command=lambda: self.action_card(song))
        self.songs_metadata[song][1].place(relx=1, rely=1, relheight=1, anchor='se')
        music_frame.pack(side='top', fill='x', ipady=30, pady=(0, 10))
        del title, artist, length, music_frame

    def remove_music_cards(self) -> None:
        for widget in self.get_all_widgets(self.playlist_cards):
            widget.destroy()

    def get_metadata(self) -> None:
        try:
            self.songs_metadata: dict = {}
            for song in self.songs:
                if splitext(song)[1] == '.mp3':
                    self.songs_metadata[song]: list = [MP3(song), None]
                else:
                    self.songs_metadata[song]: list = [None, None]
        except Exception as err_obj:
            self.dump_err(err_obj)

    def switch_frame(self) -> None:
        SELECTED: str = self.selected.get()
        self.settings['last_card'] = SELECTED
        if SELECTED == 'playback':
            self.playback_frame.lift()
        elif SELECTED == 'playlist':
            self.playlist_frame.lift()
        elif SELECTED == 'folder':
            self.folder_frame.lift()
        elif SELECTED == 'settings':
            self.settings_frame.lift()
        del SELECTED

    def folder_card(self, path: str) -> None:
        folder_frame: ClassVar = Frame(self.folder_cards, background='#111')
        Label(folder_frame, image=self.folder_icon, background='#333', foreground='#fff', font=('Consolas', 16)).place(x=0, y=0, width=50, relheight=1)
        Label(folder_frame, text=f'{basename(path)}', background='#111', foreground='#fff', font=('Consolas', 14)).place(x=58, rely=0.28, anchor='w')
        Label(folder_frame, text=f'{path}', background='#111', foreground='#fff', font=('Consolas', 12)).place(x=58, rely=0.72, anchor='w')
        ttk.Button(folder_frame, image=self.close_icon, style='folder.TButton', takefocus=False,command=lambda: self.remove_folder(folder_frame, path)).place(relx=1, rely=1, relheight=1, anchor='se')
        folder_frame.pack(side='top', fill='x', ipady=30, pady=(0, 10))

    def remove_folder(self, card: ClassVar, path: str) -> None:
        self.settings['folders'].remove(path)
        for widget in self.get_all_widgets(card):
            widget.destroy()
        card.destroy()
        self.scan_for_folders()
        self.refresh_folder()
        self.scan_for_songs()
        self.refresh_songs()

    def add_folder(self) -> None:
        new_directory: str = askdirectory()
        if new_directory and not new_directory in self.settings['folders']:
            self.settings['folders'].append(new_directory)
            self.scan_for_songs()
            self.scan_for_folders()
            self.folder_card(new_directory)
            self.refresh_folder()
        del new_directory

    def refresh_folder(self) -> None:
        self.folder_canvas.yview_moveto(0)
        self.folder_canvas.itemconfigure(self.folder_window, width=self.folder_canvas.winfo_width(), height=len(self.settings['folders']) * 71)

    def remove_folder_cards(self) -> None:
        for widget in self.get_all_widgets(self.folder_cards):
            widget.destroy()

    def scan_for_folders(self) -> None:
        self.remove_folder_cards()
        for folder in self.settings['folders']:
            if isdir(folder):
                self.folder_card(folder)
            else:
                self.settings['folders'].remove(folder)
        if not bool(self.settings['folders']):
            self.info_card(f'ADD A FOLDER TO START LISTENING', self.folder_cards)

    def open_logs(self) -> None:
        if getLogger().isEnabledFor(ERROR):
            shutdown()
        if isfile("errors.log"):
            startfile("errors.log")

    def dump_err(self, err_obj: ClassVar) -> None:
        self.error_reason['text'] = str(err_obj)
        self.error_frame.lift()
        error(err_obj, exc_info=True)

    def load_settings(self) -> None:
        try:
            if isfile('settings.json'):
                with open('settings.json', 'r') as file:
                    self.settings = load(file)
                    self.settings_correction()
            else:
                self.settings = {'folders': [], 'last_card': 'playback', 'shuffle': False, 'repeat': 'none', 'wheel_acceleration': 1.0, 'width': 750, 'height': 450, 'volume': 0.50}
        except Exception as err_obj:
            print(err_obj)

    def apply_settings(self) -> None:
        # set window size
        self.main_window.geometry(f'{self.settings["width"]}x{self.settings["height"]}+{int(self.main_window.winfo_x() + ((self.main_window.winfo_screenwidth() - self.settings["width"]) / 2))}+{int(self.main_window.winfo_y() +((self.main_window.winfo_screenheight() - self.settings["height"]) / 2))}')
        # switch to frame
        self.selected.set(self.settings['last_card'])
        self.switch_frame()
        # update shuffle and repeat buttons
        self.update_buttons()
        # volume
        self.volume_bar.set(self.settings['volume'])
        self.update_volume()
        # last played
        if bool(self.playlist):
            if self.settings['song'] in self.playlist:
                self.song = self.settings['song']

    def save_settings(self) -> None:
        try:
            with open('settings.json', 'w') as file:
                dump(self.settings, file)
        except Exception as err_obj:
            print(err_obj)

    def settings_correction(self) -> None:
        frames: list = ['playback', 'playlist', 'folder', 'settings']
        try:
            self.settings['last_card']
        except Exception as _:
            self.settings['last_card'] = ''
        finally:
            if not self.settings['last_card'] in frames:
                self.settings['last_card']: str = 'playback'
        try:
            self.settings['folders']: list = list(
                set(self.settings['folders']))
        except Exception as err_obj:
            print(err_obj)
        try:
            self.settings['shuffle']
        except Exception as _:
            self.settings['shuffle']: bool = False
        try:
            self.settings['repeat']
        except Exception as _:
            self.settings['repeat']: str = 'none'
        try:
            self.settings['wheel_acceleration']
        except Exception as _:
            self.settings['wheel_acceleration']: float = 1.0 
        try:
            self.settings['width']
        except Exception as _:
            self.settings['width']: int = 750
        try:
            self.settings['height']
        except Exception as _:
            self.settings['height']: int = 450
        try:
            self.settings['volume']
        except Exception as _:
            self.settings['volume']: float = 0.50
        try:
            self.settings['song']
        except Exception as _:
            self.settings['song']: str = ''
        del frames

    def get_all_widgets(self, widget) -> list:
        widget_list = widget.winfo_children()
        for widget in widget_list:
            if widget.winfo_children():
                widget_list.extend(widget.winfo_children())
        return widget_list

    def close(self) -> None:
        # hide window
        self.main_window.withdraw()
        # stop music playback
        if mixer.get_busy():
            mixer.music.stop()
            sleep(2)
        # exit mixer
        mixer.quit()
        # destroy all widgets
        for widget in self.get_all_widgets(self.main_window):
            widget.destroy()
        # save window size
        self.settings['width'] = self.main_window.winfo_width()
        self.settings['height'] = self.main_window.winfo_height()
        self.settings['song'] = self.song
        self.save_settings()
        # exit program
        self.main_window.destroy()

    def scan_for_songs(self) -> None:
        supported_extensions: list = ['.mp3']
        self.songs = []
        try:
            for folder in self.settings['folders']:
                for file in listdir(folder):
                    if splitext(file)[1] in supported_extensions:
                        self.songs.append(abspath(join(folder, file)))
            del supported_extensions
            self.playlist = self.songs
            self.active_card = []
            self.sort_songs()
            self.get_metadata()
            self.add_songs()
            self.update_lenght()
            self.update_num_of_songs()
            self.update_state()
            self.update_active_card()
        except Exception as err_obj:
            error(err_obj, exc_info=True)

    def refresh_songs(self) -> None:
        self.playlist_canvas.yview_moveto(0)
        self.playlist_canvas.itemconfigure(self.playlist_window, width=self.playlist_canvas.winfo_width(), height=len(self.playlist) * 71)

    def add_songs(self) -> None:
        self.remove_music_cards()
        for song in self.songs:
            try:
                self.music_card(song)
            except Exception as err_obj:
                error(err_obj, exc_info=True)
        if not bool(self.songs):
            self.info_card(f'WE ARE UNABLE TO FIND ANY SONG', self.playlist_cards)

    def validate_entry(self, char: str, length: int) -> bool:
        disallowed_chars: list = [37, 40, 41, 42, 43, 47, 61, 63, 91, 92, 94, 124]
        if not bool(char) or len(char) > 1:
            del disallowed_chars
            return True
        if ord(char) in disallowed_chars:
            self.main_window.bell()
            del disallowed_chars
            return False
        del disallowed_chars
        return True

    def search_song(self, event=None) -> None:
        word: str = str(self.search_box.get())
        result: str = ''
        if bool(word) and bool(self.songs):
            self.playlist = []
            self.active_card = []
            self.remove_music_cards()
            self.playlist_canvas.yview_moveto(0)
            for song in self.songs:
                if self.songs_metadata[song][0] is not None:
                    if 'TIT2' in self.songs_metadata[song][0]:
                        result += f'{self.songs_metadata[song][0]["TIT2"]} '
                    if 'TPE1' in self.songs_metadata[song][0]:
                        result += f'{self.songs_metadata[song][0]["TPE1"]} '
                    if 'TALB' in self.songs_metadata[song][0]:
                        result += f'{self.songs_metadata[song][0]["TALB"]} '
                    if 'TCON' in self.songs_metadata[song][0]:
                        result += f'{self.songs_metadata[song][0]["TCON"]} '
                result += f'{basename(song)} '
                if bool(findall(word.lower(), result.lower())):
                    self.music_card(song)
                    self.playlist.append(song)
                result = ''
            self.refresh_songs()
            if not bool(self.playlist_cards.winfo_children()):
                self.info_card(f'NO MATCH FOR \'{word}\'', self.playlist_cards)
        else:
            self.playlist = self.songs
            self.add_songs()
            self.refresh_songs()
        self.update_lenght()
        self.update_num_of_songs()
        self.update_active_card()
        del word, result

    def info_card(self, msg: str, frame: ClassVar) -> None:
        music_frame: ClassVar = Frame(frame, background='#111')
        Label(music_frame, image=self.close_icon, background='#333', foreground='#fff', font=('Consolas', 15)).place(x=0, y=0, width=50, relheight=1)
        Label(music_frame, text=f' {msg}', background='#111', foreground='#fff', font=('Consolas', 14)).place(x=58, rely=0.5, anchor='w')
        music_frame.pack(side='top', fill='x', ipady=30, pady=(0, 10))

    def update_state(self) -> None:
        # disable buttons
        if not bool(self.songs):
            self.playlist_play.state(['disabled'])
            self.shuffle_button.state(['disabled'])
            self.play_button.state(['disabled'])
            self.previous_button.state(['disabled'])
            self.next_button.state(['disabled'])
            self.repeat_button.state(['disabled'])
        else:
            self.playlist_play.state(['!disabled'])
            self.shuffle_button.state(['!disabled'])
            self.play_button.state(['!disabled'])
            self.previous_button.state(['!disabled'])
            self.next_button.state(['!disabled'])
            self.repeat_button.state(['!disabled'])

    def update_buttons(self) -> None:
        # shuffle
        if self.settings['shuffle']:
            self.shuffle_button['style'] = 'shuffle.TButton'
        # repeat
        if self.settings['repeat'] in ['all', 'one']:
            self.repeat_button.configure(style='shuffle.TButton')
            if self.settings['repeat'] == 'one':
                self.repeat_button.configure(image=self.repeat_one_icon)
        else:
            self.shuffle_button['style'] = 'TButton'

    def update_lenght(self) -> None:
        self.get_playtime()
        self.playtime_label['text'] = f'{self.play_time}'

    def update_num_of_songs(self) -> None:
        num_of_songs: int = len(self.playlist)
        if num_of_songs == 1:
            self.num_of_songs['text'] = f'{num_of_songs} Song'
        else:
            self.num_of_songs['text'] = f'{num_of_songs} Songs'
        del num_of_songs

    def toggle_shuffle(self) -> None:
        if self.settings['shuffle']:
            self.settings['shuffle'] = False
            self.shuffle_button.configure(style='TButton')
        else:
            self.settings['shuffle'] = True
            self.shuffle_button.configure(style='shuffle.TButton')
        self.sort_songs()
        self.add_songs()
        self.update_active_card()

    def toggle_repeat(self) -> None:
        if self.settings['repeat'] == 'none':
            self.settings['repeat'] = 'all'
            self.repeat_button.configure(style='shuffle.TButton')
        elif self.settings['repeat'] == 'all':
            self.settings['repeat'] = 'one'
            self.repeat_button.configure(image=self.repeat_one_icon)
        else:
            self.settings['repeat'] = 'none'
            self.repeat_button.configure(style='TButton', image=self.repeat_icon)

    def sort_songs(self) -> None:
        if self.settings['shuffle']:
            shuffle(self.songs)
        else:
            self.songs.sort(key=self.sort_by_letter)

    def sort_by_letter(self, letter: str) -> str:
        return splitext(basename(letter))[0].split(' ')[0].lower()

    def get_playtime(self) -> None:
        play_time: float = 0.0
        for song in self.playlist:
            if self.songs_metadata[song][0] is not None:
                play_time += self.songs_metadata[song][0].info.length
        self.play_time: ClassVar = timedelta(seconds=int(play_time))
        del play_time

    def init_mixer(self) -> None:
        try:
            mixer.pre_init(frequency=44100, size=0, channels=2, buffer=512)
            mixer.init()
        except Exception as err_obj:
            self.dump_err(err_obj)

    def toggle_volume(self) -> None:
        self.settings['volume'] = 0.00
        self.update_volume()
        self.volume_bar.set(0)
        mixer.music.set_volume(self.settings['volume'])

    def change_volume(self, event) -> None:
        self.settings['volume'] = round(float(event), 2)
        self.update_volume()
        mixer.music.set_volume(self.settings['volume'])
    
    def update_volume(self) -> None:
        if self.settings['volume'] == 0.00:
            self.mute_button.configure(image=self.no_audio_icon)
        elif 0.01 <= self.settings['volume'] <= 0.30:
            self.mute_button.configure(image=self.low_audio_icon)
        elif 0.30 <= self.settings['volume'] <= 0.90:
            self.mute_button.configure(image=self.med_audio_icon)
        elif self.settings['volume'] > 0.90:
            self.mute_button.configure(image=self.audio_icon)

    def update_active_card(self) -> None:
        for widget in self.active_card:
            if widget not in self.get_all_widgets(self.playlist_cards):
                self.active_card.remove(widget)
            else:
                for widget in self.active_card:
                    widget.configure(image=self.play_icon)
                    self.active_card.remove(widget)
        if  mixer.music.get_busy() and bool(self.song) and bool(self.playlist) and self.songs_metadata[self.song][1] in self.get_all_widgets(self.playlist_cards) and not self.paused:
            self.songs_metadata[self.song][1].configure(image=self.pause_icon)
            self.active_card.append(self.songs_metadata[self.song][1])

    def update_play_button(self) -> None:
        if mixer.music.get_busy() and self.paused:
            self.play_button.configure(image=self.play_icon)
        elif mixer.music.get_busy() and not self.paused:
           self.play_button.configure(image=self.pause_icon)
        else:
            self.play_button.configure(image=self.play_icon)

    def action_play(self) -> None:
        if bool(self.playlist):
            if mixer.music.get_busy():
                if self.paused:
                    self.unpause_song()
                else:
                    self.pause_song()
            elif bool(self.song):
                self.play_song()
            else:
                self.song = self.playlist[0]
                self.play_song()
    
    def action_next(self) -> None:
        if bool(self.playlist):
            if bool(self.song):
                if (self.playlist.index(self.song) + 1) < len(self.playlist):
                    self.song = self.playlist[self.playlist.index(self.song) + 1]
                    self.play_song()
            else:
                self.play_song()
    
    def action_prev(self) -> None:
        if bool(self.playlist):
            if bool(self.song):
                if (self.playlist.index(self.song) - 1) >= 0:
                    self.song = self.playlist[self.playlist.index(self.song) - 1]
                    self.play_song()
            else:
                self.play_song()

    def action_card(self, song) -> None:
        if bool(self.playlist):
            if song == self.song and mixer.music.get_busy():
                if self.paused:
                    self.unpause_song()
                else:
                    self.pause_song()
            else:
                self.song = song
                self.play_song()
    
    def action_all(self) -> None:
        if bool(self.playlist):
            self.song = self.playlist[0]
            self.play_song()

    def play_song(self) -> None:
        if bool(self.playlist):
            if mixer.music.get_busy():
                mixer.music.stop()
            mixer.music.load(self.song)
            mixer.music.play()
            self.paused = False
            self.update_songs_metadata()
            self.update_active_card()
            self.update_play_button()
        if active_count() == 1:
            Thread(target=self.play_thread, daemon=True).start()

    def pause_song(self) -> None:
        if mixer.music.get_busy() and bool(self.playlist):
            mixer.music.pause()
            self.paused = True
            self.update_active_card()
            self.update_play_button()

    def unpause_song(self) -> None:
        if mixer.music.get_busy() and bool(self.playlist):
            mixer.music.unpause()
            self.paused = False
            self.update_active_card()
            self.update_play_button()

    def play_thread(self) -> None:
        position: float = 0.0
        minute: float = 0.0
        second: float = 0.0
        while mixer.music.get_busy() and bool(self.playlist):
            position = mixer.music.get_pos() / 1000
            minute, second = divmod(position, 60)
            self.time_passed['text'] = f'{int(minute)}:{str(int(second)).zfill(2)}'
            self.scale_bar.set(position)
            sleep(0.08)
        del position, minute, second
        self.main_window.after(500, self.after_play)

    def update_songs_metadata(self) -> None:
        if self.songs_metadata[self.song][0] is not None:
            if 'APIC:' in self.songs_metadata[self.song][0]:
                raw_album: bytes = self.songs_metadata[self.song][0].get("APIC:").data
                self.new_cover_art_icon: ClassVar = ImageTk.PhotoImage(Image.open(BytesIO(raw_album)).resize((220, 220)))
                self.cover_art.configure(image=self.new_cover_art_icon)
                del raw_album
            else:
                self.cover_art.configure(image=self.cover_art_icon)
            if 'TIT2' in self.songs_metadata[self.song][0]:
                self.song_name['text'] = f'{self.songs_metadata[self.song][0]["TIT2"]}'
            else:
                self.song_name['text'] = splitext(basename(self.song))[0]
            if 'TPE1' in self.songs_metadata[self.song][0]:
                self.song_name['text'] = f'{self.song_name["text"]}\n{self.songs_metadata[self.song][0]["TPE1"]}'
            if 'TALB' in self.songs_metadata[self.song][0]:
                self.album_name['text'] = f'{self.songs_metadata[self.song][0]["TALB"]}'
            else:
                self.album_name['text'] = 'Unknown'
            length: float = self.songs_metadata[self.song][0].info.length
            self.scale_bar.configure(from_=0, to=length)
            minute, second = divmod((length), 60)
            self.song_length['text'] = f'{int(minute)}:{str(int(second)).zfill(2)}'
            del length, minute, second
        else:
            self.song_name['text'] = 'Unknown'
            self.song_length['text'] = '--:--'
            self.scale_bar.configure(from_=0, to=0)

    def after_play(self) -> None:
        if bool(self.playlist):
            if self.settings['repeat'] == 'one':
                self.play_song()
            elif self.settings['repeat'] == 'all':
                if bool(self.song):
                    if (self.playlist.index(self.song) + 1) < len(self.playlist):
                        self.song = self.playlist[self.playlist.index(self.song) + 1]
                        self.play_song()
                    else:
                        self.song = self.playlist[0]
                        self.play_song()
                else:
                    self.play_song()
            elif self.settings['repeat'] == 'none':
                self.update_active_card()
                self.update_play_button()


if __name__ == '__main__':
    App()

