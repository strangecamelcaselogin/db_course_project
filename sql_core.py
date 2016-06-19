from hashlib import sha256
from datetime import datetime
import sqlite3 as lite

from flask import session

from settings import *


def form_mark_list():
    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        rows = cur.execute("SELECT Car_Brands.Brand FROM Car_Brands").fetchall()

        return {row[0]: row[0] for row in rows}


def form_ticket_list():
    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        cur.execute('''SELECT Placed.Ticket_Number FROM Placed, Cars, Clients
                       WHERE (Placed.Car_Number = Cars.Car_Number) AND (Clients.ID_client = Cars.ID_client)
                       AND (Clients.Phone = :phone)''',
                        {'phone': session['phone']})

        rows = cur.fetchall()

    return {row[0]: row[0] for row in rows}


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


# ADMIN MANAGE

def add_box(form):
    mark_name = form.nb_mark_name.data
    cost = form.cost.data
    #status = '0'

    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        cur.execute('''INSERT INTO Box (Brand, Price, Status)
                       VALUES (:mark, :cost, :status)''',
                    {'mark': mark_name,
                     'cost': cost,
                     'status': OPENED})

    return True


def close_box(form):
    id_box = form.cb_box_code.data
    #status = '2'

    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        cnt = cur.execute("SELECT COUNT(*) FROM Box WHERE ID_Box = :id",
                          {'id': id_box}).fetchone()[0]

        if cnt == 1:
            cur.execute('''UPDATE Box SET Status = :status  WHERE ID_Box = :id''',
                        {'id': id_box,
                         'status': CLOSED})
            return True

    return False


def update_box(form):
    n = float(form.u_cost.data.replace(',', '.'))

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


# RENT
def rent_(form):
    mark = form.mark_list.data
    date_end = datetime.strptime(form.date_end.data, '%d.%m.%Y')
    date_start = datetime.strptime(form.date_start.data, '%d.%m.%Y')
    n_auto = form.number_auto.data

    if date_end <= date_start:
        raise Exception('Дата окончания аренды раньше даты начала.')

    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        id_box = cur.execute('''SELECT ID_Box, min(Price)
                                FROM Box
                                WHERE (Brand = :mark) and (Status = :opened)''',
                             {'mark': mark,
                              'opened': OPENED}).fetchone()[0]

        cnt = cur.execute("SELECT COUNT(*) FROM Placed WHERE Car_Number = :n_auto",
                          {'n_auto': n_auto}).fetchone()[0]

        # Если нашли бокс
        # и автомобиль с этим номером не занимает никакой другой бокс
        if (id_box is not None) and (cnt == 0):
            cur.execute('''INSERT INTO Placed (ID_Box, Car_Number, Rent_Start, Rent_End)
                           VALUES (:id_box, :n_auto, :start, :end)''',
                        {'id_box': id_box,
                         'n_auto': n_auto,
                         'start': date_start,
                         'end': date_end})

            cur.execute("UPDATE Box SET Status = :busy WHERE ID_Box = :id_box",
                        {'busy': BUSY,
                         'id_box': id_box})

            # Записываем новую машину в базу
            cnt = cur.execute("SELECT COUNT(*) FROM Cars WHERE Car_Number = :n_auto",
                              {'n_auto': n_auto}).fetchone()[0]

            if cnt == 0:
                client = cur.execute("SELECT ID_Client FROM Clients WHERE Phone = :phone",
                                     {'phone': session['phone']}).fetchone()

                cur.execute('''INSERT INTO Cars (Car_Number, ID_client, Brand)
                               VALUES (:n_auto, :id_client, :mark)''',
                            {'n_auto': n_auto,
                             'id_client': client[0],
                             'mark': mark})

            return True

    return False


def refuse(phone, ticket_id):
    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()
        # Проверить пользователя ли эта квитанция
        # сделать все остальное
        # ?????
        # PROFIT



# ADMIN INFO
def get_list_cwm(form):
    mark_name = form.mark_name.data

    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        cur.execute('''SELECT Clients.First_Name, Clients.Middle_Name, Clients.Second_Name
                       FROM Clients, Cars
                       WHERE (Cars.Brand = :mark_name) and (Clients.ID_client = Cars.ID_client)''',
                    {'mark_name': mark_name})

        info = cur.fetchall()

    return info


def get_list_cde(form):
    date = form.date_end.data

    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        cur.execute('''SELECT Clients.First_Name, Clients.Middle_Name, Clients.Second_Name
                       FROM Clients, Cars, Placed
                       WHERE (Placed.Rent_End = :date) AND (Placed.Car_Number = Cars.Car_Number)
                       AND (Clients.ID_client = Cars.ID_client)''',
                    {'date': date})

        info = cur.fetchall()

    return info


def get_list_c():
    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        info = cur.execute('''SELECT Clients.First_Name, Clients.Middle_Name,
                                Clients.Second_Name, Clients.Address
                              FROM Clients''').fetchall()

    return info