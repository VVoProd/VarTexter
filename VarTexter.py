from tkinter import *
from tkinter.filedialog import askopenfile, asksaveasfile
from tkinter.scrolledtext import ScrolledText
from tkinter import Scrollbar, font, Button, Menu, Frame, messagebox
from tkinter.ttk import Combobox, Progressbar, Frame, Notebook
from subprocess import *
from pygments.lexers import PythonLexer
from pygments.token import Token
from time import *
import webbrowser, win32api, urllib.parse, keyboard, re, pyperclip, os, datetime
syntax = "plain_text"
shrift_font = "Times New Roman"
shrift_num = 15
filepath = "Не сохранено"
lexer = PythonLexer()
name = "Unlighted"
shrifts = list()
for i in range(1, 101):
    shrifts.append(i)
style = shrift_font
height_t = shrift_num
username = os.getlogin()
tabs = 2
info_txt = """
Инструкция пользования VarTexter
Горячие клавиши
-Работа с файлами
--Новый файл Ctrl+N
--Открыть файл Ctrl+O
--Сохранить файл Ctrl+S
--Сохранить файл как Ctrl+Shift+S
-Работа с текстом
--Копировать Ctrl+C
--Вставить Ctrl+V
--Вырезать Ctrl+X
--Выделить всё Ctrl+A
--Поиск в браузере Ctrl+B
-Работа с окном
--Открыть новое окно Ctrl+Shift+N
--Закрыть окно Кнопка закрытия окна
-Настройки
--Шрифт Ctrl+R
--Темы Ctrl+T
"""
window = Tk()
window.title(f"VarTexter - {filepath}")
backup = open(r"""C:\Users\%s\Documents\backup.up""" % username, "a+")
window.rowconfigure(0, minsize=600, weight=1)
window.columnconfigure(1, minsize=800, weight=1)
window.geometry("700x500+0+0")
txt_edit = ScrolledText(window, undo=True, maxundo=-1, autoseparators=True, font=((shrift_font), shrift_num),selectbackground="light gray", selectforeground="blue")
txt_edit.pack(expand = True, fill= "both")
def save_file(event=False):
    global filepath
    contents = txt_edit.get(1.0, END)
    filepath = asksaveasfile(title="VarTexter - Сохранить файл", defaultextension=".txt", filetypes=([("Текстовый файл", "*.txt"),("Python Files", "*.py"), ("Все файлы", "*.*")]))
    if filepath:
        filepath.write(contents)
    window.title(f"VarTexter - {filepath.name}")
    try:
        backup = open(r"""C:\Users\%s\Documents\backup.up""" % username, "a+")
        backup.write(f"\nSaved file at filepath: {filepath.name}; Time: {datetime.datetime.now()}")
    except AttributeError:
        pass
def open_file(event=False):
    global filepath
    if filepath != "Не сохранено":
        save_with_ext()
        filepath = askopenfile(title="VarTexter - Открыть файл", mode ="r", filetypes =[("Текстовые файлы", "*.txt"),("Python Files", "*.py"), ("Все файлы", "*.*")])
        if filepath is not None:
            try:
                content = filepath.read()
                txt_edit.delete(1.0, END)
                txt_edit.insert(END, content)
                window.title(f"VarTexter - {filepath.name}")
                backup = open(r"""C:\Users\%s\Documents\backup.up""" % username, "a+")
                backup.write(f"\nOpened file at filepath: {filepath.name}; Time: {datetime.datetime.now()}")
            except UnicodeDecodeError:
                messagebox.showerror(title="VarTexter", message="Этот тип файла не распознаётся программой")
    else:
        filepath = askopenfile(title="VarTexter - Открыть файл", mode ="r", filetypes =[("Текстовые файлы", "*.txt"),("Python Files", "*.py"), ("Все файлы", "*.*")])
        if filepath is not None:
            try:
                content = filepath.read()
                txt_edit.delete(1.0, END)
                txt_edit.insert(END, content)
                window.title(f"VarTexter - {filepath.name}")
                backup = open(r"""C:\Users\%s\Documents\backup.up""" % username, "a+")
                backup.write(f"\nOpened file at filepath: {filepath.name}; Time: {datetime.datetime.now()}")
            except UnicodeDecodeError:
                messagebox.showerror(title="VarTexter", message="Этот тип файла не распознаётся программой")
def save_with_ext(event=False):
    if filepath != "Не сохранено":
        if filepath is not None:
            saving = open(f"{filepath.name}", "r+")
            saving.truncate(0)
            text_to_saving = txt_edit.get(1.0, END)
            saving.write(text_to_saving)
            saving.close()
            try:
                backup = open(r"""C:\Users\%s\Documents\backup.up""" % username, "a+")
                backup.write(f"\nСохранены изменения в файле: {filepath.name}; Time: {datetime.datetime.now()}")
            except AttributeError:
                pass
        else:
            save_file()
    if filepath == "Не сохранено":
        save_file()
def new_file(event=False):
    try:
        if filepath == "Не сохранено":
            res = messagebox.askyesnocancel("VarTexter", "Сохранить текст перед закрытием?")
            if res is True:
                save_with_ext()
                keyboard.send("Ctrl+a")
                keyboard.send("Backspace")
            elif res is False:
                keyboard.send("Ctrl+a")
                keyboard.send("Backspace")
            elif res is Cancel:
                res.destroy()
        else:
            window.destroy()
    except NameError:
        pass
def printing(event=False):
    try:
        win32api.ShellExecute(0, "print", filepath.name, None, ".", 0)
    except AttributeError:
        messagebox.showerror(title="VarTexter - Print", message="Неправильный путь")
    except Exception:
        messagebox.showwarning(title="VarTexter - Print", message="Принтер не найден")
def open_new_w():
    Popen(r"""C:\Program Files\VarTexter\VarTexter.exe""")
def closew():
    try:
        if filepath == "Не сохранено":
            res = messagebox.askyesnocancel("VarTexter", "Сохранить текст перед закрытием?")
            if res is True:
                save_file()
                window.destroy()
            elif res is False:
                window.destroy()
            elif res is Cancel:
                res.destroy()
        else:
            save_with_ext()
            window.destroy()
    except NameError:
        pass
def get_shrift(event=False):
    global test_text
    window_s = Tk()
    window_s.title(f"VarTexter - Шрифт")
    window_s.geometry("300x150+10+50")
    window_s.resizable(0,0)
    window_s["bg"]="white"
    combo_s = Combobox(window_s)
    combo_s["values"] = (shrifts)
    combo_s.pack()
    fonts=list(font.families())
    fonts.sort()
    combo_t = Combobox(window_s)  
    combo_t["values"] = (fonts)
    combo_t.pack()
    test_text = Label(window_s, text="123QuickBrownлИса¡Jumpç\nOverЛениВАяDoG", font=(f"{shrift_font}", shrift_num), background="white", activebackground="white")
    test_text.pack()
    def to_text():
        combo_t_g = "Times New Roman"
        combo_s_g = 10
        combo_t_g = combo_t.get()
        combo_s_g = combo_s.get()
        style = combo_t_g
        height_t = combo_s_g
        global txt_edit, window_s
        txt_edit.configure(font=(f"{combo_t_g}", combo_s_g))
    def test():
        combo_t_g = combo_t.get()
        combo_s_g = combo_s.get()
        test_text.configure(font=(f"{combo_t_g}", combo_s_g))
        test_text.pack()
    test_but = Button(window_s, text="Попробовать на тексте", command=test, background="white", activebackground="white",relief="flat")
    test_but.pack()
    ok_but = Button(window_s, text="Применить к тексту", command=to_text, background="white", activebackground="white",relief="flat")
    ok_but.pack()
    window_s.bind("<F4>", fatal_closing)
    window_s.iconbitmap(r"""C:\Program Files\VarTexter\vartexter.ico""")
    window_s.mainloop()
def fatal_closing(event):
    window.destroy()
    window_s.destroy()
    backup.close()
def undo(event=False):
    txt_edit.edit_undo()
def redo(event=False):
    txt_edit.edit_redo()
def copy_v(event=False):
    copy_v = pyperclip.copy(txt_edit.selection_get())
def paste(event=False):
    paste_v = txt_edit.insert(END, pyperclip.paste())
def delete_txt(event=False):
    delete_v = txt_edit.delete("sel.first", "sel.last")
def search_in_br(event=False):
    try:
        search = txt_edit.selection_get()
        webbrowser.open(search)
    except Exception:
        search = txt_edit.get(1.0, END)
        webbrowser.open(search)
def get_txt_edit_coord(s: str, i: int):
    for row_number, line in enumerate(s.splitlines(keepends=True), 1):
        if i < len(line):
            return f"{row_number}.{i}"
        i -= len(line)
def on_edit(event):
    backup = open(r"""C:\Users\%s\Documents\backup.up""" % username, "a+")
    for tag in txt_edit.tag_names():
        txt_edit.tag_remove(tag, 1.0, END)
    s = txt_edit.get(1.0, END)
    tokens = lexer.get_tokens_unprocessed(s)
    for i, token_type, token in tokens:
        backup.write(token)
        j = i + len(token)
    txt_edit.edit_modified(0)
txt_edit.bind("<<Modified>>", on_edit)
def all_info(event=False):
    info = Tk()
    info.geometry("300x400+10+50")
    info.title("VarTexter - Информация")
    info["bg"]="white"
    info.resizable(0,0)
    info_lbl = Label(info, text=f"{info_txt}", background="white")
    info_lbl.pack()
    info.iconbitmap(r"""C:\Program Files\VarTexter\vartexter.ico""")
    info.mainloop()
def theme_black(event=False):
    txt_edit.configure(background="black", foreground="white", cursor="xterm white")
def theme_white(event=False):
    txt_edit.configure(background="white", foreground="black", cursor="xterm black")
def themes(event=False):
    background_change = Tk()
    background_change.iconbitmap(r"""C:\Program Files\VarTexter\vartexter.ico""")
    background_change.title("VarTexter - Темы")
    background_change.resizable(0,0)
    background_change.geometry("300x250+30+30")
    background_change["bg"]="white"
    change_theme_l = Label(background_change, text="Темы для редактора:", background="white", activebackground="white")
    black_theme_b = Button(background_change, text="Темная тема", command=theme_black, relief="flat", background="white", activebackground="white")
    white_theme_b = Button(background_change, text="Светлая тема(стандарт)", command=theme_white, relief="flat", background="white", activebackground="white")
    hex_theme1 = Entry(background_change)
    hex_theme2 = Entry(background_change)
    hex_theme3 = Entry(background_change)
    def hex_change():
        r_color = hex_theme1.get()
        g_color = hex_theme2.get()
        b_color = hex_theme3.get()
        hex_theme = str(r_color+g_color+b_color)
        try:
            txt_edit.configure(background=f"#{hex_theme}")
        except Exception:
            messagebox.showwarning(title="VarTexter", message="Неправильный цвет!")
    hex_theme_set = Button(background_change, text="Применить RGB или HEX к фону", command=hex_change, relief="flat", background="white", activebackground="white")
    hex_font1 = Entry(background_change)
    hex_font2 = Entry(background_change)
    hex_font3 = Entry(background_change)
    def hex_font_change():
        r_color_f = hex_font1.get()
        g_color_f = hex_font2.get()
        b_color_f = hex_font3.get()
        hex_font = str(r_color_f+g_color_f+b_color_f)
        try:
            txt_edit.configure(foreground=f"#{hex_font}")
        except Exception:
            messagebox.showwarning(title="VarTexter", message="Неправильный цвет!")
    hex_font_set = Button(background_change, text="Применить RGB или HEX к тексту", command=hex_font_change, relief="flat", background="white", activebackground="white")
    change_theme_l.pack()
    black_theme_b.pack()
    white_theme_b.pack()
    hex_theme1.pack()
    hex_theme2.pack()
    hex_theme3.pack()
    hex_theme_set.pack()
    hex_font1.pack()
    hex_font2.pack()
    hex_font3.pack()
    hex_font_set.pack()
    background_change.iconbitmap(r"""C:\Program Files\VarTexter\vartexter.ico""")
    background_change.mainloop()
class RKB(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.menu = Menu(self.parent, tearoff=0)
        self.menu.add_command(label="Поиск в браузере", command=search_in_br)
        self.menu.add_separator()
        self.menu.add_command(label="Копировать", command=copy_v)
        self.menu.add_command(label="Вставить", command=paste)
        self.menu.add_command(label="Вырезать", command=delete_txt)
        self.menu.add_separator()
        self.menu.add_command(label="Выделить всё", command=lambda: keyboard.send("Ctrl+a"))
        self.parent.bind("<Button-3>", lambda event: self.menu.post(event.x_root, event.y_root))
        self.pack()
main_menu = Menu(tearoff = False)
file_menu = Menu(tearoff = False)
text_menu = Menu(tearoff = False)
sett_menu = Menu(tearoff = False)
help_menu = Menu(tearoff = False)
main_menu.add_cascade(label="Файл", menu=file_menu)
main_menu.add_cascade(label="Правка", menu=text_menu)
main_menu.add_cascade(label="Настройки", menu=sett_menu)
main_menu.add_cascade(label="Помощь", menu=help_menu)
file_menu.add_command(label="Новый файл (Ctrl+N)", command=new_file)
file_menu.add_command(label="Открыть файл (Ctrl+O)", command=open_file)
file_menu.add_command(label="Сохранить (Ctrl+S)", command=save_with_ext)
file_menu.add_command(label="Сохранить файл как (Ctrl+Shift+S)", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Печать (Ctrl+P)", command=printing)
file_menu.add_separator()
file_menu.add_command(label="Выход (Ctrl+Q)", command=closew)
file_menu.add_command(label="Новое окно (Ctrl+Shift+N)", command=open_new_w)
text_menu.add_command(label="Назад (Ctrl+Z)", command=undo)
text_menu.add_command(label="Вперед (Ctrl+Shift+Z)", command=redo)
text_menu.add_separator()
text_menu.add_command(label="Копировать (Ctrl+C)", command=redo)
text_menu.add_command(label="Вставить (Ctrl+V)", command=redo)
text_menu.add_command(label="Вырезать (Ctrl+X)", command=delete_txt)
text_menu.add_separator()
text_menu.add_command(label="Поиск в браузере (Ctrl+B)", command=delete_txt)
sett_menu.add_command(label="Шрифт (Ctrl+R)", command=get_shrift)
sett_menu.add_separator()
sett_menu.add_command(label="Темы", command=themes)
help_menu.add_command(label="Справка (Ctrl+I)", command=all_info)
app = RKB(window)
window.bind("<Control-Shift-S>", save_file)
window.bind("<Control-s>", save_with_ext)
window.bind("<Control-o>", open_file)
window.bind("<Control-r>", get_shrift)
window.bind("<Control-Shift-N>", open_new_w)
window.bind("<Control-Shift-Z>", redo)
window.bind("<Control-x>", delete_txt)
window.bind("<Control-n>", new_file)
window.bind("<Control-b>", on_edit)
window.bind("<Control-t>", themes)
window.bind("<Control-i>", all_info)
window.bind("<Control-p>", printing)
window.bind("<Control-b>", search_in_br)
window.config(menu=main_menu)
window.protocol("WM_DELETE_WINDOW", closew)
try:
    window.iconbitmap(r"""C:\Program Files\VarTexter\vartexter.ico""")
except:
    pass
window.mainloop()
