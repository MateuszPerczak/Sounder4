from tkinter import Toplevel, Label, Button, ttk, Frame, Canvas, Scrollbar, Entry, Tk, PhotoImage
from typing import ClassVar
from traceback import format_exc

class Debugger:
    def __init__(self, parent) -> None:
        self.parent = parent
        del parent
        self.main_window: ClassVar = Toplevel(self.parent)
        self.disallowed_windows: list = [self.main_window.winfo_id()]
        # hide window
        self.main_window.withdraw()
        # window style
        self.main_window.configure(background='#212121')
        self.main_theme: ClassVar = ttk.Style()
        self.main_theme.theme_use('clam')
        self.main_theme.layout('debugger.TEntry',[('Entry.padding', {'children': [('Entry.textarea', {'sticky': 'nswe'})],'sticky': 'nswe'})])
        self.main_theme.configure('debugger.TEntry', background='#111',  foreground='#fff', fieldbackground='#111', selectforeground='#fff', selectbackground='#333')
        self.main_theme.configure('debugger.small.TButton', background='#111', relief='flat', font=('Consolas', 9), foreground='#fff')
        self.main_theme.map('debugger.small.TButton', background=[('pressed', '!disabled', '#111'), ('active', '#151515')])
        self.main_theme.configure('debugger.TButton', background='#111', relief='flat', font=('Consolas', 12), foreground='#fff')
        self.main_theme.map('debugger.TButton', background=[('pressed', '!disabled', '#111'), ('active', '#151515')])
        self.main_theme.configure('debugger.Vertical.TScrollbar', gripcount=0, relief='flat', background='#333', darkcolor='#111', lightcolor='#111', troughcolor='#111', bordercolor='#111', arrowcolor='#333')
        self.main_theme.layout('debugger.Vertical.TScrollbar',[('Vertical.Scrollbar.trough', {'children': [('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})], 'sticky': 'ns'})])
        self.main_theme.map('debugger.Vertical.TScrollbar', background=[('pressed', '!disabled', '#313131'), ('disabled', '#111'), ('active', '#313131'), ('!active', '#333')])
        # window attributes
        self.main_window.attributes("-topmost", True)
        self.main_window.title(f'DEBUGGING: {self.parent.title()}')
        # self.main_window.geometry('665x800')
        self.main_window.minsize(665, 500)
        self.main_window.protocol('WM_DELETE_WINDOW', self.close_debugger)
        # variables
        self.widget: ClassVar = None
        self.highlighted_elements: dict = {}
        self.inspecting: bool = False
        self.allow_self_debug = False
        self.blank_photo: ClassVar = PhotoImage(height=16, width=16)
        self.blank_photo.blank()
        self.main_window.iconphoto(False, self.blank_photo)
        # content
        top_frame: ClassVar = Frame(self.main_window, background=self.main_window['background'])
        # inspect button
        self.inspect_button: ClassVar = ttk.Button(top_frame, text='INSPECT ELEMENT', takefocus=False, style='debugger.TButton', command=self.toggle_inspect)
        self.inspect_button.pack(side='left', padx=(10, 0), pady=10)
        self.inspect_next_button: ClassVar = ttk.Button(top_frame, text='INSPECT NEXT', takefocus=False, style='debugger.TButton', command=self.inspect_next)
        self.inspect_next_button.state(['disabled'])
        self.inspect_next_button.pack(side='left', padx=(10, 0), pady=10)
        self.widgets_label: ClassVar = Label(top_frame, text=f'{len(self.get_all_widgets(self.parent))} WIDGETS', background='#111', foreground='#fff', font=('Consolas', 12))
        self.widgets_label.pack(side='left', padx=(10, 0), pady=10, ipady=5, ipadx=5)
        self.refresh_button: ClassVar = ttk.Button(top_frame, text='REFRESH', takefocus=False, style='debugger.TButton', command=lambda: self.inspect_widget(self.widget))
        self.refresh_button.state(['disabled'])
        self.refresh_button.pack(side='left', padx=(10, 0))
        self.mode_label: ClassVar = Label(top_frame, text='NORMAL', background='#111', foreground='#fff', font=('Consolas', 12))
        self.mode_label.pack(side='left', padx=10, ipady=5, ipadx=5)
        top_frame.pack(side='top', fill='x')
        mid_frame: ClassVar = Frame(self.main_window, background=self.main_window['background'])
        widget_frame: ClassVar = Frame(mid_frame, background='#333')
        Label(widget_frame, text='WIDGET CLASS, NAME', background=widget_frame['background'], foreground='#fff', font=('Consolas', 12), anchor='w').pack(side='top', fill='x', padx=5, pady=(5, 0))
        self.widget_name: ClassVar = Label(widget_frame, text='', background='#111', foreground='#fff', anchor='w', font=('Consolas', 12))
        self.widget_name.pack(side='top', fill='x', padx=5, pady=5)
        Label(widget_frame, text='WIDGET DIMENTIONS', background=widget_frame['background'], foreground='#fff', font=('Consolas', 12), anchor='w').pack(side='top', fill='x', padx=5, pady=(5, 0))
        self.widget_dimensions: ClassVar = Label(widget_frame, text='', background='#111', foreground='#fff', anchor='w', font=('Consolas', 12))
        self.widget_dimensions.pack(side='top', fill='x', padx=5, pady=5)
        Label(widget_frame, text='WIDGET MANAGER', background=widget_frame['background'], foreground='#fff', font=('Consolas', 12), anchor='w').pack(side='top', fill='x', padx=5, pady=(5, 0))
        self.widget_manager: ClassVar = Label(widget_frame, text='', background='#111', foreground='#fff', anchor='w', font=('Consolas', 12))
        self.widget_manager.pack(side='top', fill='x', padx=5, pady=5)
        Label(widget_frame, text='MANAGER CONFIG', background=widget_frame['background'], foreground='#fff', font=('Consolas', 12), anchor='w').pack(side='top', fill='x', padx=5, pady=(5, 0))
        self.manager_config: ClassVar = Label(widget_frame, text='', background='#111', foreground='#fff', anchor='w', font=('Consolas', 12))
        self.manager_config.pack(side='top', fill='x', padx=5, pady=5)
        Label(widget_frame, text='WIDGET PARENT', background=widget_frame['background'], foreground='#fff', font=('Consolas', 12), anchor='w').pack(side='top', fill='x', padx=5, pady=(5, 0))
        parent_frame: ClassVar = Frame(widget_frame, background=widget_frame['background'])
        self.widget_perent: ClassVar = Label(parent_frame, text='', background='#111', foreground='#fff', anchor='w', font=('Consolas', 12))
        self.widget_perent.pack(side='left', fill='x', expand=True)
        self.inspect_perent: ClassVar = ttk.Button(parent_frame, text='INSPECT', takefocus=False, style='debugger.small.TButton', command=lambda: self.inspect_widget(self.widget._nametowidget(self.widget.winfo_parent())))
        self.inspect_perent.state(['disabled'])
        self.inspect_perent.pack(side='left', fill='x', padx=5)
        parent_frame.pack(side='top', fill='x', padx=5, pady=(5, 0))
        Label(widget_frame, text='WIDGET BINDINGS', background=widget_frame['background'], foreground='#fff', font=('Consolas', 12), anchor='w').pack(side='top', fill='x', padx=5, pady=(5, 0))
        self.widget_bindings: ClassVar = Label(widget_frame, text='', background='#111', foreground='#fff', anchor='w', font=('Consolas', 12))
        self.widget_bindings.pack(side='top', fill='x', padx=5, pady=5)
        Label(widget_frame, text='WIDGET PROPERTIES', background=widget_frame['background'], foreground='#fff', font=('Consolas', 12), anchor='w').pack(side='top', fill='x', padx=5, pady=(5, 0))
        properties_frame: ClassVar = Frame(widget_frame, background=widget_frame['background'])
        properties_text: ClassVar = Frame(properties_frame, background=properties_frame['background'])
        Label(properties_text, text='WIDGET TEXT:', background='#111', foreground='#fff', anchor='w', font=('Consolas', 12)).pack(side='left', fill='x')
        self.entry: ClassVar = ttk.Entry(properties_text, style='debugger.TEntry', font=('Consolas', 12))
        self.entry.state(['disabled'])
        self.entry.pack(side='left', fill='x', ipady=2, expand=True, padx=(5, 0))
        self.apply_button: ClassVar = ttk.Button(properties_text, text='APPLY', takefocus=False, style='debugger.small.TButton', command=self.apply_changes)
        self.apply_button.state(['disabled'])
        self.apply_button.pack(side='left', fill='x', padx=5)
        properties_text.pack(side='top', fill='x', pady=(0, 5))
        properties_image: ClassVar = Frame(properties_frame, background=properties_frame['background'])
        Label(properties_image, text='WIDGET IMG:', background='#111', foreground='#fff', anchor='w', font=('Consolas', 12)).pack(side='left', fill='x')
        self.widget_image: ClassVar = ttk.Button(properties_image, text='OPEN IMAGE', takefocus=False, style='debugger.small.TButton', command=self.open_image)
        self.widget_image.state(['disabled'])
        self.widget_image.pack(side='left', fill='x', padx=5)
        properties_image.pack(side='top', fill='x', pady=(0, 5))
        properties_function: ClassVar = Frame(properties_frame, background=properties_frame['background'])
        Label(properties_function, text='WIDGET FUNCTION:', background='#111', foreground='#fff', anchor='w', font=('Consolas', 12)).pack(side='left', fill='x')
        self.widget_function: ClassVar = ttk.Button(properties_function, text='CALL FUNCTION', takefocus=False, style='debugger.small.TButton', command=self.call_function)
        self.widget_function.state(['disabled'])
        self.widget_function.pack(side='left', fill='x', padx=5)
        properties_function.pack(side='top', fill='x')
        properties_frame.pack(side='top', fill='x', padx=5, pady=(5, 0))
        Label(widget_frame, text='WIDGET CHILDRENS', background=widget_frame['background'], foreground='#fff', font=('Consolas', 12), anchor='w').pack(side='top', fill='x', padx=5, pady=(5, 0))
        canvas_frame: ClassVar = Frame(widget_frame, background=widget_frame['background'])
        scrollbar: ClassVar = ttk.Scrollbar(canvas_frame, style='debugger.Vertical.TScrollbar')
        self.canvas: ClassVar = Canvas(canvas_frame, borderwidth=0, highlightthickness=0, background='#111', yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.canvas.yview)
        self.canvas_cards: ClassVar = Frame(self.canvas, background=self.canvas['background'])
        self.canvas_cards.bind('<Configure>', lambda _: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas_window: ClassVar = self.canvas.create_window((0, 0), window=self.canvas_cards, anchor='nw')
        self.canvas.bind('<Configure>', lambda _: self.canvas.itemconfigure(self.canvas_window, width=self.canvas.winfo_width(), height=len(self.canvas_cards.winfo_children()) * 51))
        self.canvas.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10, padx=(0, 10))
        canvas_frame.pack(side='top', fill='both', expand=True)
        widget_frame.pack(side='top', fill='both', expand=True, padx=10)
        mid_frame.pack(side='top', fill='both', expand=True)
        Label(self.main_window, text='DEBUGGER BY MATEUSZ PERCZAK (Łosiek)', background='#111', foreground='#fff', font=('Consolas', 12), anchor='w').pack(side='top', fill='x', padx=10, pady=(10, 0))
        # show window
        self.main_window.bind('<MouseWheel>', self.on_mouse)
        self.entry.bind('<KeyRelease>', self.entry_diff)
        self.main_window.after(100, self.init_img_window)
        self.main_window.after(150, lambda: self.inspect_widget(self.parent))
        self.check_bind_collisions()
        self.main_window.deiconify()
        self.show_window()
        self.main_window.mainloop()

    def check_bind_collisions(self) -> None:
        parent_binds: tuple = self.parent.bind()
        if parent_binds:
            message: str = ''
            if '<Configure>' in parent_binds:
                message += '<Configure>, '
            else:
                self.parent.bind('<Configure>', lambda _: self.load_properties())
            if '<Motion>' in parent_binds:
                message += '<Motion>, '
                self.inspect_button.state(['disabled'])
            if '<Button-1>' in parent_binds:
                message += '<Button-1> '
                self.inspect_button.state(['disabled'])
            if '<Key-F2>' in parent_binds:
                message += '<F2> '
            else:
                self.main_window.bind('<F2>', self.switch_mode) 
            if message:
                print(f'Warning it appears that your root window uses binds {message}that could collide with the debugger.', f'To minimalize conflicts {message}will be disabled!')
            del message, parent_binds
        else:
            self.parent.bind('<Configure>', lambda _: self.load_properties())
            self.main_window.bind('<F5>', self.finish_inspection)
            self.main_window.bind('<F2>', self.switch_mode) 

    def toggle_inspect(self) -> None:
        if self.inspecting:
            self.stop_inspecting()
        else:
            self.start_inspecting()      

    def stop_inspecting(self) -> None:
        self.inspecting = False
        self.parent.unbind('<Motion>')
        self.parent.unbind('<Button-1>')
        self.inspect_button['text'] = 'INSPECT ELEMENT'

    def start_inspecting(self) -> None:
        self.inspecting = True
        self.parent.bind('<Motion>', self.while_inspection)
        self.parent.bind('<Button-1>', self.finish_inspection)
        self.inspect_button['text'] = 'INSPECTING ...'

    def while_inspection(self, _) -> None:
        position: tuple = self.parent.winfo_pointerxy()
        widget: ClassVar = self.parent.winfo_containing(position[0], position[1])
        if widget:
            pass
        if self.widget != widget:
            self.widget = widget
            self.unhighlight_elements()
            self.load_properties()
            if not self.widget in self.highlighted_elements:
                self.highlight_element(self.widget, '#3498db')
        del position, widget

    def load_properties(self) -> None:
        if self.widget:
            self.refresh_button.state(['!disabled'])
            self.widget_name['text'] = f'{self.widget.winfo_class()} ({self.widget.winfo_name()})'
            self.widget_dimensions['text'] = f'X: {self.widget.winfo_x()} Y: {self.widget.winfo_y()} WIDTH: {self.widget.winfo_width()} HEIGHT: {self.widget.winfo_height()}'
            self.widget_manager['text'] = self.widget.winfo_manager().upper()
            self.manager_config['text'] = ''
            widget_config: dict = {}
            if self.widget_manager['text'] == 'PACK':
                widget_config = self.widget.pack_info()
            elif self.widget_manager['text'] == 'PLACE':
                widget_config = self.widget.place_info()
            elif self.widget_manager['text'] == 'GRID':
                widget_config = self.widget.grid_info()
            if widget_config:
                for key in widget_config:
                    if key == 'in' or not widget_config[key] or widget_config[key] == 'none':
                        continue
                    self.manager_config['text'] += f'{key}: {widget_config[key]} '
                self.manager_config['text'] = self.manager_config['text'].upper()
            del widget_config
            self.widget_perent['text'] = self.widget.winfo_parent()
            self.widget_bindings['text'] = self.widget.bind()
            if self.widget.winfo_class() in ('Button', 'TButton', 'Label', 'TLabel', 'Radiobutton'):
                self.entry.state(['!disabled'])
                self.entry.delete(0, 'end')
                self.entry.insert(0, self.widget['text'])
                self.widget_image.state(['disabled'])
                if 'image' in self.widget.config() and self.widget['image']:
                    self.widget_image.state(['!disabled'])
                    self.img_label['image'] = self.widget['image']
                else:
                    self.img_label['image'] = self.blank_photo
                if 'command' in self.widget.config():
                    self.widget_function.state(['!disabled'])
            elif self.widget.winfo_class() in ('Entry', 'TEntry'):
                self.entry.state(['!disabled'])
                self.entry.delete(0, 'end')
                self.entry.insert(0, self.widget.get())
                self.widget_image.state(['disabled'])
                self.widget_function.state(['disabled'])
            else:
                self.entry.delete(0, 'end')
                self.entry.state(['disabled'])
                self.widget_image.state(['disabled'])
                self.widget_function.state(['disabled'])
                self.img_label['image'] = self.blank_photo
                self.widget_function.state(['disabled'])
            if self.widget != self.parent:
                self.inspect_perent.state(['!disabled'])
                if len(self.widget._nametowidget(self.widget.winfo_parent()).winfo_children()) > 1:
                    self.inspect_next_button.state(['!disabled'])
                else:
                    self.inspect_next_button.state(['disabled'])
            else:
                self.inspect_next_button.state(['disabled'])
                self.inspect_perent.state(['disabled'])
        else:
            self.refresh_button.state(['disabled'])

    def init_img_window(self) -> None:
        self.img_window: ClassVar = Toplevel()
        self.disallowed_windows.append(self.img_window.winfo_id())
        self.img_window.withdraw()
        self.img_window.title('')
        self.img_window.minsize(150, 150)
        self.img_window.attributes("-topmost", True)
        self.img_window.iconphoto(False, self.blank_photo)
        self.img_label: ClassVar = Label(self.img_window, background='#111')
        self.img_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.img_window.protocol('WM_DELETE_WINDOW', lambda: self.img_window.withdraw())
        self.img_window.mainloop()

    def open_image(self) -> None:
        if not self.img_window.winfo_ismapped():
            self.img_window.deiconify()

    def call_function(self) -> None:
        self.unhighlight_elements()
        self.widget.invoke()
        self.highlight_element(self.widget, '#f1c40f')

    def inspect_next(self) -> None:
        if self.widget:
            parent_childrens: list = self.widget._nametowidget(self.widget.winfo_parent()).winfo_children()
            for window in self.disallowed_windows:
                for child in parent_childrens:
                    if window == child.winfo_id():
                        parent_childrens.remove(child)
            widget_index: int = parent_childrens.index(self.widget)
            if len(parent_childrens) > widget_index + 1:
                self.inspect_widget(parent_childrens[widget_index + 1])
            else:
                self.inspect_widget(parent_childrens[0])
            del parent_childrens, widget_index

    def switch_mode(self, _) -> None:
        self.allow_self_debug = not self.allow_self_debug
        if self.allow_self_debug:
            self.mode_label['text'] = 'EXTENDED'
        else:
            self.mode_label['text'] = 'NORMAL'
        self.load_properties()
        self.load_widget_childrens()
        self.update_canvas()

    def inspect_widget(self, widget) -> None:
        self.widget = widget
        self.load_widget_childrens()
        self.update_canvas()
        self.unhighlight_elements()
        self.load_properties()
        if not self.widget in self.highlighted_elements:
            self.highlight_element(self.widget, '#3498db')

    def finish_inspection(self, _) -> None:
        self.stop_inspecting()
        self.load_properties()
        self.load_widget_childrens()
        self.update_canvas()

    def load_widget_childrens(self) -> None:
        for widget in self.get_all_widgets(self.canvas_cards):
            widget.destroy()
        for widget in self.widget.winfo_children():
            self.add_child(widget)

    def update_canvas(self) -> None:
        self.canvas.itemconfigure(self.canvas_window, width=self.canvas.winfo_width(), height=len(self.widget.winfo_children()) * 51)
        self.canvas.yview_moveto(0)

    def add_child(self, widget) -> None:
        if self.allow_self_debug or not widget.winfo_id() in self.disallowed_windows:
            child_frame: ClassVar = Frame(self.canvas_cards, background=self.main_window['background'])
            Label(child_frame, text=f'{widget.winfo_class()}', background='#333', foreground='#fff', font=('Consolas', 12), ).pack(side='left', anchor='center', fill='y')
            Label(child_frame, text=f'POS_X {widget.winfo_x()} POS_Y {widget.winfo_y()} WIDTH {widget.winfo_width()}PX HEIGHT {widget.winfo_height()}PX', background='#111', foreground='#fff', font=('Consolas', 12)).pack(side='left', anchor='center', padx=(10, 0))
            ttk.Button(child_frame, text='INSPECT', style='debugger.TButton', command=lambda: self.inspect_widget(widget)).pack(side='right', anchor='center', padx=10)
            child_frame.pack(side='top', fill='x', pady=(5, 0), ipady=5, padx=5)

    def entry_diff(self, _) -> None:
        if self.widget:
            if self.widget.winfo_class() in ('Button', 'TButton', 'Label', 'TLabel', 'Radiobutton'):
                if self.widget['text'] == self.entry.get():
                    self.apply_button.state(['disabled'])
                else:
                    self.apply_button.state(['!disabled'])
            elif self.widget.winfo_class() in ('Entry', 'TEntry'):
                if self.widget.get() == self.entry.get():
                    self.apply_button.state(['disabled'])
                else:
                    self.apply_button.state(['!disabled'])

    def apply_changes(self) -> None:
        if self.widget.winfo_class() in ('Button', 'TButton', 'Label', 'TLabel', 'Radiobutton'):
                self.widget['text'] = self.entry.get()
        elif self.widget.winfo_class() in ('Entry', 'TEntry'):
            self.widget.delete(0, 'end')
            self.widget.insert(0, self.entry.get())
        self.apply_button.state(['disabled'])

    def highlight_element(self, widget, color) -> None:
        if not widget in self.highlighted_elements:
            if 'background' in widget.config():
                self.highlighted_elements[widget] = widget['background']
                widget['background'] = color
                if widget.winfo_class() in ('Button', 'Radiobutton'):
                    widget['state'] = 'disabled'
            else:
                self.highlighted_elements[widget] = ''
                self.widget.state(['disabled'])

    def unhighlight_elements(self) -> None:
        widgets_to_remove: list = []
        for widget in self.highlighted_elements:
            if 'background' in widget.config():
                widget['background'] = self.highlighted_elements[widget]
                if widget.winfo_class() in ('Button', 'Radiobutton'):
                    widget['state'] = 'normal'
            else:
                widget.state(['!disabled'])
            widgets_to_remove.append(widget)
        for widget in widgets_to_remove:
            self.highlighted_elements.pop(widget)
        del widgets_to_remove

    def show_window(self) -> None:
        if self.parent:
            if not self.parent.winfo_ismapped():
                self.parent.deiconify()

    def get_all_widgets(self, widget) -> list:
        try:
            widget_list = widget.winfo_children()
            for widget in widget_list:
                if widget.winfo_children():
                    widget_list.extend(widget.winfo_children())
            return widget_list
        except Exception as _:
            print(format_exc())

    def on_mouse(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')

    def close_debugger(self) -> None:
        try:
            self.parent.unbind('<Motion>')
            self.parent.unbind('<Button-1>')
            self.parent.unbind('<Configure>')
            self.unhighlight_elements()
            self.img_window.destroy()
            self.main_window.destroy()
            del self
        except Exception as _:
            print(format_exc())




