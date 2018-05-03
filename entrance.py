from tkinter import *
from module_family import Family
fam = Family('localhost','family','root','13-qw24')



root = Tk()
root.title('Аутентификация')
root.minsize(220,160)
root.resizable(width=False, height=False)

login_text = Label(root, text='Login').place(x=5, y=2, width=60, height=40)
login_entry = Entry(root, width=15)
login_entry.place(x=90, y=10)

pass_text = Label(root, text='Password').place(x=5, y=30)
pass_entry = Entry(root, width=15, show='*')
pass_entry.place(x=90, y=30)

#=====================================ADMIN==========================================================
def admin():
    #Создаем класс окна
    root_admin = Tk()
    root_admin.title('Моя родословная')
    root_admin.minsize(680, 330)
    root_admin.resizable(width=False, height=False)

    #создаем текстовое окошко для вывода
    output = Text(root_admin, bg='white', font='Arial 12',wrap=WORD)
    output.place(x=10, y=115, width=645, height=200)

    scr = Scrollbar(root_admin, command=output.yview)  #создаем скролл бар
    output.configure(yscrollcommand = scr.set)
    scr.place(x=660, y=180)

    def show_people():
        humans = fam.print_people()  # обращаемся к классу Family в файле module_family
        for human in humans:
            output.insert('0.0', str(human) + '\n')  # 0.0 -верх влево вставляем нового человека
        output.insert('0.0', '*Название базы: family\n' + '\n')

    def cls_screen():
        output.delete(1.0, END)

    def add_people():
        modal = Tk()
        modal.title('Добавление новой записи')
        modal.minsize(300, 220)
        a = Entry(modal, width=25)  # для ввода инфы
        a.grid(row=1, column=2)
        l = Label(modal, text='name')  # заголовок который мы видим
        l.grid(row=1, column=1)
        a1 = Entry(modal, width=25)  # для ввода инфы
        a1.grid(row=2, column=2)
        l1 = Label(modal, text='surname')  # заголовок который мы видим
        l1.grid(row=2, column=1)
        a2 = Entry(modal, width=25)  # для ввода инфы
        a2.grid(row=3, column=2)
        l2 = Label(modal, text='date of birth')  # заголовок который мы видим
        l2.grid(row=3, column=1)
        a3 = Entry(modal, width=25)  # для ввода инфы
        a3.grid(row=4, column=2)
        l3 = Label(modal, text='date of death')  # заголовок который мы видим
        l3.grid(row=4, column=1)
        # создаем большое текстовое окно для коммента
        a4 = Text(modal, width=19, height=10, wrap=WORD)
        a4.grid(row=5, column=2)
        l4 = Label(modal, text='comment')  # заголовок который мы видим
        l4.grid(row=5, column=1)
        #   name, surname, dateofbirth, dateofdeath, comment
        # делаем кнопку сохранить запись
        def save_people():
            fam.add_people(a.get(), a1.get(), a2.get(), a3.get(),
                           a4.get(1.0, END)[:-1])  # a.get - ВЗЯТЬ ТЕКСТ ИЗ ТЕКСТОВОГО ПОЛЯ!
            output.insert('0.0', '*Новая запись добавлена\n')
            modal.destroy()

        button_save_people = Button(modal, text='Сохранить', width=15, height=1,
                                    command=save_people)  # command -это именно метод поэтому без скобок
        button_save_people.grid(row=7, column=2)
        modal.mainloop()

    def del_people():
        modal_del = Tk()
        modal_del.title('Удаление записи')
        modal_del.minsize(300, 100)
        a = Entry(modal_del, width=25)  # для ввода инфы
        a.grid(row=1, column=2)
        l = Label(modal_del, text='Введите № записи:')  # заголовок который мы видим
        l.grid(row=1, column=1)
        # делаем кнопку сохранить запись
        def deleting_people():
            fam.delete_people(a.get())  # delete_people - берем из модуля module_family.py
            output.insert('0.0', '*Запись удалена\n')
            modal_del.destroy()
        button_del_people = Button(modal_del, text='Удалить', width=15, height=1,
                                   command=deleting_people)  # command -это именно метод поэтому без скобок
        button_del_people.grid(row=3, column=2)
        modal_del.mainloop()

    def add_user():
        modal = Tk()
        modal.title('Добавление нового пользователя')
        modal.minsize(300, 220)
        a = Entry(modal, width=25)  # для ввода инфы
        a.grid(row=1, column=2)
        l = Label(modal, text='Login')  # заголовок который мы видим
        l.grid(row=1, column=1)
        a1 = Entry(modal, width=25)  # для ввода инфы
        a1.grid(row=2, column=2)
        l1 = Label(modal, text='Password')  # заголовок который мы видим
        l1.grid(row=2, column=1)

        # Root - выбор admin или user
        l2 = Label(modal, text='Root:')  # заголовок который мы видим
        l2.grid(row=3, column=1)
        r = ['Administrator', 'User']
        lis = Listbox(modal, selectmode=SINGLE, height=2, width=25)
        lis.grid(row=3, column=2)
        for i in r:
            lis.insert(END, i)
        lis.selection_set(0, 0)
        if lis.selection_get()=='Administrator':
            roots = 1
        else:
            roots = 0

        # проверка на корректность ввода логина и пароля цветом
        def correct_login(event):
            data = a.get()
            if len(data) > 10 or len(data) < 4:
                a['bg'] = 'red'
            else:
                a['bg'] = '#7CFC00'
        a.bind('<Any-KeyRelease>', correct_login)

        def correct_pass(event):
            data = a1.get()
            if len(data) < 3:
                a1['bg'] = 'red'
            else:
                a1['bg'] = '#7CFC00'
        a1.bind('<Any-KeyRelease>', correct_pass)


        # делаем кнопку сохранить запись
        def save_user():
            # проверка на корректность ввода логина и пароля

            if (a.get().isalpha() and (a1.get().isalpha() or a1.get().isdigit())):
                fam.add_user(a.get(), a1.get(), roots)  # a.get - ВЗЯТЬ ТЕКСТ ИЗ ТЕКСТОВОГО ПОЛЯ!
                output.insert('0.0', '*Новый пользователь добавлен\n')
                modal.destroy()
            else:
                modal_ok = Tk()
                modal_ok.title('Error')
                modal_ok.minsize(200, 90)
                l = Label(modal_ok, text='Введите корректные данные!')
                l.grid(row=1, column=1)
                def close_ok():
                    modal_ok.destroy()
                button_ok = Button(modal_ok, text='Ok', width=15, height=1,
                                            command=close_ok)  # command -это именно метод поэтому без скобок
                button_ok.grid(row=3, column=1)


        button_save_people = Button(modal, text='Сохранить', width=15, height=1,
                                    command=save_user)  # command -это именно метод поэтому без скобок
        button_save_people.grid(row=8, column=2)
        modal.mainloop()

    def del_user():
        modal_del = Tk()
        modal_del.title('Удаление записи')
        modal_del.minsize(300, 100)
        a = Entry(modal_del, width=25)  # для ввода инфы
        a.grid(row=1, column=2)
        l = Label(modal_del, text='Введите логин пользователя:')  # заголовок который мы видим
        l.grid(row=1, column=1)
        # делаем кнопку сохранить запись
        def deleting_user():
            fam.delete_user(a.get())  # delete_user - берем из модуля module_family.py
            output.insert('0.0', '*Запись удалена\n')
            modal_del.destroy()
        button_del_people = Button(modal_del, text='Удалить', width=15, height=1,
                                   command=deleting_user)  # command -это именно метод поэтому без скобок
        button_del_people.grid(row=3, column=2)
        modal_del.mainloop()




    #создаем кнопку 'Список людей'
    but_show_humans = Button(root_admin, text = 'Список людей', bg='white', fg='black', font='Arial',
                              width=22, height=1, command=show_people ) #fg - цвет шрифта
    but_show_humans.place(x = 10, y = 10)

    #создаем кнопку 'Очистить вывод'
    but_cls_humans = Button(root_admin, text = 'Очистить вывод', bg='white', fg='black',font='Arial',
                              width=22, height=1, command=cls_screen) #fg - цвет шрифта
    but_cls_humans.place(x = 10, y = 50)


    but_add_humans = Button(root_admin, text = 'Добавить новую запись', bg='white', fg='black',font='Arial',
                              width=22, height=1, command=add_people) #fg - цвет шрифта
    but_add_humans.place(x = 230, y = 10)


    but_del_humans = Button(root_admin, text = 'Удалить запись', bg='white', fg='black',font='Arial',
                              width=22, height=1, command=del_people) #fg - цвет шрифта
    but_del_humans.place(x = 230, y = 50)

    but_add_user = Button(root_admin, text = 'Добавить пользователя', bg='white', fg='black',font='Arial',
                              width=22, height=1, command=add_user) #fg - цвет шрифта
    but_add_user.place(x = 452, y = 10)

    but_del_user = Button(root_admin, text = 'Удалить пользователя', bg='white', fg='black',font='Arial',
                              width=22, height=1, command=del_user) #fg - цвет шрифта
    but_del_user.place(x = 452, y = 50)

    root_admin.mainloop()
#=====================================USER==========================================================

def user():
    #Создаем класс окна
    root_admin = Tk()
    root_admin.title('Моя родословная')
    root_admin.minsize(680, 330)
    root_admin.resizable(width=False, height=False)

    #создаем текстовое окошко для вывода
    output = Text(root_admin, bg='white', font='Arial 12',wrap=WORD)
    output.place(x=10, y=115, width=645, height=200)

    scr = Scrollbar(root_admin, command=output.yview)  #создаем скролл бар
    output.configure(yscrollcommand = scr.set)
    scr.place(x=660, y=180)

    def show_people():
        humans = fam.print_people()  # обращаемся к классу Family в файле module_family
        for human in humans:
            output.insert('0.0', str(human) + '\n')  # 0.0 -верх влево вставляем нового человека
        output.insert('0.0', '*Название базы: family\n' + '\n')

    def cls_screen():
        output.delete(1.0, END)

    #создаем кнопку 'Список людей'
    but_show_humans = Button(root_admin, text = 'Список людей', bg='white', fg='black', font='Arial',
                              width=22, height=1, command=show_people ) #fg - цвет шрифта
    but_show_humans.place(x = 10, y = 10)

    #создаем кнопку 'Очистить вывод'
    but_cls_humans = Button(root_admin, text = 'Очистить вывод', bg='white', fg='black',font='Arial',
                              width=22, height=1, command=cls_screen) #fg - цвет шрифта
    but_cls_humans.place(x = 10, y = 50)

    root_admin.mainloop()

#==================================================================================================


def playto():
    l = login_entry.get()
    p = pass_entry.get()

    if (l.isalpha() and (p.isalpha() or p.isdigit())) == True:
        text = fam.aft(login_entry.get(), pass_entry.get())
        if (str(text[0]) == "0"):
            # вызов метода для отображения интерфейса user
            root.destroy()
            user()
        else:
            if (str(text[0]) == "1"):
                # вызов метода для отображения интерфейса admin
                root.destroy()
                admin()
            else:
                # создание окна для отображения ошибки авторизации
                rooter = Tk()
                rooter.title("ERROR")
                root.minsize(50, 50)
                out = Text(rooter, bg="white", font="Arial 12", width=50, height=10)
                out.grid(row=1, column=1, padx=(1, 1))
                out.insert("0.0",
                           "ERROR!: Вы ввели не верный логин или пароль." + "\n" + " Либо Вы не зарегистрированны в приложении.")
                rooter.mainloop()

    else:
        rooter = Tk()
        rooter.title("ERROR")
        root.minsize(50, 50)
        out = Text(rooter, bg="white", font="Arial 12", width=50, height=10)
        out.grid(row=1, column=1, padx=(1, 1))
        out.insert("0.0", "ERROR!: Вы ввели не верные данные.")
        rooter.mainloop()

Button(root, text='Sign in', command=playto).place(x=60, y=70, width=90, height=40)
b= Button(root, text='Admin', command=admin).place(x=60, y=140, width=90, height=40)


def correct_login(event):
    data = login_entry.get()
    if len(data)>10 or len(data)<4:
        login_entry['bg']='red'
    else:
        login_entry['bg']='#7CFC00'
login_entry.bind('<Any-KeyRelease>', correct_login)


def correct_pass(event):
    data = pass_entry.get()
    if len(data)<3:
        pass_entry['bg']='red'
    else:
        pass_entry['bg']='#7CFC00'
pass_entry.bind('<Any-KeyRelease>', correct_pass)

root.mainloop()


