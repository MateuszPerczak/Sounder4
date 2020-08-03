from tkinter import Toplevel, Label, Button, ttk, Frame, Canvas, Scrollbar, Tk
from typing import ClassVar

class Debugger:
    def __init__(self, parent) -> None:
        self.parent = parent
        del parent
        self.main_window: ClassVar = Toplevel()
        # hide window
        self.main_window.withdraw()
        # window style
        self.main_window.configure(background='#212121')
        self.main_theme: ClassVar = ttk.Style()
        self.main_theme.theme_use('clam')
        self.main_theme.configure('debugger.TButton', background='#111', relief='flat', font=('corbel', 12), foreground='#fff')
        self.main_theme.map('debugger.TButton', background=[('pressed', '!disabled', '#111'), ('active', '#151515')])
        self.main_theme.configure('debugger.Vertical.TScrollbar', gripcount=0, relief='flat', background='#212121', darkcolor='#212121', lightcolor='#212121', troughcolor='#212121', bordercolor='#212121', arrowcolor='#212121')
        self.main_theme.map('debugger.Vertical.TScrollbar', background=[('pressed', '!disabled', '#333'), ('disabled', '#212121'), ('active', '#111'), ('!active', '#111')])
        # window attributes
        self.main_window.attributes("-topmost", True)
        self.main_window.title(f'DEBUGGER - {self.parent.title()}')
        self.main_window.geometry('600x500')
        self.main_window.minsize(600, 500)
        self.main_window.protocol('WM_DELETE_WINDOW', self.close_debugger)
        # variables
        self.widget: ClassVar = None
        self.highlighted_widgets: list = []
        # content
        Label(self.main_window, text=' WIDGET INSPECTOR', background='#111', foreground='#fff', font=('Consolas', 14), anchor='w').pack(side='top', fill='x', ipadx=5, ipady=5)
        # buttons frame
        buttons_frame: ClassVar = Frame(self.main_window, background='#212121')
        # inspect button
        self.inspect_button: ClassVar = ttk.Button(buttons_frame, text='INSPECT ELEMENT', takefocus=False, style='debugger.TButton', command=self.inspect_element)
        self.inspect_button.pack(side='left', pady=(10, 0))
        # delete button
        self.delete_button: ClassVar = ttk.Button(buttons_frame, text='DELETE ELEMENT', takefocus=False, style='debugger.TButton', command=self.delete_element)
        # disable button
        self.delete_button.state(['disabled'])
        self.delete_button.pack(side='left', padx=10, pady=(10, 0))
        # parent button
        self.highlight_parent: ClassVar = ttk.Button(buttons_frame, text='HIGHLIGHT PARENT', takefocus=False, style='debugger.TButton', command=lambda: self.highlight_element(self.widget._nametowidget(self.widget.winfo_parent()), '#c62828'))
        self.highlight_parent.state(['disabled'])
        self.highlight_parent.pack(side='left', padx=10, pady=(10, 0))
        buttons_frame.pack(side='top', fill='x', padx=10)
        # widget frame
        self.widget_frame: ClassVar = Frame(self.main_window, background='#111')
        self.widget_frame.pack(side='top', anchor='w', fill='both', padx=10, pady=(10, 0))
        # widget label
        self.widget_info: ClassVar = Label(self.widget_frame, background='#111', foreground='#fff', font=('Consolas', 13), justify='left')
        self.widget_info.pack(side='top', anchor='w', padx=5, pady=5)
        # children label
        Label(self.main_window, text=' WIDGET CHILDRENS', background='#111', foreground='#fff', font=('Consolas', 14), anchor='w').pack(side='top', fill='x', ipadx=5, ipady=5, pady=10)
        # children buttons frame
        children_buttons_frame: ClassVar = Frame(self.main_window, background='#212121')
        # highlight button
        self.highlight_button: ClassVar = ttk.Button(children_buttons_frame, text='HIGHLIGHT ALL', takefocus=False, style='debugger.TButton', command=self.highlight_childrens)
        # disable button
        self.highlight_button.state(['disabled'])
        self.highlight_button.pack(side='left')
        # unhighlight button
        self.unhighlight_button: ClassVar = ttk.Button(children_buttons_frame, text='UNHIGHLIGHT ELEMENTS', takefocus=False, style='debugger.TButton', command=self.unhighlight_childrens)
        self.unhighlight_button.state(['disabled'])
        self.unhighlight_button.pack(side='left', padx=10)
        children_buttons_frame.pack(side='top', fill='x', padx=10)
        # children frame
        children_frame: ClassVar = Frame(self.main_window, background='#212121')
        # scrollbar
        children_scrollbar: ClassVar = ttk.Scrollbar(children_frame, style='debugger.Vertical.TScrollbar')
        # canvas
        self.children_canvas: ClassVar = Canvas(children_frame, borderwidth=0, highlightthickness=0, background='#212121', yscrollcommand=children_scrollbar.set)
        # bind scrollbar to canvas
        children_scrollbar.configure(command=self.children_canvas.yview)
        # add frame for content
        self.children_cards: ClassVar = Frame(self.children_canvas, background='#212121')
        # update canvas
        self.children_cards.bind('<Configure>', lambda _: self.children_canvas.configure(scrollregion=self.children_canvas.bbox('all')))
        self.children_window: ClassVar = self.children_canvas.create_window((0, 0), window=self.children_cards, anchor='nw')
        self.children_canvas.bind('<Configure>', lambda _: self.children_canvas.itemconfigure(self.children_window, width=self.children_canvas.winfo_width(), height=len(self.children_cards.winfo_children()) * 55))
        # pack
        children_scrollbar.pack(side='right', fill='y', pady=10)
        self.children_canvas.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        children_frame.pack(side='top', fill='both', expand=True, padx=10, pady=(0, 10))
        # show window
        self.main_window.deiconify()
        self.main_window.bind('<MouseWheel>', self.on_mouse)
        Debug(self.main_window)
        self.main_window.mainloop()

    def inspect_element(self) -> None:
        self.parent.bind('<Motion>', self.while_inspection)
        self.parent.bind('<Button-1>', self.end_inspection)
        self.inspect_button['text'] = 'INSPECTING ...'
        for widget in self.get_all_widgets(self.children_cards):
            widget.destroy()
        self.unhighlight_elements()
        
    def end_inspection(self, _) -> None:
        self.parent.unbind('<Motion>')
        self.parent.unbind('<Button-1>')
        self.inspect_button['text'] = 'INSPECT ELEMENT'
        self.after_inspection()
        
    def while_inspection(self, _) -> None:
        position: tuple = self.parent.winfo_pointerxy()
        widget: ClassVar = self.parent.winfo_containing(position[0], position[1])
        if widget:
            self.highlight_parent.state(['!disabled'])
        else:
            self.highlight_parent.state(['disabled'])
        if widget and widget.winfo_manager() in ('pack', 'place', 'grid'):
            self.delete_button.state(['!disabled'])
        else:
            self.delete_button.state(['disabled'])
        if widget != self.widget:
            self.unhighlight_elements()
            self.widget = widget
            self.highlight_element(widget, '#1565c0')
            self.widget_info['text'] = f'WIDGET: {self.widget.winfo_name()}\nCLASS: {self.widget.winfo_class()}\nMANAGER: {self.widget.winfo_manager()}\nPOSITION: {self.widget.winfo_x()}X {self.widget.winfo_y()}Y\nDIMENSIONS: {self.widget.winfo_width()}W {self.widget.winfo_height()}H\nPARENT: {self.widget._nametowidget(self.widget.winfo_parent()).winfo_name()}'
        del position, widget

    def after_inspection(self) -> None:
        for widget in self.get_all_widgets(self.children_cards):
            widget.destroy()
        for widget in self.widget.winfo_children():
            self.children_card(widget)
        if len(self.get_all_widgets(self.children_cards)) > 1:
            self.highlight_button.state(['!disabled'])
        else:
            self.highlight_button.state(['disabled'])
        # resize children card
        self.children_canvas.itemconfigure(self.children_window, width=self.children_canvas.winfo_width(), height=len(self.widget.winfo_children()) * 55)

    def children_card(self, widget: ClassVar) -> None:
        card_frame: ClassVar = Frame(self.children_cards, background='#111')
        Label(card_frame, text=f'{widget.winfo_class()} ({widget.winfo_name()})', background='#333', foreground='#fff', font=('Consolas', 12), ).pack(side='left', anchor='center', fill='y')
        Label(card_frame, text=f'DIMENTIONS: {widget.winfo_width()}W {widget.winfo_height()}H', background='#111', foreground='#fff', font=('Consolas', 12)).pack(side='left', anchor='center', padx=(10, 0))
        Label(card_frame, text=f'POSITION: {widget.winfo_x()}X {widget.winfo_y()}Y', background='#111', foreground='#fff', font=('Consolas', 12)).pack(side='left', anchor='center', padx=(10, 0))
        if 'background' in widget.config():
            ttk.Button(card_frame, text='HIGHLIGHT ELEMENT', takefocus=False, style='debugger.TButton', command=lambda: self.highlight_element(widget, '#2e7d32')).pack(side='right', anchor='center', padx=10)
        card_frame.pack(side='top', fill='x', pady=(0, 10), ipady=5)

    def highlight_childrens(self) -> None:
        for widget in self.widget.winfo_children():
            self.highlight_element(widget, '#2e7d32')

    def unhighlight_childrens(self) -> None:
        self.unhighlight_elements()
        self.highlight_element(self.widget, '#1565c0')

    def edit_widget_attributes(self, _) -> None:
        if self.widget.winfo_class() == 'Label':
            pass

    def delete_element(self) -> None:
        manager: str = self.widget.winfo_manager()
        if manager == 'pack':
            self.widget.pack_forget()
        elif manager == 'place':
            self.widget.place_forget()
        elif manager == 'grid':
            self.widget.grid_forget()
        self.delete_button.state(['disabled'])
        del manager

    def highlight_element(self, widget_to_highlight, color) -> None:
        already_highlighted: bool = False
        for widget in self.highlighted_widgets:
            if widget[0] == widget_to_highlight:
                already_highlighted = True
        if 'background' in widget_to_highlight.config():
            if not already_highlighted:
                self.highlighted_widgets.append((widget_to_highlight, widget_to_highlight['background']))
                widget_to_highlight['background'] = color
                self.unhighlight_button.state(['!disabled'])
                if widget_to_highlight == self.widget._nametowidget(self.widget.winfo_parent()):
                    self.highlight_parent.state(['disabled'])
        del already_highlighted, widget_to_highlight, color

    def unhighlight_elements(self) -> None:
        for _ in range(len(self.highlighted_widgets)):
            for widget in self.highlighted_widgets:
                widget[0]['background'] = widget[1]
                self.highlighted_widgets.remove(widget)
        self.unhighlight_button.state(['disabled'])
        self.highlight_parent.state(['!disabled'])

    def get_all_widgets(self, widget) -> list:
        widget_list = widget.winfo_children()
        for widget in widget_list:
            if widget.winfo_children():
                widget_list.extend(widget.winfo_children())
        return widget_list

    def on_mouse(self, event):
        self.children_canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')

    def close_debugger(self) -> None:
        self.parent.unbind('<Motion>')
        self.parent.unbind('<Button-1>')
        self.unhighlight_elements()
        self.main_window.destroy()
        del self
