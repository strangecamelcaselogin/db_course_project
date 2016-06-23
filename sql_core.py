from hashlib import sha256
from datetime import datetime
import sqlite3 as lite

from flask import session

import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt

from settings import *


# ANY
def get_mark_list():
    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        rows = cur.execute("SELECT Car_Brands.Brand FROM Car_Brands").fetchall()

        return [(row[0], row[0]) for row in rows]


def get_marks_statistic():
    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        rows = cur.execute("SELECT Brand, COUNT(Brand) AS Count_brand FROM Cars GROUP BY Brand").fetchall()

        labels = []
        sizes = []
        for row in rows:
            labels.append(row[0])
            sizes.append(row[1])

        plt.figure(num=1, figsize=(6, 6))
        plt.axes(aspect=1)
        plt.pie(sizes, labels=labels)
        plt.savefig(PIE + '\\pie_brand.png', format='png')


def get_box_list():
    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        rows = cur.execute('''SELECT Box.ID_Box
                              FROM Box, Placed
                              WHERE (Box.ID_Box = Placed.ID_Box)
                              AND (Placed.Busy = "YES")''').fetchall()

        return [(row[0], row[0]) for row in rows]


def get_list_box_mark(brand):  #получаем все боксы и их стоимости для одной марки
    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        rows = cur.execute('''SELECT Box.ID_Box, Box.Price FROM Box
                           WHERE (Box.Brand = :brand)
                           AND Box.ID_Box NOT IN (SELECT ID_Box FROM Placed WHERE Busy = "YES")''',
                            {'brand': brand}).fetchall()

        if (len(rows) != 0):
            return(rows)


def get_tickets_list():
    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        cur.execute('''SELECT Placed.Ticket_Number, Cars.Car_Number, Box.Price, Box.ID_Box, Placed.Rent_Start,
                        Placed.Rent_End, Placed.Busy
                       FROM Box, Placed, Cars, Clients
                       WHERE (Placed.Car_Number = Cars.Car_Number) AND (Clients.ID_client = Cars.ID_client)
                       AND (Clients.Phone = :phone) AND (Box.ID_Box = Placed.ID_Box)''',
                    {'phone': session['phone']})

        rows = cur.fetchall()

    return reversed(rows)


def get_client_name():
    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        cur.execute('''SELECT Clients.First_Name, Clients.Second_Name
                       FROM  Clients
                       WHERE Clients.Phone = :phone''',
                    {'phone': session['phone']})

        full_name = cur.fetchone()

    return full_name


def get_client_cars():
    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        client_cars = cur.execute('''SELECT Car_Number
                                     FROM Cars
                                     WHERE ID_client = (SELECT ID_client
                                                        FROM Clients
                                                        WHERE Phone = :phone)''',
                                  {'phone': session['phone']}).fetchall()

    return [(row[0], row[0]) for row in client_cars]


# CLIENT
def rent_box(date_start, date_end, number):
    if date_end <= date_start:
        return 'Дата окончания аренды не может быть раньше начала.'

    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        mark = cur.execute("SELECT Brand FROM Cars WHERE Car_Number = :number",
                           {'number': number}).fetchone()[0]

        # Занимает ли эта машина бокс прямо сейчас
        cnt = cur.execute('''SELECT COUNT(*)
                             FROM Placed
                             WHERE Car_Number = :number AND Busy = "YES"''',
                          {'number': number}).fetchone()[0]

        if cnt == 0:
            id_box = cur.execute('''SELECT ID_Box, min(Price)
                                    FROM Box
                                    WHERE Brand = :mark
                                    AND ID_Box NOT IN (SELECT ID_Box
                                                       FROM Placed
                                                       WHERE Busy = "YES")''',
                                 {'mark': mark}).fetchone()[0]

            if id_box is not None:
                cur.execute('''INSERT INTO Placed (ID_Box, Car_Number, Rent_Start, Rent_End, Paid, Busy)
                               VALUES (:id_box, :n_auto, :start, :end, "NO", "YES")''',
                            {'id_box': id_box,
                             'n_auto': number,
                             'start': date_start,
                             'end': date_end})

                return True

            else:
                return 'К сожалению, у нас нет свободных боксов для вашей марки авто.'

        else:
            return 'Для вашей машины уже зарезервирован бокс'


def refuse_box(phone, ticket_id):
    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        id_client = cur.execute("SELECT ID_client FROM Clients WHERE Phone = :phone",
                                {'phone': phone}).fetchone()[0]

        cur.execute('''UPDATE Placed SET Busy = "NO"
                       WHERE :id_client = (SELECT ID_Client
                                           FROM Cars
                                           WHERE Car_Number = Placed.Car_Number)
                       AND Ticket_Number = :ticket_id''',
                    {'id_client': id_client,
                     'ticket_id': ticket_id})

    return True


def add_car(mark, number):
    #mark = form.mark_list.data
    #number = form.number_auto.data

    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        cnt = cur.execute("SELECT COUNT(*) FROM Cars WHERE Car_Number = :n_auto",
                          {'n_auto': number}).fetchone()[0]

        if cnt == 0:
            id_client = cur.execute("SELECT ID_Client FROM Clients WHERE Phone = :phone",
                                 {'phone': session['phone']}).fetchone()[0]

            # Записываем новую машину в базу
            cur.execute('''INSERT INTO Cars (Car_Number, ID_client, Brand)
                           VALUES (:number, :id_client, :mark)''',
                        {'number': number,
                         'id_client': id_client,
                         'mark': mark})

            return True

        else:
            return 'Такая машина уже зарегистрирована.'


def delete_car(number):
    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        cnt = cur.execute("SELECT COUNT(*) FROM Cars WHERE Car_Number = :n_auto",
                          {'n_auto': number}).fetchone()[0]

        if cnt == 1:
            id_client = cur.execute("SELECT ID_Client FROM Clients WHERE Phone = :phone",
                                {'phone': session['phone']}).fetchone()[0]

            cur.execute("DELETE FROM Cars WHERE Car_Number = :number AND ID_client = :id_client",
                        {'number': number,
                         'id_client': id_client})

            return True

    return False


# ADMIN MANAGE
def add_box(mark_name, cost):

    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        cur.execute('''INSERT INTO Box (Brand, Price)
                       VALUES (:mark, :cost)''',
                    {'mark': mark_name,
                     'cost': cost})

    return True


def close_box(id_box):
    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        cnt = cur.execute("SELECT COUNT(*) FROM Box WHERE ID_Box = :id",
                          {'id': id_box}).fetchone()[0]

        if cnt == 1:
            cur.execute("DELETE FROM Box WHERE ID_Box = :id",
                        {'id': id_box})

            return True

    return False


def update_box(n):
    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()
        cur.execute("UPDATE Box SET Price = Price * :n", {'n': n})

    return True


def add_mark(mark_name):
    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        cnt = cur.execute("SELECT COUNT(*) FROM Car_Brands WHERE Brand = :mark",
                          {'mark': mark_name}).fetchone()[0]

        if cnt == 0:
            cur.execute('''INSERT INTO Car_Brands (Brand) VALUES (:mark)''',
                        {'mark': mark_name})
            return True

    return False


def delete_mark(mark_name):
    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        cnt = cur.execute("SELECT COUNT(*) FROM Car_Brands WHERE Brand = :mark",
                          {'mark': mark_name}).fetchone()[0]

        if cnt == 1:
            cur.execute("DELETE FROM Car_Brands WHERE Brand = :mark",
                        {'mark': mark_name})
            return True

    return False


# ADMIN INFO
def get_list_c():
    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        info = cur.execute('''SELECT Clients.First_Name, Clients.Middle_Name,
                              Clients.Second_Name, Clients.Address
                              FROM Clients''').fetchall()

    return info


def get_list_cwm(mark_name):
    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        info = cur.execute('''SELECT DISTINCT Clients.ID_client, Second_Name, First_Name, Middle_Name, Address, Phone
                              FROM Clients, Cars
                              WHERE (Cars.Brand = :mark_name) AND (Clients.ID_client = Cars.ID_client)''',
                           {'mark_name': mark_name}).fetchall()

    return info


def get_list_cde(date):
    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        info = cur.execute('''SELECT ID_client, Second_Name, First_Name, Middle_Name, Address, Phone
                              FROM Clients
                              WHERE ID_client IN (SELECT ID_client
                                                  FROM Cars, Placed
                                                  WHERE Cars.Car_number = Placed.Car_Number
                                                  AND Busy = "YES"
                                                  AND Rent_End = :date)''',
                           {'date': date}).fetchall()

    return info


def get_client_by_box(box_number):

    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        info = cur.execute('''SELECT ID_client, Second_Name, First_Name, Middle_Name, Address, Phone
                              FROM Clients
                              WHERE ID_client IN (SELECT ID_client
                                                  FROM Cars, Placed
                                                  WHERE Cars.Car_Number = Placed.Car_Number
                                                  AND Busy = "YES"
                                                  AND ID_Box = :box_number)''',
                           {'box_number': box_number}).fetchall()

    return info


# LOGIN ADN REGISTER
def login(form):
    phone = form.phone.data
    hashed_password = sha256(form.password.data.encode('utf-8')).hexdigest()

    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()
        cnt = cur.execute('''SELECT COUNT(*)
                             FROM Clients
                             WHERE Phone = :phone AND Password = :password''',
                          {'phone': phone, 'password': hashed_password}).fetchone()[0]

        if cnt == 1:
            session['logged_in'] = True
            session['phone'] = phone
            if phone == ADMIN:
                session['is_admin'] = True

            return True

    return False


def register(form):
    phone = form.phone.data
    hashed_password = sha256(form.password.data.encode('utf-8')).hexdigest()

    f_name = form.name.data
    s_name = form.second_name.data
    m_name = form.mid_name.data
    address = form.address.data

    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        cnt = cur.execute("SELECT COUNT(*) FROM Clients WHERE Phone = :phone",
                          {'phone': phone}).fetchone()[0]

        if cnt == 0:
            cur.execute('''INSERT INTO Clients (Second_Name, First_Name, Middle_Name, Address, Phone, Password)
                           VALUES (:s_name, :f_name, :m_name, :address, :phone, :password)''',
                        {'s_name': s_name,
                         'f_name': f_name,
                         'm_name': m_name,
                         'address': address,
                         'phone': phone,
                         'password': hashed_password})

            return True

    return False

