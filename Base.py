# -*- coding: utf-8 -*-
"""
Created on Fri May 20 08:45:41 2022

@author: ruben.castaneda
"""

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def add_material(conn, material):
    """
    Create a new material into the materials table
    :param conn:
    :param material:
    :return: material id
    """
    sql = ''' INSERT INTO materials(name,kappa11,kappa12,kappa21,kappa22,Cp,rho,typekappa)
              VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, material)
    conn.commit()
    #return cur.lastrowid

def select_material(conn, name):
    """
    Query tasks by name
    :param conn: the Connection object
    :param name:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM materials WHERE name=?", (name,))

    rows = cur.fetchall()
    
    #for row in rows:
    #    print(row)
    return rows

def select_all_materials(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM materials ORDER BY name")

    rows = cur.fetchall()

    #for row in rows:
    #    print(row)
        
    return rows

def materials():
    database = "Database\materials.db"

    sql_create_materials_table = """ CREATE TABLE IF NOT EXISTS materials (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        kappa11 double NOT NULL,
                                        kappa12 double NOT NULL,
                                        kappa21 double NOT NULL,
                                        kappa22 double NOT NULL,
                                        typekappa integer NOT NULL,
                                        Cp double NOT NULL,
                                        rho double NOT NULL
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create materials table
        create_table(conn, sql_create_materials_table)
        
    else:
        print("Error! cannot create the database connection.")
    
    return conn

def update_material(conn, material):
    """
    update name, kappa11, kappa12, kappa21, kappa22, typekappa, Cp, rho,   of a id
    :param conn:
    :param material:
    :return: project id
    """
    sql = ''' UPDATE materials
              SET name = ? ,
                  kappa11 = ? ,
                  kappa12 = ? ,
                  kappa21 = ? ,
                  kappa22 = ? ,
                  Cp = ? ,
                  rho = ? ,
                  typekappa = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, material)
    conn.commit()

def delete_task(conn, id):
    """
    Delete a material by material id
    :param conn:  Connection to the SQLite database
    :param id: id of the material
    :return:
    """
    sql = 'DELETE FROM materials WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

"""if __name__ == '__main__':

    conn = materials()
    rows = select_all_materials(conn)
    #for i in range(len(rows)):
        #display(rows[i][1])
    #with conn:
        # create a new project
    material = ('Aluminium 2024-O',2780.0,0.0,0.0,0.0,875.0,193.0,0)
    material_id = add_material(conn, material)
    material = ('Aluminium 2024-T4',2780.0,0.0,0.0,0.0,875.0,121.0,0)
    material_id = add_material(conn, material)
    material = ('Aluminium 6061-O',2700.0,0.0,0.0,0.0,896.0,180.0,0)
    material_id = add_material(conn, material)
    material = ('Aluminium 6061-T4',2700.0,0.0,0.0,0.0,896.0,154.0,0)
    material_id = add_material(conn, material)
    material = ('Aluminium 6061-T6',2700.0,0.0,0.0,0.0,896.0,167.0,0)
    material_id = add_material(conn, material)
    material = ('Aluminium 7075-T6',2810.0,0.0,0.0,0.0,960.0,130.0,0)
    material_id = add_material(conn, material)
    material = ('Aluminum 1050-H14',2705.0,0.0,0.0,0.0,900.0,227.0,0)
    material_id = add_material(conn, material)
    material = ('Aluminum 1060-H12',2705.0,0.0,0.0,0.0,900.0,230.0,0)
    material_id = add_material(conn, material)
    material = ('Aluminum 1100-H12',2710.0,0.0,0.0,0.0,904.0,220.0,0)
    material_id = add_material(conn, material)
    material = ('Aluminum 1145-H18',2700.0,0.0,0.0,0.0,904.0,227.0,0)
    material_id = add_material(conn, material)
    material = ('Aluminum 1199-H18',2700.0,0.0,0.0,0.0,900.0,240.0,0)
    material_id = add_material(conn, material)
    material = ('Aluminum 2024-T6',2780.0,0.0,0.0,0.0,875.0,151.0,0)
    material_id = add_material(conn, material)
    material = ('Aluminum 5052-H32',2680.0,0.0,0.0,0.0,880.0,138.0,0)
    material_id = add_material(conn, material)
    material = ('Aluminum 6061-T8',2700.0,0.0,0.0,0.0,896.0,170.0,0)
    material_id = add_material(conn, material)
    material = ('Aluminum 6063-T1',2700.0,0.0,0.0,0.0,900.0,193.0,0)
    material_id = add_material(conn, material)
    material = ('Aluminum 7075-O',2810.0,0.0,0.0,0.0,960.0,173.0,0)
    material_id = add_material(conn, material)
    material = ('Aluminum 7175-T66',2800.0,0.0,0.0,0.0,864.0,142.0,0)
    material_id = add_material(conn, material)
    material = ('Copper Cold-worked',8960.0,0.0,0.0,0.0,385.0,385.0,0)
    material_id = add_material(conn, material)
    material = ('Copper Zinc Alloy',8580.0,0.0,0.0,0.0,377.0,9.8,0)
    material_id = add_material(conn, material)
    material = ('Copper Tin Selenide',5940.0,0.0,0.0,0.0,310.0,3.5,0)
    material_id = add_material(conn, material)
    material = ('Titanium',4500.0,0.0,0.0,0.0,528.0,17.0,0)
    material_id = add_material(conn, material)
    material = ('Titanium Ti-6Al-4V (Grade 5)',4430.0,0.0,0.0,0.0,526.3,6.7,0)
    material_id = add_material(conn, material)
    material = ('AISI 1018 Steel',7870.0,0.0,0.0,0.0,486.0,51.9,0)
    material_id = add_material(conn, material)
    material = ('AISI 1045 Steel',7850.0,0.0,0.0,0.0,486.0,49.8,0)
    material_id = add_material(conn, material)"""
      