import sqlite3 as lite
from hashlib import sha256

from flask import session

from settings import *


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
def add_box():
    pass


def delete_box():
    pass


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
    status = '1'

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

def delete_mark():
    pass