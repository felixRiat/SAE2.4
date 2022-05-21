#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

admin_meuble = Blueprint('admin_meuble', __name__,
                        template_folder='templates')

@admin_meuble.route('/admin/meubles/show')
def show_meuble():
    mycursor = get_db().cursor()
    sql = '''SELECT
    MEUBLE.id_meuble as id_meuble,
    MEUBLE.libelle_meuble as libelle_meuble,
    MEUBLE.prix_meuble as prix_meuble,
    MEUBLE.dimension_meuble as dimension_meuble,
    MEUBLE.poids_meuble as poids_meuble,
    MEUBLE.id_marque as id_marque,
    MARQUE.libelle_marque as libelle_marque,
    MEUBLE.id_type_meuble as id_type_meuble,
    TYPE_MEUBLE.libelle_type_meuble as libelle_type_meuble
    FROM MEUBLE
    INNER JOIN MARQUE ON MARQUE.id_marque = MEUBLE.id_marque
    INNER JOIN TYPE_MEUBLE ON TYPE_MEUBLE.id_type_meuble = MEUBLE.id_type_meuble
    ORDER BY MARQUE.libelle_marque, MEUBLE.libelle_meuble;'''
    mycursor.execute(sql)
    meubles = mycursor.fetchall()
    for meuble in meubles:
        tuple_couleur = (meuble['id_meuble'])
        sql_couleur = '''SELECT COULEUR.libelle_couleur, coloris.stock
        FROM coloris
        INNER JOIN COULEUR ON COULEUR.id_couleur = coloris.id_couleur
        WHERE coloris.id_meuble = %s'''
        mycursor.execute(sql_couleur, tuple_couleur)
        meuble['stock_meuble'] = mycursor.fetchall()
    print(meubles)
    return render_template('admin/meuble/show_meuble.html', MEUBLE=meubles)

@admin_meuble.route('/admin/meuble/add', methods=['GET'])
def add_meuble():
    mycursor = get_db().cursor()
    sql = "SELECT * FROM TYPE_MEUBLE;"
    mycursor.execute(sql)
    type_meuble = mycursor.fetchall()
    sql = "SELECT * FROM MARQUE;"
    mycursor.execute(sql)
    marque = mycursor.fetchall()
    sql = "SELECT * FROM COULEUR;"
    mycursor.execute(sql)
    couleur = mycursor.fetchall()
    print(couleur)
    return render_template('admin/meuble/add_meuble.html', TYPE_MEUBLE=type_meuble, MARQUE=marque, couleurs=couleur)

@admin_meuble.route('/admin/meuble/add', methods=['POST'])
def valid_add_meuble():
    libelle_meuble = request.form.get('libelle_meuble', '')
    stock_meuble = request.form.get('stock_meuble', '')
    prix_meuble = request.form.get('prix_meuble', '')
    dimension_meuble = request.form.get('dimension_meuble', '')
    poids_meuble = request.form.get('poids_meuble', '')
    id_marque = request.form.get('id_marque', '')
    id_type_meuble = request.form.get('id_type_meuble', '')
    id_couleur = request.form.get('id_couleur', '')

    tuple_insert = (libelle_meuble, prix_meuble, dimension_meuble, poids_meuble, id_marque, id_type_meuble)
    sql = "INSERT INTO MEUBLE (libelle_meuble, prix_meuble, dimension_meuble, poids_meuble, Id_marque, Id_type_meuble) VALUES(%s, %s, %s, %s, %s, %s);"
    mycursor = get_db().cursor()
    mycursor.execute(sql, tuple_insert)
    get_db().commit()

    sql_id_meuble = "SELECT last_insert_id() as id_meuble;"
    mycursor.execute(sql_id_meuble)
    id_meuble = mycursor.fetchone()['id_meuble']

    tuple_insert_stock = (id_meuble, id_couleur, stock_meuble)
    sql_insert_stock = '''INSERT INTO coloris(id_meuble, id_couleur, stock) VALUES (%s, %s, %s);'''
    mycursor.execute(sql_insert_stock, tuple_insert_stock)
    get_db().commit()

    return redirect(url_for('admin_meuble.show_meuble'))

@admin_meuble.route('/admin/meuble/delete', methods=['GET'])
def delete_meuble():
    id = request.args.get('id', '')
    flag = request.args.get('flag', '')
    id_type = request.args.get('id_type', '')
    print(id)
    tuple_delete = (id)
    sql = "DELETE FROM IMAGES WHERE id_meuble = %s;"
    sql1 = "DELETE FROM coloris WHERE id_meuble = %s;"
    sql2 = "DELETE FROM fait_de WHERE id_meuble = %s;"
    sql3 = "DELETE FROM vend WHERE id_meuble = %s;"
    sql4 = "DELETE FROM MEUBLE WHERE id_meuble = %s;"

    mycursor = get_db().cursor()
    mycursor.execute(sql, tuple_delete)
    mycursor.execute(sql1, tuple_delete)
    mycursor.execute(sql2, tuple_delete)
    mycursor.execute(sql3, tuple_delete)
    mycursor.execute(sql4, tuple_delete)
    get_db().commit()

    print("un article supprimé, id :", id)
    flash(u'un article supprimé, id : ' + id)
    if flag == 'meuble':
        return redirect(url_for('admin_meuble.show_meuble'))
    else:
        return redirect(url_for('admin_type_meuble.delete_type_meuble_meuble', id_type_meuble=id_type))

@admin_meuble.route('/admin/meuble/edit/<int:id>', methods=['GET'])
def edit_meuble(id):
    mycursor = get_db().cursor()
    sql = "SELECT * FROM TYPE_MEUBLE;"
    mycursor.execute(sql)
    type_meuble = mycursor.fetchall()
    sql = "SELECT * FROM MARQUE;"
    mycursor.execute(sql)
    marque = mycursor.fetchall()
    tuple_select = (id)
    sql = "SELECT * FROM MEUBLE WHERE id_meuble = %s;"
    mycursor.execute(sql, tuple_select)
    meuble = mycursor.fetchone()

    sql = '''SELECT * FROM coloris 
    INNER JOIN COULEUR ON COULEUR.id_couleur = coloris.id_couleur
    WHERE id_meuble = %s;'''
    mycursor.execute(sql, tuple_select)
    couleur = mycursor.fetchall()
    return render_template('admin/meuble/edit_meuble.html', MARQUE=marque, TYPE_MEUBLE=type_meuble, MEUBLE=meuble, couleurs=couleur)

@admin_meuble.route('/admin/meuble/edit', methods=['POST'])
def valid_edit_article():
    id_meuble = request.form.get('id_meuble', '')
    libelle_meuble = request.form.get('libelle_meuble', '')
    prix_meuble = request.form.get('prix_meuble', '')
    dimension_meuble = request.form.get('dimension_meuble', '')
    poids_meuble = request.form.get('poids_meuble', '')
    id_marque = request.form.get('id_marque', '')
    id_type_meuble = request.form.get('id_type_meuble', '')

    tuple_update = (libelle_meuble, prix_meuble, dimension_meuble, poids_meuble, id_marque, id_type_meuble, id_meuble)
    sql = "UPDATE MEUBLE SET libelle_meuble = %s, prix_meuble = %s, dimension_meuble = %s, poids_meuble = %s, Id_marque = %s, Id_type_meuble = %s WHERE id_meuble = %s;"
    mycursor = get_db().cursor()
    mycursor.execute(sql, tuple_update)
    get_db().commit()

    tuple_get_couleur = (id_meuble)
    sql_get_couleur = '''SELECT * FROM coloris WHERE id_meuble = %s;'''
    mycursor.execute(sql_get_couleur, tuple_get_couleur)
    couleurs = mycursor.fetchall()
    for couleur in couleurs:
        id_couleur = couleur['id_couleur']
        stock = request.form.get(str(id_couleur), '')
        tuple_update_stock = (stock, id_couleur, id_meuble)
        sql_update_stock = '''UPDATE coloris SET stock = %s WHERE id_couleur = %s AND id_meuble = %s;'''
        mycursor.execute(sql_update_stock, tuple_update_stock)
        get_db().commit()

    return redirect(url_for('admin_meuble.show_meuble'))
