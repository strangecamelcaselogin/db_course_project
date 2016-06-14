from hashlib import sha256
from datetime import date

import sqlite3 as lite

from flask import session

from settings import *

def form_mark_list():

    brand = dict()

    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        cur.execute("SELECT Car_Brands.Brand FROM Car_Brands")

        rows = cur.fetchall()
        print(rows)
        for row in rows:
            brand[row[0]] = row[0]

    return brand


def form_ticket_list():
    ticket = dict()

    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        cur.execute("SELECT Placed.Ticket_Number FROM Placed, Cars, Clients "
                    "WHERE (Placed.Car_Number = Cars.Car_Number) and (Clients.ID_client = Cars.ID_client)"
                    "and (Clients.Phone = :phone)",
                    {'phone': session['phone']})

        rows = cur.fetchall()
        for row in rows:
            ticket[row[0]] = row[0]

    return ticket

# LOGIN ADN REGISTER
def login(form):
    phone = form.phone.data
    hashed_password = sha256(form.password.data.encode('utf-8')).hexdigest()

    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()
        cur.execute('''SELECT  * FROM Clients WHERE Phone = :phone AND Password = :password''',
                    {'phone': phone, 'password': hashed_password})

        data = cur.fetchall()

        if len(data) == 1:
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

        cur.execute("SELECT * FROM Clients WHERE Phone = :phone", {'phone': phone})

        if len(cur.fetchall()) == 0:
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
def close_box(form):
    id_box = form.cb_box_code.data
    status = '2'

    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Box WHERE ID_Box = :id",
                    {'id': id_box})

        if len(cur.fetchall()) != 0:
            cur.execute('''UPDATE Box SET Status = :status  WHERE ID_Box = :id''',
                        {'id': id_box,
                         'status': status})
            return True

    return False


def add_mark(mark_name):
    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Car_Brands WHERE Brand = :mark",
                    {'mark': mark_name})

        if len(cur.fetchall()) == 0:
            cur.execute('''INSERT INTO Car_Brands (Brand) VALUES (:mark)''',
                        {'mark': mark_name})
            return True

    return False

def add_box(form):
    mark_name = form.nb_mark_name.data
    cost = form.cost.data
    status = '0'

    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Car_Brands WHERE Brand = :mark",
                    {'mark': mark_name})

        if len(cur.fetchall()) != 0:
            cur.execute('''INSERT INTO Box (Brand, Price, Status) VALUES (:mark, :cost, :status)''',
                        {'mark': mark_name,
                         'cost': cost,
                         'status': status})

            return True

    return False

def delete_mark(mark_name):
    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Car_Brands WHERE Brand = :mark",
                    {'mark': mark_name})

        print('что тут?',cur.fetchall()[0])
        print(mark_name)
        if len(cur.fetchall()) == 0:
            print('112233')
            cur.execute('''DELETE FROM Car_Brands WHERE Brand = :mark''',
                        {'mark': mark_name})
            return True

    return False

def update_box(form):
    n = float(form.u_cost.data.replace(',', '.'))

    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()
        cur.execute("UPDATE Box SET Price = Price * :n",
                    {'n': n})
        return True

    return False

# RENT
def rent_(form):
    mark = form.mark_list.data
    date_end = form.date_end.data
    date_start = form.date_start.data
    n_auto = form.number_auto.data


    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()
        cur.execute("SELECT ID_Box, min(Price) FROM Box WHERE (Brand = :mark) and (Status = '0')",
                    {'mark': mark})

        rows = cur.fetchall()

        cur.execute("SELECT * FROM Placed WHERE Car_Number = :n_auto",
                    {'n_auto': n_auto})

        if (len(rows[0]) != 0) and (len(cur.fetchall()) == 0):
            cur.execute('''INSERT INTO Placed (ID_Box, Car_Number, Rent_Start, Rent_End) VALUES (:id_box, :n_auto, :start, :end)''',
                        {'id_box': rows[0][0],
                         'n_auto': n_auto,
                         'start': date_start,
                         'end': date_end})

            cur.execute( '''UPDATE Box SET Status = '1' WHERE ID_Box = :id_box''',
                        {'id_box': rows[0][0]})

            #записываем новую машину в базу
            cur.execute("SELECT * FROM Cars WHERE Car_Number = :n_auto",
                        {'n_auto': n_auto})

            if (len(cur.fetchall()) == 0):

                #print('user', session['phone'])
                cur.execute("SELECT ID_Client FROM Clients WHERE Phone = :phone",
                            {'phone': session['phone']})

                row_client = cur.fetchall()

                cur.execute('''INSERT INTO Cars (Car_Number, ID_client, Brand) VALUES (:n_auto, :id_client, :mark)''',
                                {'n_auto': n_auto,
                                 'id_client': row_client[0][0],
                                 'mark': mark})

            return True

    return False


# ADMIN INFO
def get_list_cwm(form):
    mark_name = form.mark_name.data

    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        cur.execute("select Clients.First_Name, Clients.Middle_Name, Clients.Second_Name from Clients, Cars "
                    "where  (Cars.Brand = :mark_name) and (Clients.ID_client = Cars.ID_client)",
                    {'mark_name': mark_name})

        info = cur.fetchall()

    return info


def get_list_cde(form):
    date = form.date_end.data

    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        cur.execute("select Clients.First_Name, Clients.Middle_Name, Clients.Second_Name from Clients, Cars, Placed "
                    "where  "
                    "(Placed.Rent_End = :date) and (Placed.Car_Number = Cars.Car_Number) "
                    "and (Clients.ID_client = Cars.ID_client)",
                    {'date': date})

        info = cur.fetchall()

    return info


def get_list_c():

    con = lite.connect(DATABASE)
    with con:
        cur = con.cursor()

        cur.execute("select Clients.First_Name, Clients.Middle_Name, Clients.Second_Name, Clients.Address from Clients")

        info = cur.fetchall()

    return info


def refuse():
    pass