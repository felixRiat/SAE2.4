#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

admin_type_meuble = Blueprint('admin_type_meuble', __name__,
                        template_folder='templates')

@admin_type_meuble.route('/admin/type-meubles/show')
def show_type_meuble():
    mycursor = get_db().cursor()
    sql = '''SELECT TYPE_MEUBLE.id_type_meuble,
     TYPE_MEUBLE.libelle_type_meuble,
     COUNT(MEUBLE.id_meuble) as nb_meuble
     FROM TYPE_MEUBLE
     LEFT JOIN MEUBLE ON MEUBLE.id_type_meuble = TYPE_MEUBLE.id_type_meuble
     GROUP BY TYPE_MEUBLE.id_type_meuble
     ORDER BY TYPE_MEUBLE.libelle_type_meuble;'''
    mycursor.execute(sql)
    type_meuble = mycursor.fetchall()
    return render_template('admin/type_meuble/show_type_meuble.html', TYPE_MEUBLE=type_meuble)

@admin_type_meuble.route('/admin/type-meuble/add', methods=['GET'])
def add_type_meuble():
    return render_template('admin/type_meuble/add_type_meuble.html')

@admin_type_meuble.route('/admin/type-meuble/add', methods=['POST'])
def valid_add_type_meuble():
    libelle = request.form.get('libelle_type_meuble', '')
    tuple_insert = (libelle)
    sql = "INSERT INTO TYPE_MEUBLE(libelle_type_meuble) VALUES (%s);"
    mycursor = get_db().cursor()
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/admin/type-meubles/show')

@admin_type_meuble.route('/admin/type-meuble/delete', methods=['GET'])
def delete_type_meuble():
    id = request.args.get('id_type_meuble', '')
    tuple_delete = (id)
    sql = "SELECT COUNT(*) as nb FROM MEUBLE WHERE id_type_meuble = %s"
    mycursor = get_db().cursor()
    mycursor.execute(sql, tuple_delete)
    nb_meuble = mycursor.fetchall()
    if (nb_meuble[0]['nb'] != 0):
        return redirect(url_for('admin_type_meuble.delete_type_meuble_meuble', id_type_meuble=id))

    sql2 = "DELETE FROM TYPE_MEUBLE WHERE id_type_meuble = %s;"
    mycursor.execute(sql2, tuple_delete)
    get_db().commit()
    return redirect('/admin/type-meubles/show')

@admin_type_meuble.route('/admin/type-meuble/delete-meuble')
def delete_type_meuble_meuble():
    id_type_meuble = request.args.get('id_type_meuble', '')
    tuple_select = (id_type_meuble)
    sql = "SELECT * FROM MEUBLE WHERE id_type_meuble = %s;"
    mycursor = get_db().cursor()
    mycursor.execute(sql, tuple_select)
    meuble = mycursor.fetchall()
    if(meuble == ()):
        tuple_delete = (id_type_meuble)
        sql2 = "DELETE FROM TYPE_MEUBLE WHERE id_type_meuble = %s"
        mycursor.execute(sql2, tuple_delete)
        get_db().commit()
        return redirect(url_for('admin_type_meuble.show_type_meuble'))
    return render_template('admin/type_meuble/delete_type_meuble.html', MEUBLES=meuble)

@admin_type_meuble.route('/admin/type-meuble/edit/<int:id>', methods=['GET'])
def edit_type_meuble(id):
    mycursor = get_db().cursor()
    tuple_edit = (id)
    sql = "SELECT * FROM TYPE_MEUBLE WHERE id_type_meuble = %s;"
    mycursor.execute(sql, tuple_edit)
    type_meuble = mycursor.fetchone()
    return render_template('admin/type_meuble/edit_type_meuble.html', TYPE_MEUBLE=type_meuble)

@admin_type_meuble.route('/admin/type-meuble/edit', methods=['POST'])
def valid_edit_type_meuble():
    libelle = request.form['libelle_type_meuble']
    id_type_meuble = request.form.get('id_type_meuble', '')
    tuple_edit = (libelle, id_type_meuble)
    sql = "UPDATE TYPE_MEUBLE SET libelle_type_meuble = %s WHERE id_type_meuble = %s;"
    mycursor = get_db().cursor()
    mycursor.execute(sql, tuple_edit)
    get_db().commit()

    return redirect('/admin/type-meubles/show') #url_for('show_type_article')

