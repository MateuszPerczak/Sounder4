from tkinter import Tk, Frame, Label, PhotoImage, Radiobutton, Button, StringVar, BooleanVar, Canvas, Scrollbar, ttk, Entry, Toplevel, Text, messagebox, Spinbox
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askyesno
from logging import basicConfig, error, ERROR, getLevelName, getLogger, shutdown
from traceback import format_exc
from typing import ClassVar
from os import getcwd, listdir, startfile, remove as rmfile
from os.path import basename, isfile, isdir, splitext, abspath, join, getsize
from PIL import Image, ImageTk
from json import dump, load
from mutagen.mp3 import MP3
from io import BytesIO
from random import shuffle, randint
from datetime import timedelta
from re import findall
from pygame import mixer
from threading import Thread, active_count, enumerate as enum_threads
from time import sleep
from webbrowser import open as open_browser
from requests import get
from Debugger import Debugger

class Sounder:
    def __init__(self):
        # logging error messages
        basicConfig(filename=f"{getcwd()}\\errors.log", level=ERROR)
        # create window
        self.main_window: ClassVar = Tk()
        # hide window
        self.main_window.withdraw()
        # configure window 
        self.main_window.minsize(822, 555)
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
        self.main_theme.configure('restore.TButton', background='#151515', relief='flat', font=('corbel', 12), foreground='#fff')
        self.main_theme.map('restore.TButton', background=[('pressed', '!disabled', '#d84040'), ('active', '#f04747')], foreground=[('pressed', '!disabled', '#fff'), ('active', '#fff')])
        self.main_theme.configure('menu.TButton', background='#151515', relief='flat', font=('corbel', 12), foreground='#fff')
        self.main_theme.map('menu.TButton', background=[('pressed', '!disabled', '#151515'), ('active', '#212121')])
        self.main_theme.layout('Vertical.TScrollbar',[('Vertical.Scrollbar.trough', {'children': [('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})], 'sticky': 'ns'})])
        self.main_theme.configure('Vertical.TScrollbar', gripcount=0, relief='flat', background='#212121', darkcolor='#212121', lightcolor='#212121', troughcolor='#212121', bordercolor='#212121', arrowcolor='#212121')
        self.main_theme.map('Vertical.TScrollbar', background=[('pressed', '!disabled', '#333'), ('disabled', '#212121'), ('active', '#111'), ('!active', '#111')])
        self.main_theme.configure("Horizontal.TProgressbar", foreground='#000', background='#212121', lightcolor='#111', darkcolor='#111', bordercolor='#111', troughcolor='#111')
        self.main_theme.map('Horizontal.TScale', background=[('pressed', '!disabled', '#333'), ('active', '#333')])
        # self.main_theme.configure('Horizontal.TScale', troughcolor='#151515', background='#333', relief="flat", gripcount=0, darkcolor="#151515", lightcolor="#151515", bordercolor='#151515')
        self.main_theme.configure('Horizontal.TScale', troughcolor='#111', background='#212121', relief='flat', gripcount=0, darkcolor='#111', lightcolor='#111', bordercolor='#111')
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
        self.debugger_frame: ClassVar = Frame(self.content_frame, background='#212121')
        self.error_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.main_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.select_frame.pack(side='top', fill='x', ipady=25)
        self.content_frame.pack(side='left', fill='both', expand=True)
        self.settings_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.playback_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.playlist_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.folder_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.debugger_frame.place(x=0, y=0, relwidth=1, relheight=1)
        # end
        # variables
        self.selected: StringVar = StringVar()
        self.on_startup: StringVar = StringVar()
        self.time_precision: StringVar = StringVar()
        self.sort_by: StringVar = StringVar()
        self.move_song: StringVar = StringVar()
        self.update: BooleanVar = BooleanVar()
        self.icons_folder: StringVar = StringVar()
        self.settings: dict = {}
        self.songs: list = []
        self.playlist: list = []
        self.active_card: list = []
        self.volume: float = 0.0
        self.song: str = ''
        self.paused: bool = False
        self.VERSION: str = '0.9.5'
        # on load
        # load settings
        self.load_settings()
        # load icons
        self.load_images()
        # error_frame
        Label(self.error_frame, image=self.warning_icon, text='Something went wrong', compound='top', font=('corbel', 35), background='#212121', foreground='#fff', anchor='center', justify='center').place(relx=0.5, rely=0.35, anchor='center', height=250)
        self.error_reason: ClassVar = Label(self.error_frame, text='', font=('corbel', 20), background='#212121', foreground='#e74c3c', anchor='center', justify='center')
        ttk.Button(self.error_frame, image=self.bug_icon, text=' Report a bug', compound='left', style='error.TButton', takefocus=False, command=lambda: open_browser('https://github.com/losek1/Sounder4/issues', new=0, autoraise=True)).place(relx=0.7, rely=0.96, anchor='s')
        ttk.Button(self.error_frame, image=self.logs_icon, text=' Open logs', compound='left', style='error.TButton', takefocus=False, command=self.open_logs).place(relx=0.3, rely=0.96, anchor='s')
        self.error_reason.place(relx=0.5, rely=0.64, anchor='s')
        # end
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
        top_frame: ClassVar = Frame(self.playback_frame, background='#212121')
        # menu frame
        self.menu_frame: ClassVar = Frame(top_frame, background=top_frame['background'], width=0)
        self.button_frame: ClassVar = Frame(self.menu_frame, background='#111')
        Label(self.button_frame, image=self.file_icon, text=' MANAGE SONG', background='#333', foreground='#fff', font=('Consolas', 14), compound='left').pack(side='top', fill='x', anchor='w', ipady=4, ipadx=2)
        ttk.Button(self.button_frame, image=self.trash_icon, text='REMOVE FROM DISK', style='restore.TButton', compound='left', takefocus=False, command=lambda: self.manage_song(True)).pack(side='bottom', fill='x', anchor='w', padx=10, pady=10)
        ttk.Button(self.button_frame, image=self.trash_icon, text='REMOVE FROM PLAYLIST', style='menu.TButton', compound='left', takefocus=False, command=lambda: self.manage_song(False)).pack(side='bottom', fill='x', anchor='w', padx=10, pady=(10, 0))
        self.menu_frame.pack(side='left', fill='y', padx=(0, 10), pady=(10, 0))
        # album label
        self.album_name: ClassVar = Label(top_frame, text='ALBUM NAME', font=('Consolas', 15), compound='left', background=top_frame['background'], foreground='#fff', anchor='center', justify='center')  
        self.album_name.pack(side='top', anchor='center', fill='x', padx=10, pady=(10, 0), expand=True)
        # cover label
        self.cover_art: ClassVar = Label(top_frame, image=self.cover_art_icon, background=top_frame['background'])
        self.cover_art.pack(side='top', anchor='center', fill='x', padx=10, pady=(10, 0), expand=True)   
        # song label
        self.song_name: ClassVar = Label(top_frame, text='SONG TITLE', font=('Consolas', 15), background=top_frame['background'], foreground='#fff', anchor='center', justify='center')
        self.song_name.pack(side='top', anchor='center', fill='x', padx=10, pady=(10, 0), expand=True)
        # artist label   
        self.song_artist: ClassVar = Label(top_frame, text='ARTIST NAME', font=('Consolas', 12), background=top_frame['background'], foreground='#fff', anchor='center', justify='center')
        self.song_artist.pack(side='top', anchor='center', fill='x', padx=10, pady=(0, 10), expand=True)   
        # bottom frame
        bottom_frame: ClassVar = Frame(self.playback_frame, background='#111')
        # buttons frame
        buttons_frame: ClassVar = Frame(bottom_frame, background=bottom_frame['background'])
        # play button
        self.play_button: ClassVar = ttk.Button(buttons_frame, image=self.play_icon, takefocus=False, command=self.action_play)
        self.play_button.place(relx=0.5, rely=0.5, anchor='center')
        # next button
        self.next_button: ClassVar = ttk.Button(buttons_frame, image=self.next_icon, takefocus=False, command=self.action_next)
        self.next_button.place(relx=0.7, rely=0.5, anchor='center')
        # previous button
        self.previous_button: ClassVar = ttk.Button(buttons_frame, image=self.previous_icon, takefocus=False, command=self.action_prev)
        self.previous_button.place(relx=0.3, rely=0.5, anchor='center')
        # shuffle button
        self.shuffle_button: ClassVar = ttk.Button(buttons_frame, image=self.shuffle_icon, takefocus=False, command=self.toggle_shuffle)
        self.shuffle_button.place(relx=0.1, rely=0.5, anchor='center')
        # repeat button
        self.repeat_button: ClassVar = ttk.Button(buttons_frame, image=self.repeat_icon, takefocus=False, command=self.toggle_repeat)
        self.repeat_button.place(relx=0.9, rely=0.5, anchor='center')
        # scale frame
        progress_frame: ClassVar = Frame(bottom_frame, background=bottom_frame['background'])
        # time passed
        self.time_passed: ClassVar = Label(progress_frame, text='--:--', font=('Consolas', 9), compound='left', background=bottom_frame['background'], foreground='#fff', anchor='center', justify='center')
        self.time_passed.pack(side='left', ipadx=8)
        # progress bar
        self.progress_bar: ClassVar = ttk.Progressbar(progress_frame, orient="horizontal", mode="determinate")
        self.progress_bar.pack(side='left', fill='x', expand=True)
        # song length
        self.song_length: ClassVar = Label(progress_frame, text='--:--', font=('Consolas', 9), compound='left', background=bottom_frame['background'], foreground='#fff', anchor='center', justify='center')
        self.song_length.pack(side='right', ipadx=8)
        # volume frame
        volume_frame: ClassVar = Frame(bottom_frame, background=bottom_frame['background'])
        # volume button
        self.mute_button: ClassVar = ttk.Button(volume_frame, image=self.no_audio_icon, takefocus=False, command=self.toggle_volume)
        self.mute_button.pack(side='left', anchor='center', padx=5)
        # volume bar
        self.volume_bar: ClassVar = ttk.Scale(volume_frame, orient='horizontal', from_=0, to=1, command=self.change_volume)
        self.volume_bar.pack(side='left', anchor='center', padx=5, fill='x', expand=True)
        # menu button
        left_frame: ClassVar = Frame(bottom_frame, background=bottom_frame['background'])
        ttk.Button(left_frame, image=self.menu_icon, takefocus=False, command=self.open_music_menu).pack(side='left', anchor='center', padx=5)
        self.favorites_button: ClassVar = ttk.Button(left_frame, image=self.heart_icon, takefocus=False, command=self.add_favorites)
        self.favorites_button.pack(side='left', anchor='center', padx=5)
        # place frames
        top_frame.pack(side='top', anchor='center', fill='both', expand=True)
        bottom_frame.pack(side='bottom', anchor='center', fill='x', ipady=45)
        buttons_frame.place(relx=0.5, y=10, width=350, height=48, anchor='n')
        volume_frame.place(relx=1, y=10, relwidth=0.22, height=48, anchor='ne')
        left_frame.place(relx=0, y=10, relwidth=0.15, height=48, anchor='nw')
        progress_frame.place(relx=0.5, y=68, relwidth=1, height=20, anchor='n')
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
        self.folder_cards: ClassVar = Frame(self.folder_canvas, background=self.folder_top_frame['background'])
        # add folders
        self.scan_for_folders()
        # update canvas
        self.folder_cards.bind('<Expose>', lambda _: self.folder_canvas.configure(scrollregion=self.folder_canvas.bbox('all')))
        self.folder_window: ClassVar = self.folder_canvas.create_window((0, 0), window=self.folder_cards, anchor='nw')
        self.folder_canvas.bind('<Expose>', lambda _: self.folder_canvas.itemconfigure(self.folder_window, width=self.folder_canvas.winfo_width(), height=len(self.settings['folders']) * 71))
        # pack canvas
        self.folder_scrollbar.pack(side='right', fill='y', pady=(0, 10))
        self.folder_canvas.pack(side='left', fill='both',expand=True, padx=10, pady=(0, 10))
        # end
        # playlist
        self.playlist_top_frame: ClassVar = Frame(self.playlist_frame, background='#212121')
        # validate entry
        search_box_validator = (self.main_window.register(self.validate_search_entry), '%S', '%i')
        # entry
        self.search_box: ClassVar = Entry(self.playlist_top_frame, validate="key", validatecommand=search_box_validator, exportselection=False, border=0, insertbackground='#fff', selectbackground='#333', selectforeground='#fff', background='#111', foreground='#fff', font=('Consolas', 16))
        self.search_box.place(x=10, rely=0.5, height=35, width=230, anchor='w')
        # search button
        ttk.Button(self.playlist_top_frame, image=self.search_icon, style='folder.TButton', takefocus=False, command=self.search_song).place(x=240, rely=0.5, anchor='w', height=35, width=35)
        # play all button
        self.playlist_play: ClassVar = ttk.Button(self.playlist_top_frame, image=self.play_playlist, text='PLAY ALL', style='folder.TButton', takefocus=False, compound='left', command=self.action_all)
        # total play time
        self.playtime_label: ClassVar = Label(self.playlist_top_frame, image=self.clock_icon, text='00:00:00', compound='left', background='#111', foreground='#fff', font=('Consolas', 12))
        # number of songs
        self.num_of_songs = Label(self.playlist_top_frame, image=self.note_icon, text='', compound='left', background='#111', foreground='#fff', font=('Consolas', 12))
        # sort menu
        self.sort_button: ClassVar = ttk.Button(self.playlist_top_frame, image=self.filter_icon, text='SORT BY', style='folder.TButton', takefocus=False, compound='left', command=self.open_sort_menu)
        # place widgets
        self.playlist_play.place(x=285, rely=0.5, anchor='w', height=35)
        self.playtime_label.place(x=418, rely=0.5, anchor='w', height=35, width=120)
        self.num_of_songs.place(x=548, rely=0.5, anchor='w', height=35, width=120)
        self.sort_button.place(x=678, rely=0.5, anchor='w', height=35, width=120)
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
        self.playlist_cards.bind('<Expose>', lambda _: self.playlist_canvas.configure(scrollregion=self.playlist_canvas.bbox('all')))
        self.playlist_window: ClassVar = self.playlist_canvas.create_window((0, 0), window=self.playlist_cards, anchor='nw')
        self.playlist_canvas.bind('<Expose>', lambda _: self.playlist_canvas.itemconfigure(self.playlist_window, width=self.playlist_canvas.winfo_width(), height=len(self.playlist) * 71))
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
        self.settings_cards: ClassVar = Frame(self.settings_canvas, background=self.settings_top_frame['background'])
        # settings content
        # file size
        file_size_frame: ClassVar = Frame(self.settings_cards, background='#111')
        Label(file_size_frame, image=self.audio_file_icon, text=' MUSIC FILE SIZE', compound='left', background=file_size_frame['background'], foreground='#fff', font=('Consolas', 16), anchor='w').pack(side='top', fill='x', pady=5, padx=10)
        min_size_frame: ClassVar = Frame(file_size_frame, background=file_size_frame['background'])
        Label(min_size_frame, text='MIN FILE SIZE:', background=min_size_frame['background'], foreground='#fff', font=('Consolas', 12), anchor='w').pack(side='left', anchor='w', pady=5, padx=10)
        size_box_validator = (self.main_window.register(self.validate_size_entry), '%S', '%i')
        self.min_size_entry: ClassVar = Entry(min_size_frame, validate="key", validatecommand=size_box_validator, exportselection=False, border=0, insertbackground='#fff', selectbackground='#333', selectforeground='#fff', background='#212121', foreground='#fff', font=('Consolas', 12), width=8, justify='center')
        self.min_size_entry.pack(side='left', anchor='w')
        Label(min_size_frame, text='MB', background=min_size_frame['background'], foreground='#fff', font=('Consolas', 12), anchor='w').pack(side='left', anchor='w', pady=5, padx=10)
        min_size_frame.pack(side='top', fill='x', expand=True)
        max_size_frame: ClassVar = Frame(file_size_frame, background=file_size_frame['background'])
        Label(max_size_frame, text='MAX FILE SIZE:', background=max_size_frame['background'], foreground='#fff', font=('Consolas', 12), anchor='w').pack(side='left', anchor='w', pady=5, padx=10)
        size_box_validator = (self.main_window.register(self.validate_size_entry), '%S', '%i')
        self.max_size_entry: ClassVar = Entry(max_size_frame, validate="key", validatecommand=size_box_validator, exportselection=False, border=0, insertbackground='#fff', selectbackground='#333', selectforeground='#fff', background='#212121', foreground='#fff', font=('Consolas', 12), width=8, justify='center')
        self.max_size_entry.pack(side='left', anchor='w')
        Label(max_size_frame, text='MB', background=max_size_frame['background'], foreground='#fff', font=('Consolas', 12), anchor='w').pack(side='left', anchor='w', pady=5, padx=10)
        max_size_frame.pack(side='top', fill='x', expand=True)
        file_size_frame.pack(side='top', fill='x', pady=(0, 10))
        # transition
        transition_frame = Frame(self.settings_cards, background='#111')
        Label(transition_frame, image=self.transition_icon, text=' TRANSITION', compound='left', background=transition_frame['background'], foreground='#fff', font=('Consolas', 16), anchor='w').pack(side='top', fill='x', pady=5, padx=10)
        self.transition_label: ClassVar = Label(transition_frame, text=f'VALUE: {self.settings["transition"]}s', background=transition_frame['background'], foreground='#fff', font=('Consolas', 12), anchor='w')
        self.transition_label.pack(side='top', fill='x', anchor='center', pady=5, padx=10)
        Label(transition_frame, text='0s', background=transition_frame['background'], foreground='#fff', font=('Consolas', 12), anchor='w').pack(side='left', anchor='w', pady=5, padx=10)
        self.transition_scale: ClassVar = ttk.Scale(transition_frame, orient='horizontal', from_=0, to=18, length=5, command=self.change_transition)
        self.transition_scale.pack(side='left', fill='x', anchor='w', expand=True, pady=5, padx=10)
        Label(transition_frame, text='18s', background=transition_frame['background'], foreground='#fff', font=('Consolas', 12), anchor='w').pack(side='left', anchor='w', pady=(5, 10), padx=10)
        transition_frame.pack(side='top', fill='x', pady=(0, 10))
        # move playing song to view
        move_song_frame: ClassVar = Frame(self.settings_cards, background='#111')
        Label(move_song_frame, image=self.arrow_icon, text=' MOVE PLAYING SONG TO VIEW', compound='left', background=move_song_frame['background'], foreground='#fff', font=('Consolas', 16), anchor='w').pack(side='top', fill='x', pady=5, padx=10)
        self.move_song_label: ClassVar = Label(move_song_frame, text=f'{self.settings["move_song"]} MOVE PLAYING SONG TO VIEW', background=move_song_frame['background'], foreground='#fff', font=('Consolas', 12), anchor='w')
        self.move_song_label.pack(side='top', fill='x', anchor='center', pady=5, padx=10)
        Radiobutton(move_song_frame, relief='flat', text='ALWAYS', indicatoron=False, font=('corbel', 12), bd=0, background=move_song_frame['background'], foreground='#fff', selectcolor='#212121', takefocus=False,
                    highlightbackground='#222', activebackground='#222', activeforeground='#fff', variable=self.move_song, value='ALWAYS', command=self.change_move_song).pack(side='left', fill='x', expand=True, padx=10, pady=(5, 10), ipady=5)
        Radiobutton(move_song_frame, relief='flat', text='NEVER', indicatoron=False, font=('corbel', 12), bd=0, background=move_song_frame['background'], foreground='#fff', selectcolor='#212121', takefocus=False,
                    highlightbackground='#222', activebackground='#222', activeforeground='#fff', variable=self.move_song, value='NEVER', command=self.change_move_song).pack(side='left', fill='x', expand=True, padx=10, pady=(5, 10), ipady=5)
        Radiobutton(move_song_frame, relief='flat', text='WHILE PLAYLIST IS NOT ACTIVE', indicatoron=False, font=('corbel', 12), bd=0, background=move_song_frame['background'], foreground='#fff', selectcolor='#212121', takefocus=False,
                    highlightbackground='#222', activebackground='#222', activeforeground='#fff', variable=self.move_song, value='WHILE', command=self.change_move_song).pack(side='left', fill='x', expand=True, padx=10, pady=(5, 10), ipady=5)
        move_song_frame.pack(side='top', fill='x', pady=(0, 10))
        # time precision
        time_precision_frame = Frame(self.settings_cards, background='#111')
        Label(time_precision_frame, image=self.time_icon, text=' TIME PRECISION', compound='left', background=time_precision_frame['background'], foreground='#fff', font=('Consolas', 16), anchor='w').pack(side='top', fill='x', pady=5, padx=10)
        self.precision_label: ClassVar = Label(time_precision_frame, text='CURRENT PRECISION: ', background=time_precision_frame['background'], foreground='#fff', font=('Consolas', 12), anchor='w')
        self.precision_label.pack(side='top', fill='x', pady=5, padx=10)
        Radiobutton(time_precision_frame, relief='flat', text='PRECISE', indicatoron=False, font=('corbel', 12), bd=0, background=time_precision_frame['background'], foreground='#fff', selectcolor='#212121', takefocus=False,
                    highlightbackground='#222', activebackground='#222', activeforeground='#fff', variable=self.time_precision, value='PRECISE', command=self.change_precision).pack(side='left', fill='x', expand=True, padx=10, pady=(5, 10), ipady=5)
        Radiobutton(time_precision_frame, relief='flat', text='MORE PRECISE', indicatoron=False, font=('corbel', 12), bd=0, background=time_precision_frame['background'], foreground='#fff', selectcolor='#212121', takefocus=False,
                    highlightbackground='#222', activebackground='#222', activeforeground='#fff', variable=self.time_precision, value='MORE PRECISE', command=self.change_precision).pack(side='left', fill='x', expand=True, padx=10, pady=(5, 10), ipady=5)
        time_precision_frame.pack(side='top', fill='x', pady=(0, 10))
        # after init
        play_frame: ClassVar = Frame(self.settings_cards, background='#111')
        Label(play_frame, image=self.power_icon, text=' STARTUP', compound='left', background=play_frame['background'], foreground='#fff', font=('Consolas', 16), anchor='w').pack(side='top', fill='x', pady=5, padx=10)
        self.startup_label: ClassVar = Label(play_frame, text='ON APP STARTUP: ', background=play_frame['background'], foreground='#fff', font=('Consolas', 12), anchor='w')
        self.startup_label.pack(side='top', fill='x', pady=5, padx=10)
        Radiobutton(play_frame, relief='flat', text='DO NOTHING', indicatoron=False, font=('corbel', 12), bd=0, background=play_frame['background'], foreground='#fff', selectcolor='#212121', takefocus=False,
                    highlightbackground='#222', activebackground='#222', activeforeground='#fff', variable=self.on_startup, value='DO NOTHING', command=self.change_startup).pack(side='left', fill='x', expand=True, padx=10, pady=(5, 10), ipady=5)
        Radiobutton(play_frame, relief='flat', text='PLAY LATEST SONG', indicatoron=False, font=('corbel', 12), bd=0, background=play_frame['background'], foreground='#fff', selectcolor='#212121', takefocus=False,
                    highlightbackground='#222', activebackground='#222', activeforeground='#fff', variable=self.on_startup, value='PLAY LATEST SONG', command=self.change_startup).pack(side='left', fill='x', expand=True, padx=10, pady=(5, 10), ipady=5)
        Radiobutton(play_frame, relief='flat', text='PLAY FIRST SONG', indicatoron=False, font=('corbel', 12), bd=0, background=play_frame['background'], foreground='#fff', selectcolor='#212121', takefocus=False,
                    highlightbackground='#222', activebackground='#222', activeforeground='#fff', variable=self.on_startup, value='PLAY FIRST SONG', command=self.change_startup).pack(side='left', fill='x', expand=True, padx=10, pady=(5, 10), ipady=5)
        play_frame.pack(side='top', fill='x', pady=(0, 10))
        # scroll acceleration
        scroll_frame: ClassVar = Frame(self.settings_cards, background='#111')
        Label(scroll_frame, image=self.slider_icon, text=' SCROLL ACCELERATION', compound='left', background=scroll_frame['background'], foreground='#fff', font=('Consolas', 16), anchor='w').pack(side='top', fill='x', pady=5, padx=10)
        self.acceleration_label: ClassVar = Label(scroll_frame, text=f'VALUE: {self.settings["wheel_acceleration"]}X', background=scroll_frame['background'], foreground='#fff', font=('Consolas', 12), anchor='w')
        self.acceleration_label.pack(side='top', fill='x', anchor='center', pady=5, padx=10)
        Label(scroll_frame, text='SLOW', background=scroll_frame['background'], foreground='#fff', font=('Consolas', 12), anchor='w').pack(side='left', anchor='w', pady=5, padx=10)
        self.acceleration_scale: ClassVar = ttk.Scale(scroll_frame, orient='horizontal', from_=1, to=8, length=8, command=self.change_acceleration)
        self.acceleration_scale.pack(side='left', fill='x', anchor='w', expand=True, pady=5, padx=10)
        Label(scroll_frame, text='FAST', background=scroll_frame['background'], foreground='#fff', font=('Consolas', 12), anchor='w').pack(side='left', anchor='w', pady=(5, 10), padx=10)
        scroll_frame.pack(side='top', fill='x', pady=(0, 10))
        # updater
        update_frame: ClassVar = Frame(self.settings_cards, background='#111')
        Label(update_frame, image=self.update_big_icon, text=' UPDATES', compound='left', background=update_frame['background'], foreground='#fff', font=('Consolas', 16), anchor='w').pack(side='top', fill='x', pady=5, padx=10)
        self.update_label: ClassVar = Label(update_frame, text='CHECK FOR UPDATES: ', background=update_frame['background'], foreground='#fff', font=('Consolas', 12), anchor='w')
        self.update_label.pack(side='top', fill='x', pady=5, padx=10)
        Radiobutton(update_frame, relief='flat', text='YES', indicatoron=False, font=('corbel', 12), bd=0, background=update_frame['background'], foreground='#fff', selectcolor='#212121', takefocus=False,
                    highlightbackground='#222', activebackground='#222', activeforeground='#fff', variable=self.update, value=True, command=self.change_update).pack(side='left', fill='x', expand=True, padx=10, pady=(5, 10), ipady=5)
        Radiobutton(update_frame, relief='flat', text='NO', indicatoron=False, font=('corbel', 12), bd=0, background=update_frame['background'], foreground='#fff', selectcolor='#212121', takefocus=False,
                    highlightbackground='#222', activebackground='#222', activeforeground='#fff', variable=self.update, value=False, command=self.change_update).pack(side='left', fill='x', expand=True, padx=10, pady=(5, 10), ipady=5)
        update_frame.pack(side='top', fill='x', pady=(0, 10))
        # icons
        icons_frame: ClassVar = Frame(self.settings_cards, background='#111')
        Label(icons_frame, image=self.question_mark_icon, text=' ICONS', compound='left', background=icons_frame['background'], foreground='#fff', font=('Consolas', 16), anchor='w').pack(side='top', fill='x', pady=5, padx=10)
        Label(icons_frame, text='Note: Restart needed to apply changes', background=icons_frame['background'], foreground='#fff', font=('Consolas', 12), anchor='w').pack(side='top', fill='x', pady=5, padx=10)
        Radiobutton(icons_frame, relief='flat', text='USE DEFAULT', indicatoron=False, font=('corbel', 12), bd=0, background=icons_frame['background'], foreground='#fff', selectcolor='#212121', takefocus=False,
                    highlightbackground='#222', activebackground='#222', activeforeground='#fff', variable=self.icons_folder, value='icons', command=self.change_icons).pack(side='left', fill='x', expand=True, padx=10, pady=(5, 10), ipady=5)
        Radiobutton(icons_frame, relief='flat', text='USE FLUENT', indicatoron=False, font=('corbel', 12), bd=0, background=icons_frame['background'], foreground='#fff', selectcolor='#212121', takefocus=False,
                    highlightbackground='#222', activebackground='#222', activeforeground='#fff', variable=self.icons_folder, value='fluent_icons', command=self.change_icons).pack(side='left', fill='x', expand=True, padx=10, pady=(5, 10), ipady=5)
        icons_frame.pack(side='top', fill='x', pady=(0, 10))
        # about
        about_frame: ClassVar = Frame(self.settings_cards, background='#111')
        Label(about_frame, image=self.logo_icon, text=' ABOUT SOUNDER', compound='left', background=about_frame['background'], foreground='#fff', font=('Consolas', 16), anchor='w').pack(side='top', fill='x', pady=5, padx=10)
        Label(about_frame, text=f'VERSION: {self.VERSION}', background=about_frame['background'], foreground='#fff', font=('Consolas', 12), anchor='w').pack(side='top', fill='x', pady=5, padx=10)
        Label(about_frame, text=f'ICONS: icons8.com', background=about_frame['background'], foreground='#fff', font=('Consolas', 12), anchor='w').pack(side='top', fill='x', pady=5, padx=10)
        Label(about_frame, text=f'AUTHOR: Mateusz Perczak (Łosiek)', background=about_frame['background'], foreground='#fff', font=('Consolas', 12), anchor='w').pack(side='top', fill='x', pady=5, padx=10)
        Label(about_frame, text=f'LICENCE: MIT', background=about_frame['background'], foreground='#fff', font=('Consolas', 12), anchor='w').pack(side='top', fill='x', pady=(5, 10), padx=10)
        about_frame.pack(side='top', fill='x', pady=(0, 10))
        # end
        # default settings
        default_frame: ClassVar = Frame(self.settings_cards, background='#111')
        Label(default_frame, image=self.restore_icon, text=' DEFAULT SETTINGS', compound='left', background=default_frame['background'], foreground='#fff', font=('Consolas', 16), anchor='w').pack(side='top', fill='x', pady=5, padx=10)
        ttk.Button(default_frame, text='RESTORE DEFAULT SETTINGS', style='restore.TButton', takefocus=False, command=self.default_settings).pack(side='top', fill='x', pady=(5, 10), padx=10)
        default_frame.pack(side='top', fill='x', pady=(0, 10))
        # update canvas
        self.settings_cards.bind('<Expose>', lambda _: self.settings_canvas.configure(scrollregion=self.settings_canvas.bbox('all')))
        self.settings_window: ClassVar = self.settings_canvas.create_window((0, 0), window=self.settings_cards, anchor='nw')
        self.settings_canvas.bind('<Expose>', lambda _: self.settings_canvas.itemconfigure(self.settings_window, width=self.settings_canvas.winfo_width(), height=self.settings_cards.winfo_height()))
        # place widgets
        self.settings_top_frame.pack(side='top', fill='x', ipady=20, pady=10)
        self.settings_scrollbar.pack(side='right', fill='y', pady=(0, 10))
        self.settings_canvas.pack(side='left', fill='both', expand=True, padx=10, pady=(0, 10))
        # end
        # main window stuff
        self.main_window.bind('<MouseWheel>', self.on_mouse)
        self.search_box.bind('<KeyRelease>', self.search_song)
        self.min_size_entry.bind('<KeyRelease>', self.change_file_size)
        self.max_size_entry.bind('<KeyRelease>', self.change_file_size)
        # change how the closing of the program works
        self.main_window.protocol('WM_DELETE_WINDOW', self.close)
        # apply settings
        Thread(target=self.apply_settings, daemon=True).start()
        # show window
        self.main_window.after(150, lambda: self.main_window.deiconify())
        # init sort menu
        self.main_window.after(300, lambda: self.init_sort_menu())
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
            self.music_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\music.png').resize((35, 35)))
            self.cover_art_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\cover_art.png').resize((220, 220)))
            self.playlist_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\playlist.png').resize((35, 35)))
            self.settings_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\settings.png').resize((35, 35)))
            self.folder_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\folder.png').resize((40, 40)))
            self.music_folder_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\music_folder.png').resize((35, 35)))
            self.play_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\play.png').resize((30, 30)))
            self.pause_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\pause.png').resize((30, 30)))
            self.next_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\next.png').resize((30, 30)))
            self.previous_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\previous.png').resize((30, 30)))
            self.plus_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\plus.png').resize((20, 20)))
            self.refresh_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\refresh.png').resize((20, 20)))
            self.search_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\search.png').resize((20, 20)))
            self.close_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\close.png').resize((30, 30)))
            self.record_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\record.png').resize((40, 40)))
            self.note_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\record.png').resize((20, 20)))
            self.play_playlist: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\play.png').resize((20, 20)))
            self.shuffle_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\shuffle.png').resize((25, 25)))
            self.clock_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\clock.png').resize((20, 20)))
            self.repeat_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\repeat.png').resize((25, 25)))
            self.repeat_one_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\repeat_one.png').resize((25, 25)))
            self.warning_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\warning.png').resize((85, 85)))
            self.bug_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\bug.png').resize((35, 35)))
            self.logs_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\logs.png').resize((35, 35)))
            self.no_audio_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\no_audio.png').resize((25, 25)))
            self.audio_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\audio.png').resize((25, 25)))
            self.low_audio_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\low_audio.png').resize((25, 25)))
            self.med_audio_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\med_audio.png').resize((25, 25)))
            self.save_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\save.png').resize((20, 20)))
            self.logo_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\logo.png').resize((40, 40)))
            self.slider_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\slider.png').resize((40, 40)))
            self.restore_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\restore.png').resize((40, 40)))
            self.power_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\power.png').resize((40, 40)))
            self.time_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\time.png').resize((40, 40)))
            self.transition_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\transition.png').resize((40, 40)))
            self.audio_file_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\audio_file.png').resize((40, 40)))
            self.update_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\update.png').resize((20, 20)))
            self.update_big_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\update.png').resize((40, 40)))
            self.menu_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\menu.png').resize((30, 30)))
            self.trash_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\trash.png').resize((20, 20)))
            self.file_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\file.png').resize((25, 25)))
            self.filter_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\filter.png').resize((20, 20)))
            self.sort_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\sort.png').resize((30, 30)))
            self.heart_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\heart.png').resize((30, 30)))
            self.filled_heart_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\filled_heart.png').resize((30, 30)))
            self.arrow_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\arrow.png').resize((40, 40)))
            self.question_mark_icon: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\question_mark.png').resize((40, 40)))
        except Exception as err_obj:
            self.dump_err(err_obj, False)

    def music_card(self, song) -> None:
        try:
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
        except Exception as err_obj:
            self.dump_err(err_obj, False)

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
            self.dump_err(err_obj, True)

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
        Label(folder_frame, text=f'{path}', background='#333', foreground='#fff', font=('Consolas', 12)).place(x=58, rely=0.72, anchor='w')
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
        if bool(new_directory) and not new_directory in self.settings['folders']:
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
            self.stop_all_playback()
            if randint(0, 2) > 0:
                self.easter_egg()

    def open_logs(self) -> None:
        if getLogger().isEnabledFor(ERROR):
            shutdown()
        if isfile("errors.log"):
            startfile("errors.log")

    def dump_err(self, err_obj: ClassVar, critical: bool) -> None:
        if critical:
            self.error_reason['text'] = str(err_obj).strip()
            self.error_frame.lift()
        error(err_obj, exc_info=True)

    def load_settings(self) -> None:
        try:
            if isfile('settings.json'):
                with open('settings.json', 'r') as file:
                    self.settings = load(file)
                    self.settings_correction()
            else:
                self.settings = {'folders': [], 'last_card': 'playback', 'shuffle': False, 'repeat': 'none', 'wheel_acceleration': 1.0, 'width': 750, 'height': 450, 'volume': 0.50, 'song': '', 'on_startup': 'DO NOTHING', 'transition': 0, 'time_precision': 'PRECISE', 'update': True, 'blacklist': [], 'sort_by': 'name', 'favorites': [], 'move_song': 'WHILE', 'icons_folder': 'icons', 'min_file_size': 0, 'max_file_size': 512}
        except Exception as err_obj:
            self.dump_err(err_obj, False)

    def apply_settings(self) -> None:
        try:
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
            # acceleration
            self.acceleration_scale.set(self.settings['wheel_acceleration'])
            # time resolution
            self.time_precision.set(self.settings['time_precision'])
            self.change_precision()
            # transition
            self.transition_scale.set(self.settings['transition'])
            # update
            self.update.set(self.settings['update'])
            self.change_update()
            # move song
            self.move_song.set(self.settings['move_song'])
            self.change_move_song()
            # icons
            self.icons_folder.set(self.settings['icons_folder'])
            self.change_icons()
            # file size
            self.min_size_entry.insert(0, self.settings['min_file_size'])
            self.max_size_entry.insert(0, self.settings['max_file_size'])
            # sort
            self.sort_by.set(self.settings['sort_by'])
            # on startup
            self.on_startup.set(self.settings['on_startup'])
            self.change_startup()
            if self.settings['on_startup'] in ['DO NOTHING', 'PLAY LATEST SONG']:
                if bool(self.playlist):
                    if self.settings['song'] in self.playlist:
                        self.song = self.settings['song']  
                        if self.settings['on_startup'] == 'PLAY LATEST SONG':
                            self.action_play()
            elif self.settings['on_startup'] == 'PLAY FIRST SONG':
                if bool(self.playlist):
                    self.song = self.playlist[0]
                    self.action_play()
            # debugger
            if 'debug' in self.settings:
                if self.settings['debug']:
                    self.main_window.bind('<F12>', lambda _: Debugger(self.main_window))
            # title bar icon
            self.main_window.iconphoto(False, self.logo_icon)
            # check for update
            if bool(self.settings['update']):
                Thread(target=self.check_update, daemon=True).start()
        except Exception as err_obj:
            self.dump_err(err_obj, True)

    def save_settings(self) -> None:
        try:
            with open('settings.json', 'w') as file:
                dump(self.settings, file)
        except Exception as err_obj:
            self.dump_err(err_obj, False)

    def settings_correction(self) -> None:
        frames: list = ['playback', 'playlist', 'folder', 'settings']
        try:
            self.settings['last_card']
        except Exception as err_obj:
            self.dump_err(err_obj, False)
            self.settings['last_card'] = ''
        finally:
            if not self.settings['last_card'] in frames:
                self.settings['last_card']: str = 'playback'
        try:
            self.settings['folders']
        except Exception as err_obj:
            self.dump_err(err_obj, False)
            self.settings['folders']: list = []
        try:
            self.settings['shuffle']
        except Exception as err_obj:
            self.dump_err(err_obj, False)
            self.settings['shuffle']: bool = False
        try:
            self.settings['repeat']
        except Exception as err_obj:
            self.dump_err(err_obj, False)
            self.settings['repeat']: str = 'none'
        try:
            self.settings['wheel_acceleration']
        except Exception as err_obj:
            self.dump_err(err_obj, False)
            self.settings['wheel_acceleration']: float = 1.0 
        try:
            self.settings['width']
        except Exception as err_obj:
            self.dump_err(err_obj, False)
            self.settings['width']: int = 750
        try:
            self.settings['height']
        except Exception as err_obj:
            self.dump_err(err_obj, False)
            self.settings['height']: int = 450
        try:
            self.settings['volume']
        except Exception as err_obj:
            self.dump_err(err_obj, False)
            self.settings['volume']: float = 0.50
        try:
            self.settings['song']
        except Exception as err_obj:
            self.dump_err(err_obj, False)
            self.settings['song']: str = ''
        try:
            self.settings['on_startup']
        except Exception as err_obj:
            self.dump_err(err_obj, False)
            self.settings['on_startup']: str = 'DO NOTHING'
        try:
            self.settings['time_precision']
        except Exception as err_obj:
            self.dump_err(err_obj, False)
            self.settings['time_precision']: str = 'PRECISE'
        try:
            self.settings['transition']
        except Exception as err_obj:
            self.dump_err(err_obj, False)
            self.settings['transition']: int = 0
        try:
            self.settings['update']
        except Exception as err_obj:
            self.dump_err(err_obj, False)
            self.settings['update']: bool = True
        try:
            if 'version' in self.settings:
                del self.settings['version']
        except Exception as err_obj:
            self.dump_err(err_obj, False)
        try:
            self.settings['blacklist']
        except Exception as err_obj:
            self.dump_err(err_obj, False)
            self.settings['blacklist']: list = []
        try:
            self.settings['sort_by']
        except Exception as err_obj:
            self.dump_err(err_obj, False)
            self.settings['sort_by']: str = 'name'
        try:
            self.settings['favorites']
        except Exception as err_obj:
            self.dump_err(err_obj, False)
            self.settings['favorites']: list = []
        try:
            self.settings['move_song']
        except Exception as err_obj:
            self.dump_err(err_obj, False)
            self.settings['move_song']: str = 'ALWAYS'
        try:
            self.settings['icons_folder']
        except Exception as err_obj:
            self.dump_err(err_obj, False)
            self.settings['icons_folder']: str = 'icons'
        try:
            self.settings['min_file_size']
        except Exception as err_obj:
            self.dump_err(err_obj, False)
            self.settings['min_file_size']: int = 0
        try:
            self.settings['max_file_size']
        except Exception as err_obj:
            self.dump_err(err_obj, False)
            self.settings['max_file_size']: int = 512
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
        supported_extensions: tuple = ('.mp3')
        self.songs = []
        min_size: int = self.settings['min_file_size'] * 1000000
        max_size: int = self.settings['max_file_size'] * 1000000
        try:
            for folder in self.settings['folders']:
                for file in listdir(folder):
                    if splitext(file)[1] in supported_extensions and not file in self.settings['blacklist'] and min_size < getsize(abspath(join(folder, file))) < max_size:
                        self.songs.append(abspath(join(folder, file)))
            del supported_extensions, min_size, max_size
            self.playlist = self.songs
            self.active_card = []
            self.sort_songs()
            self.get_metadata()
            self.add_songs()
            self.update_lenght()
            self.update_num_of_songs()
            self.update_state()
            self.update_active_card()
            self.move_to_view()
        except Exception as err_obj:
            self.dump_err(err_obj, False)

    def refresh_songs(self) -> None:
        self.playlist_canvas.itemconfigure(self.playlist_window, width=self.playlist_canvas.winfo_width(), height=len(self.playlist) * 71)
        self.move_to_view()

    def add_songs(self) -> None:
        self.remove_music_cards()
        for song in self.songs:
            try:
                self.music_card(song)
            except Exception as err_obj:
                error(err_obj, exc_info=True)
        if not bool(self.songs):
            self.info_card(f'WE ARE UNABLE TO FIND ANY SONG', self.playlist_cards)

    def validate_search_entry(self, char: str, _) -> bool:
        try:
            disallowed_chars: tuple = ('}', '{', ']', '[', '+', '=', '|', '\\', ':', ';', '/', '?', '>', '<', '%', '(', ')', '*', '^')
            if not bool(char) or len(char) > 1:
                del disallowed_chars
                return True
            if char in disallowed_chars:
                self.main_window.bell()
                del disallowed_chars
                return False
            del disallowed_chars
            return True
        except Exception as err_obj:
            self.dump_err(err_obj, True)

    def validate_size_entry(self, char: str, _) -> bool:
        if char.isdigit():
            return True
        return False

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
        self.move_to_view()
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
            self.sort_button.state(['disabled'])
            self.favorites_button.state(['disabled'])
        else:
            self.playlist_play.state(['!disabled'])
            self.shuffle_button.state(['!disabled'])
            self.play_button.state(['!disabled'])
            self.previous_button.state(['!disabled'])
            self.next_button.state(['!disabled'])
            self.repeat_button.state(['!disabled'])
            self.sort_button.state(['!disabled'])
            self.favorites_button.state(['!disabled'])

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
        self.move_to_view()

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
        if self.settings['shuffle'] and len(self.playlist) > 1:
            shuffle(self.songs)
        else:
            if self.settings['sort_by'] == 'name':
                self.songs.sort(key=self.sort_by_letter)
            elif self.settings['sort_by'] == 'favorites':
                self.songs.sort(key=self.sort_by_favorites)

    def sort_by_letter(self, song: str) -> str:
        return splitext(basename(song))[0].split(' ')[0].lower()

    def sort_by_favorites(self, song: str) -> str:
        if basename(song) in self.settings['favorites']:
            return 'A'
        return 'Z'

    def get_playtime(self) -> None:
        play_time: float = 0.0
        for song in self.playlist:
            if self.songs_metadata[song][0] is not None:
                play_time += self.songs_metadata[song][0].info.length
        self.play_time: ClassVar = timedelta(seconds=int(play_time))
        del play_time

    def init_mixer(self) -> None:
        try:
            mixer.pre_init(44100, -16, 2, 1024)
            mixer.init()
        except Exception as err_obj:
            self.dump_err(err_obj, True)

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
        try:
            for widget in self.active_card:
                if widget not in self.get_all_widgets(self.playlist_cards):
                    self.active_card.remove(widget)
                else:
                    for widget in self.active_card:
                        widget.configure(image=self.play_icon)
                        self.active_card.remove(widget)
            if  mixer.music.get_busy() and bool(self.song) and bool(self.playlist) and self.song in self.songs_metadata and self.songs_metadata[self.song][1] in self.get_all_widgets(self.playlist_cards) and not self.paused:
                self.songs_metadata[self.song][1].configure(image=self.pause_icon)
                self.active_card.append(self.songs_metadata[self.song][1])
        except Exception as err_obj:
            self.dump_err(err_obj, True)

    def update_play_button(self) -> None:
        if mixer.music.get_busy() and self.paused:
            self.play_button.configure(image=self.play_icon)
        elif mixer.music.get_busy() and not self.paused:
           self.play_button.configure(image=self.pause_icon)
        else:
            self.play_button.configure(image=self.play_icon)

    def update_favorite_button(self) -> None:
        if basename(self.song) in self.settings['favorites']:
            self.favorites_button.configure(image=self.filled_heart_icon)
        else:
            self.favorites_button.configure(image=self.heart_icon)

    def action_play(self) -> None:
        if bool(self.playlist) or bool(self.songs):
            if mixer.music.get_busy():
                if self.paused:
                    Thread(target=self.unpause_song, daemon=True).start()
                else:
                    Thread(target=self.pause_song, daemon=True).start()
            elif bool(self.song):
                Thread(target=self.play_song, daemon=True).start()
            else:
                self.song = self.playlist[0]
                Thread(target=self.play_song, daemon=True).start()

    def action_next(self) -> None:
        if bool(self.song):
            if bool(self.playlist) and self.song in self.playlist:
                if (self.playlist.index(self.song) + 1) < len(self.playlist):
                    self.song = self.playlist[self.playlist.index(self.song) + 1]
                    Thread(target=self.play_song, daemon=True).start()
                else:
                    self.song = self.playlist[0]
                    Thread(target=self.play_song, daemon=True).start()
            elif bool(self.songs) and self.song in self.songs:
                if (self.songs.index(self.song) + 1) < len(self.songs):
                    self.song = self.songs[self.songs.index(self.song) + 1]
                else:
                    self.song = self.songs[0]
                    Thread(target=self.play_song, daemon=True).start()
        else:
            Thread(target=self.play_song, daemon=True).start()
    
    def action_prev(self) -> None:
        if bool(self.song):
            if bool(self.playlist) and self.song in self.playlist:
                if (self.playlist.index(self.song) - 1) >= 0:
                    self.song = self.playlist[self.playlist.index(self.song) - 1]
                    Thread(target=self.play_song, daemon=True).start()
            elif bool(self.songs) and self.song in self.songs:
                if (self.songs.index(self.song) - 1) >= 0:
                    self.song = self.songs[self.songs.index(self.song) - 1]
                    Thread(target=self.play_song, daemon=True).start()
        else:
            Thread(target=self.play_song, daemon=True).start()

    def action_card(self, song) -> None:
        if bool(self.playlist):
            if song == self.song and mixer.music.get_busy():
                if self.paused:
                    Thread(target=self.unpause_song, daemon=True).start()
                else:
                    Thread(target=self.pause_song, daemon=True).start()
            else:
                self.song = song
                Thread(target=self.play_song, daemon=True).start()
    
    def action_all(self) -> None:
        if bool(self.playlist):
            self.song = self.playlist[0]
            Thread(target=self.play_song, daemon=True).start()

    def move_to_view(self) -> None:
        if bool(self.playlist) and bool(self.song) and self.song in self.playlist:
            self.playlist_canvas.yview_moveto(float((self.playlist.index(self.song) * 71) / self.playlist_cards.winfo_height()))

    def play_song(self) -> None:
        try:
            if bool(self.song) and bool(self.playlist) or bool(self.songs):
                mixer.music.load(self.song)
                mixer.music.play()
                self.paused = False
                Thread(target=self.update_songs_metadata, daemon=True).start()
                self.update_active_card()
                self.update_play_button()
                self.update_favorite_button()
                if active_count() == 1 or not any(thread for thread in enum_threads() if 'PlayThread' == thread.getName()):
                    Thread(target=self.play_thread, daemon=True, name='PlayThread').start()
                if self.settings['move_song'] == 'ALWAYS':
                    self.move_to_view()
                elif self.settings['move_song'] == 'WHILE':
                    SELECTED: str = self.selected.get()
                    if SELECTED != 'playlist':
                        self.move_to_view()
                    del SELECTED
        except Exception as err_obj:
            self.dump_err(err_obj, False)

    def pause_song(self) -> None:
        if mixer.music.get_busy() and bool(self.songs):
            mixer.music.pause()
            self.paused = True
            self.update_active_card()
            self.update_play_button()

    def unpause_song(self) -> None:
        if mixer.music.get_busy() and bool(self.songs):
            mixer.music.unpause()
            self.paused = False
            self.update_active_card()
            self.update_play_button()

    def stop_all_playback(self) -> None:
        if mixer.music.get_busy():
            mixer.music.stop()
        mixer.music.unload()
        self.paused = False
        self.update_play_button()
        self.update_favorite_button()

    def play_thread(self) -> None:
        try:
            position: float = 0.0
            minute: float = 0.0
            second: float = 0.0
            while mixer.music.get_busy() and bool(self.song):
                position = mixer.music.get_pos() / 1000
                self.progress_bar['value'] = position
                minute, second = divmod(position, 60)
                if self.settings['time_precision'] == 'PRECISE':
                    self.time_passed['text'] = f'{int(minute)}:{str(int(second)).zfill(2)}'
                    sleep(0.1)
                else:
                    self.time_passed['text'] = f'{int(minute)}:{str(int(second)).zfill(2)}:{str(second)[3:7].zfill(4)}'
                    sleep(0.01)
            del position, minute, second
            if self.settings['transition'] == 0:
                self.main_window.after(250, self.after_play)
            else:
                self.main_window.after((self.settings['transition'] * 1000), self.after_wait)
        except Exception as err_obj:
            self.dump_err(err_obj, True)

    def update_songs_metadata(self) -> None:
        if bool(self.song):
            if self.songs_metadata[self.song][0] is not None:
                if 'APIC:' in self.songs_metadata[self.song][0]:
                    self.new_cover_art_icon: ClassVar = ImageTk.PhotoImage(Image.open(BytesIO(self.songs_metadata[self.song][0].get("APIC:").data)).resize((220, 220)))
                    self.cover_art.configure(image=self.new_cover_art_icon)
                    self.main_window.iconphoto(False, self.new_cover_art_icon)
                else:
                    self.cover_art.configure(image=self.cover_art_icon)
                    self.main_window.iconphoto(False, self.cover_art_icon)
                if 'TIT2' in self.songs_metadata[self.song][0]:
                    self.song_name['text'] = f'{self.songs_metadata[self.song][0]["TIT2"]}'
                else:
                    self.song_name['text'] = splitext(basename(self.song))[0]
                if 'TPE1' in self.songs_metadata[self.song][0]:
                    self.song_artist['text'] = f'{self.songs_metadata[self.song][0]["TPE1"]}'
                else:
                    self.song_artist['text'] = 'Unknown'
                if 'TALB' in self.songs_metadata[self.song][0]:
                    self.album_name['text'] = f'{self.songs_metadata[self.song][0]["TALB"]}'
                else:
                    self.album_name['text'] = 'Unknown'
                length: float = self.songs_metadata[self.song][0].info.length
                self.progress_bar['maximum'] = length
                minute, second = divmod((length), 60)
                if self.settings['time_precision'] == 'PRECISE':
                    self.song_length['text'] = f'{int(minute)}:{str(int(second)).zfill(2)}'
                else:
                    self.song_length['text'] = f'{int(minute)}:{str(int(second)).zfill(2)}:{str(second)[3:7].zfill(4)}'
                del length, minute, second
            else:
                self.song_name['text'] = 'Unknown'
                self.song_artist['text'] = 'Unknown'
                self.album_name['text'] = 'Unknown'
                self.song_length['text'] = '--:--'
                self.progress_bar['maximum'] = 99999999
                self.progress_bar['value'] = 0

    def after_wait(self) -> None:
        if not mixer.music.get_busy():
            self.main_window.after(250, self.after_play())

    def after_play(self) -> None:
        try:
            if bool(self.songs) or bool(self.playlist):
                if self.settings['repeat'] == 'one':
                    Thread(target=self.play_song, daemon=True).start()
                elif self.settings['repeat'] == 'all' and bool(self.playlist):
                    if bool(self.song):
                        if self.song in self.playlist and (self.playlist.index(self.song) + 1) < len(self.playlist):
                            self.song = self.playlist[self.playlist.index(self.song) + 1]
                            Thread(target=self.play_song, daemon=True).start()
                        else:
                            self.song = self.playlist[0]
                            Thread(target=self.play_song, daemon=True).start()
                    else:
                        Thread(target=self.play_song, daemon=True).start()
                elif self.settings['repeat'] == 'all' and bool(self.songs):
                    if bool(self.song):
                        if (self.songs.index(self.song) + 1) < len(self.songs) and self.song in self.songs:
                            self.song = self.songs[self.songs.index(self.song) + 1]
                            Thread(target=self.play_song, daemon=True).start()
                        else:
                            self.song = self.songs[0]
                            Thread(target=self.play_song, daemon=True).start()
                    else:
                        Thread(target=self.play_song, daemon=True).start()
                elif self.settings['repeat'] == 'none':
                    self.update_active_card()
                    self.update_play_button()
        except Exception as err_obj:
            self.dump_err(err_obj, True)

    def change_acceleration(self, event) -> None:
        self.settings['wheel_acceleration'] = round(float(event), 2)
        self.acceleration_label['text'] = f'VALUE: {self.settings["wheel_acceleration"]}X'

    def default_settings(self) -> None:
        if askyesno('SOUNDER', f'Are you sure you want to restore default settings?', icon='warning'):
            self.settings = {'folders': [], 'last_card': 'playback', 'shuffle': False, 'repeat': 'none', 'wheel_acceleration': 1.0, 'width': 750, 'height': 450, 'volume': 0.50, 'song': '', 'on_startup': 'DO NOTHING', 'transition': 0, 'time_precision': 'PRECISE', 'update': True, 'blacklist': [], 'sort_by': 'name', 'favorites': [], 'move_song': 'WHILE', 'icons_folder': 'icons', 'min_file_size': 0, 'max_file_size': 512}
            self.close()
    
    def change_startup(self) -> None:
        value: str = self.on_startup.get()
        self.settings['on_startup'] = value
        self.startup_label['text'] = f'ON APP STARTUP: {value}'
        del value

    def change_precision(self) -> None:
        value: str = self.time_precision.get()
        self.settings['time_precision'] = value
        if value == 'PRECISE':
            self.precision_label['text'] = f'CURRENT PRECISION: {value} (0:00)'
        else:
            self.precision_label['text'] = f'CURRENT PRECISION: {value} (0:00:0000)'
        if bool(self.song):
            Thread(target=self.update_songs_metadata, daemon=True).start()
        del value

    def change_transition(self, event) -> None:
        self.settings['transition'] = int(float(event))
        self.transition_label['text'] = f'VALUE: {self.settings["transition"]}s'

    def change_update(self) -> None:
        self.settings['update'] = self.update.get()
        if bool(self.settings['update']):
            self.update_label['text'] = 'CHECK FOR UPDATES: YES'
        else:
            self.update_label['text'] = 'CHECK FOR UPDATES: NO'

    def check_update(self) -> None:
        try:
            server_version: str = get('https://raw.githubusercontent.com/losek1/Sounder4/master/updates/version.txt').text
            if int(self.VERSION.replace('.', '')) < int(server_version.replace('.', '')):
                ttk.Button(self.settings_top_frame, image=self.update_icon, text='UPDATE', style='folder.TButton', takefocus=False, compound='left', command=lambda: open_browser('https://github.com/losek1/Sounder4/releases', new=0, autoraise=True)).place(x=167, rely=0.5, anchor='w', height=35)
            del server_version
        except Exception as err_obj:
            self.dump_err(err_obj, False)  

    def open_music_menu(self) -> None:
        try:
            if self.button_frame.winfo_ismapped():
                self.button_frame.pack_forget()
                self.menu_frame.configure(width=1)  
            else:
                self.button_frame.pack(side='left', fill='y', padx=10, pady=(0, 10))
        except Exception as err_obj:
            self.dump_err(err_obj, False)

    def manage_song(self, delete: bool) -> None:
        try:
            if bool(self.song) and isfile(self.song):
                msg: tuple = ('remove', 'delete')
                song: str = self.song
                if askyesno('SOUNDER', f'Are you sure you want to {msg[int(delete)]} {song}?', icon='warning'):
                    if mixer.music.get_busy():
                        mixer.music.unload()
                        self.main_window.after(500, self.action_play)
                    if delete:
                        rmfile(song)
                    else:
                        self.settings['blacklist'].append(basename(song))
                    if len(self.playlist) > 1:
                        if self.playlist.index(song) < len(self.playlist):
                            self.song = self.playlist[self.playlist.index(song) + 1]
                        else:
                            self.song = self.playlist[0]
                    elif len(self.songs) > 1:
                        self.song = self.songs[0]
                    if song in self.playlist:
                        self.playlist.remove(song)
                    if song in self.songs:
                        self.songs.remove(song)
                    self.add_songs()
                    self.refresh_songs()
                    self.update_active_card()
                del msg, song
        except Exception as err_obj:
            self.dump_err(err_obj, False)

    def init_sort_menu(self) -> None:
            self.sort_menu: ClassVar = Toplevel()
            self.sort_menu.withdraw()
            self.sort_menu.configure(background='#111')
            self.sort_menu.title('SORT BY')
            self.sort_menu.iconbitmap(f'{self.settings["icons_folder"]}\\filter.ico')
            self.sort_menu.resizable(False, False)
            self.sort_menu.protocol('WM_DELETE_WINDOW', self.sort_menu.withdraw)
            self.sort_menu.focus_force()
            Radiobutton(self.sort_menu, relief='flat', image=self.sort_icon, text=' NAME', font=('Consolas', 14), compound='left', indicatoron=False, bd=0, background='#111', foreground='#fff', selectcolor='#212121', takefocus=False, highlightbackground='#222', activebackground='#222', activeforeground='#fff', variable=self.sort_by, value='name', command=self.change_sort, anchor='w').pack(fill='x', padx=10, pady=(10, 0), ipady=2)
            Radiobutton(self.sort_menu, relief='flat', image=self.filled_heart_icon, text=' FAVORITES', font=('Consolas', 14), compound='left', indicatoron=False, bd=0, background='#111', foreground='#fff', selectcolor='#212121', takefocus=False, highlightbackground='#222', activebackground='#222', activeforeground='#fff', variable=self.sort_by, value='favorites', command=self.change_sort, anchor='w').pack(fill='x', padx=10, pady=(10, 0), ipady=2)
            self.sort_menu.mainloop()

    def open_sort_menu(self) -> None:
        if bool(self.songs):
            if self.sort_menu.winfo_ismapped():
                self.sort_menu.withdraw()
            else:
                self.sort_menu.geometry(f'300x110+{int(self.main_window.winfo_x() + ((self.main_window.winfo_width() - 300) / 2))}+{int(self.main_window.winfo_y() + ((self.main_window.winfo_height() - 110) / 2))}')
                self.sort_menu.deiconify()
                
    def change_sort(self) -> None:
        self.settings['sort_by'] = self.sort_by.get()
        if not self.settings['shuffle']:
            self.sort_songs()
            self.add_songs()
            self.search_song()
            self.update_active_card()
            self.move_to_view()

    def add_favorites(self) -> None:
        if basename(self.song) in self.settings['favorites']:
            self.settings['favorites'].remove(basename(self.song))
        else:
            self.settings['favorites'].append(basename(self.song))
        self.update_favorite_button()
        Thread(target=self.change_sort, daemon=True).start()

    def change_move_song(self) -> None:
        value: str = self.move_song.get()
        self.settings['move_song'] = value
        if value == 'ALWAYS':
            self.move_song_label['text'] = 'ALWAYS MOVE PLAYING SONG TO VIEW'
        elif value == 'NEVER':
            self.move_song_label['text'] = 'NEVER MOVE PLAYING SONG TO VIEW'
        elif value == 'WHILE':
            self.move_song_label['text'] = 'WHILE PLAYLIST IS NOT ACTIVE MOVE PLAYING SONG TO VIEW'
        del value

    def easter_egg(self) -> None:
        if isfile(f'{self.settings["icons_folder"]}\\xx.png') and not bool(self.songs):
            self.mrt: ClassVar = ImageTk.PhotoImage(Image.open(f'{self.settings["icons_folder"]}\\xx.png').resize((220, 220)))
            self.cover_art.configure(image=self.mrt)
            self.song_name['text'] = 'To all of the queens who are fighting alone!'
            self.song_artist['text'] = "Stay strong, keep fighting!"
            self.album_name['text'] = 'HI :D'

    def change_icons(self) -> None:
        self.settings['icons_folder'] = self.icons_folder.get()

    def change_file_size(self, _) -> None:
        try:
            min_size: str = self.min_size_entry.get()
            max_size: str = self.max_size_entry.get()
            if bool(min_size):
                self.settings['min_file_size'] = int(min_size)
            if bool(max_size):
                self.settings['max_file_size'] = int(max_size)
            del min_size, max_size
        except Exception as err_obj:
            self.dump_err(err_obj, False)


if __name__ == '__main__':
        Sounder()


