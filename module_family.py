import mysql.connector
from mysql.connector import Error



class Family:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        try:
            conn = self.get_conn()
            if conn.is_connected():
                print('Подключение прошло успешно')
                conn.close()
        except Error as e:
            print(e)


    def get_conn(self):
        conn = mysql.connector.connect(host = self.host,
                                           database = self.database,
                                           user = self.user,
                                           password = self.password)
        return conn


    def print_people(self):
        try:
            sql = 'SELECT * from people'
            conn = self.get_conn()
            c = conn.cursor()       #получаем в курсор
            c.execute(sql)           # извлекаем из курсора
            print('Список всех людей в базе:')
            rows = c.fetchall()     #метод достать все
            for row in rows:
                print(row)
            conn.close()
            return rows
        except Error as e:
            print(e)


    def add_people(self, name, surname, date_of_birth, date_of_death, comment):
        try:

            sql = 'INSERT INTO people (name, surname, dateofbirth, dateofdeath, comment) VALUES (%s, %s, %s, %s, %s)'
            args = (name, surname, date_of_birth, date_of_death, comment)
            conn = self.get_conn()
            c = conn.cursor()  # получаем в курсор
            c.execute(sql, args)
            # c.execute(sql)
            conn.commit()   # заносится в базу только когда коммит
            conn.close()
        except Error as e:
            print(e)

    def add_user(self, login, password, root):
        try:
            # функция кодировки пароля методом Цезаря
            def cezar_encode(key, message):
                new_message = []
                for letter in message:
                    simbol_code = ord(letter)
                    new_code = simbol_code + key
                    new_simbol = chr(new_code)
                    new_message.append(new_simbol)
                return ''.join(new_message)
            password_encode = cezar_encode(9, password)

            sql = 'INSERT INTO logins (login, password, root) VALUES (%s, %s, %s)'
            args = (login, password_encode, root)
            conn = self.get_conn()
            c = conn.cursor()  # получаем в курсор
            c.execute(sql, args)
            # c.execute(sql)
            conn.commit()   # заносится в базу только когда коммит
            conn.close()
        except Error as e:
            print(e)


    def update_name(self, id, name):
        try:
            #sql = 'INSERT INTO category (id, name, discount, alias_name) VALUES (%s, %s, %s, %s)' если делать через format - то СТРОКИ всегда в кавычках {}

            sql = 'UPDATE people SET name = %s WHERE id = %s'
            args = (name, id)
            conn = self.get_conn()
            c = conn.cursor()  # получаем в курсор
            c.execute(sql, args)
            # c.execute(sql)
            conn.commit()   # заносится в базу только когда коммит
            conn.close()
        except Error as e:
            print(e)



    def delete_people(self, id):
        try:
            sql = 'DELETE from people WHERE id = %s'
            conn = self.get_conn()
            c = conn.cursor()  # получаем в курсор
            c.execute(sql, (id,))  # СТАВИМ ЗАПЯТУЮ КОГДА ОДИН ПАРАМЕТР
            conn.commit()   # заносится в базу только когда коммит
            conn.close()
        except Error as e:
            print(e)

    def delete_user(self, login):
        try:
            sql = 'DELETE from logins WHERE login = %s'
            conn = self.get_conn()
            c = conn.cursor()  # получаем в курсор
            c.execute(sql, (login,))  # СТАВИМ ЗАПЯТУЮ КОГДА ОДИН ПАРАМЕТР
            conn.commit()  # заносится в базу только когда коммит
            conn.close()
        except Error as e:
            print(e)

# функция авторизации - для входа в админку
    def aft(self, log, pas):

        #Функция декодирования пароля
        def cezar_encode(key, message):
            new_message = []
            for letter in message:
                simbol_code = ord(letter)
                new_code = simbol_code + key
                new_simbol = chr(new_code)
                new_message.append(new_simbol)
            return ''.join(new_message)

        password_decode = cezar_encode(9,pas)
        print('new:'+ pas +' old'+ password_decode)

        try:
            sql = "SELECT root FROM family.logins WHERE login = %s and password = %s"
            conn = mysql.connector.connect(host=self.host,
                                       database=self.database,
                                       user=self.user,
                                       password=self.password)
            c = conn.cursor()
            c.execute(sql,(log,password_decode))
            rows = c.fetchall()
            if (rows == []):
                rows = ['e','r','r','o','r']
            return rows[0]
        except Error as e:
            return e

if __name__ == "__main__":

    fam = Family('localhost','family','root','13-qw24')
    fam.print_people()

#    fam.update_name('1','Паша')
    fam.delete_people('6')
    fam.delete_people('7')
    fam.add_people('Андрей', 'Матье', '1988', '1765', 'просто хороший человек')

    print('После:')
    fam.print_people()
