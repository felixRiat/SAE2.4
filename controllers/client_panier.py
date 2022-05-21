#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                        template_folder='templates')

@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    ################################################
    # CREATION D'UN PANIER SI LE CLIENT N'EN A PAS #
    #      ET RECUPERATION DE L'ID DU PANIER       #
    ################################################
    id_client = session['user_id']
    tuple_id_client = (id_client)
    mycursor = get_db().cursor()
    sql = "SELECT * FROM PANIER WHERE id_user = %s;"
    mycursor.execute(sql, tuple_id_client)
    panier = mycursor.fetchall()
    if panier == () or panier == None:
        sql_inser = "INSERT INTO PANIER(id_user) VALUES (%s);"
        mycursor.execute(sql_inser, tuple_id_client)
        get_db().commit()
        sql = "SELECT * FROM PANIER WHERE id_user = %s;"
        mycursor.execute(sql, tuple_id_client)
        panier = mycursor.fetchall()
    id_panier = panier[0]['id_panier']
    ################################################
    #    AJOUT OU UPDATE LIGNE PANIER CONCERNER    #
    ################################################
    id_meuble = request.form.get('id_meuble','')
    qte = request.form.get('quantite', '')
    couleur = request.form.get('id_couleur', '')

    tuple_get_meuble = (id_meuble, couleur)
    sql_get_meuble = "SELECT stock as stock FROM coloris WHERE id_meuble = %s AND id_couleur = %s;"
    mycursor.execute(sql_get_meuble, tuple_get_meuble)
    meuble = mycursor.fetchone()
    print(meuble, tuple_get_meuble)
    stock = meuble['stock'] - int(qte)
    tuple_edit_qte = (stock, id_meuble, couleur)
    sql_edit_qte = "UPDATE coloris SET stock = %s WHERE id_meuble = %s AND id_couleur = %s;"
    mycursor.execute(sql_edit_qte, tuple_edit_qte)
    get_db().commit()

    tuple_select = (id_panier, id_meuble, couleur)
    sql_select_ligne = '''SELECT ligne_panier.quantite FROM ligne_panier 
    INNER JOIN MEUBLE ON MEUBLE.id_meuble = ligne_panier.id_meuble
    WHERE ligne_panier.id_panier = %s
    AND ligne_panier.id_meuble = %s
    AND ligne_panier.id_couleur = %s;'''
    mycursor.execute(sql_select_ligne, tuple_select)
    ligne = mycursor.fetchone()
    if ligne == () or ligne == None:
        tuple_add = (id_panier, id_meuble, couleur, qte)
        sql_add = "INSERT INTO ligne_panier(id_panier, id_meuble, id_couleur, quantite) VALUES (%s, %s, %s, %s);"
        mycursor.execute(sql_add, tuple_add)
        get_db().commit()
    else:
        qte = int(qte) + ligne['quantite']
        tuple_update = (qte, id_panier, id_meuble, couleur)
        sql_update = "UPDATE ligne_panier SET quantite = %s WHERE id_panier = %s AND id_meuble = %s AND id_couleur = %s;"
        mycursor.execute(sql_update, tuple_update)
        get_db().commit()
    return redirect('/client/meuble/show')

@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_meuble = request.form.get('id_meuble', '')
    couleur = request.form.get('id_couleur', '')
    #recuperation de la quantité commandé :
    tuple_recup = (id_meuble, couleur)
    sql_recup = '''SELECT ligne_panier.quantite as qte FROM ligne_panier
    INNER JOIN MEUBLE ON MEUBLE.id_meuble = ligne_panier.id_meuble
    WHERE ligne_panier.id_meuble = %s
    AND ligne_panier.id_couleur = %s;'''
    mycursor.execute(sql_recup, tuple_recup)
    qte_commande = mycursor.fetchone()
    qte_after = qte_commande['qte'] - 1
    # get id panier:
    id_client = session['user_id']
    tuple_get = (id_client)
    sql_get = "SELECT PANIER.id_panier as id_panier FROM PANIER WHERE id_user = %s;"
    mycursor.execute(sql_get, tuple_get)
    id_panier = mycursor.fetchone()

    if qte_commande['qte'] <= 1:
        # delete ligne:
        tuple_ligne = (id_meuble, id_panier['id_panier'], couleur)
        sql_ligne = "DELETE FROM ligne_panier WHERE id_meuble = %s AND id_panier = %s AND id_couleur = %s;"
        mycursor.execute(sql_ligne, tuple_ligne)
        get_db().commit()
    else:
        # update ligne:
        tuple_ligne = (qte_after, id_meuble, id_panier['id_panier'], couleur)
        sql_ligne = "UPDATE ligne_panier SET quantite = %s WHERE id_meuble = %s AND id_panier = %s AND id_couleur = %s;"
        mycursor.execute(sql_ligne, tuple_ligne)
        get_db().commit()

    #get stock:
    tuple_get_stock = (id_meuble, couleur)
    sql_get_stock = "SELECT stock as stock FROM coloris WHERE id_meuble = %s AND id_couleur = %s;"
    mycursor.execute(sql_get_stock, tuple_get_stock)
    stock = mycursor.fetchone()

    #update stock:
    stock_after = stock['stock'] + 1
    tuple_stock = (stock_after, id_meuble, couleur)
    sql_stock = "UPDATE coloris SET stock = %s WHERE id_meuble = %s AND id_couleur = %s;"
    mycursor.execute(sql_stock, tuple_stock)
    get_db().commit()

    return redirect('/client/meuble/show')

@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_meuble = request.form.get('id_meuble', '')
    id_couleur = request.form.get('id_couleur', '')
    # recuperation de la quantité commandé :
    tuple_recup = (id_meuble, id_couleur)
    sql_recup = '''SELECT ligne_panier.quantite as qte FROM ligne_panier
        INNER JOIN MEUBLE ON MEUBLE.id_meuble = ligne_panier.id_meuble
        WHERE ligne_panier.id_meuble = %s AND ligne_panier.id_couleur = %s;'''
    mycursor.execute(sql_recup, tuple_recup)
    qte_commande = mycursor.fetchone()
    # get id panier:
    id_client = session['user_id']
    tuple_get = (id_client)
    sql_get = "SELECT PANIER.id_panier as id_panier FROM PANIER WHERE id_user = %s;"
    mycursor.execute(sql_get, tuple_get)
    id_panier = mycursor.fetchone()

    # delete ligne:
    tuple_ligne = (id_meuble, id_panier['id_panier'], id_couleur)
    sql_ligne = "DELETE FROM ligne_panier WHERE id_meuble = %s AND id_panier = %s AND id_couleur = %s;"
    mycursor.execute(sql_ligne, tuple_ligne)
    get_db().commit()

    # get stock:
    tuple_get_stock = (id_meuble, id_couleur)
    sql_get_stock = "SELECT stock as stock FROM coloris WHERE id_meuble = %s AND id_couleur = %s;"
    mycursor.execute(sql_get_stock, tuple_get_stock)
    stock = mycursor.fetchone()

    # update stock:
    stock_after = stock['stock'] + qte_commande['qte']
    tuple_stock = (stock_after, id_meuble, id_couleur)
    sql_stock = "UPDATE coloris SET stock = %s WHERE id_meuble = %s AND id_couleur = %s;"
    mycursor.execute(sql_stock, tuple_stock)
    get_db().commit()

    return redirect('/client/meuble/show')

@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()

    # get id panier:
    id_client = session['user_id']
    tuple_get = (id_client)
    sql_get = "SELECT PANIER.id_panier as id_panier FROM PANIER WHERE id_user = %s;"
    mycursor.execute(sql_get, tuple_get)
    id_panier = mycursor.fetchone()

    #recuperation des lignes du panier
    tuple_panier = (id_panier['id_panier'])
    sql_panier = "SELECT * FROM ligne_panier WHERE id_panier = %s;"
    mycursor.execute(sql_panier, tuple_panier)
    panier = mycursor.fetchall()

    print(panier)
    for ligne in panier:
        id_meuble = ligne['id_meuble']
        id_couleur = ligne['id_couleur']
        tuple_recup = (id_meuble, id_couleur)
        sql_recup = '''SELECT ligne_panier.quantite as qte FROM ligne_panier
                INNER JOIN MEUBLE ON MEUBLE.id_meuble = ligne_panier.id_meuble
                WHERE ligne_panier.id_meuble = %s AND id_couleur = %s;'''
        mycursor.execute(sql_recup, tuple_recup)
        qte_commande = mycursor.fetchone()
        # delete ligne:
        tuple_ligne = (id_meuble, id_panier['id_panier'], id_couleur)
        sql_ligne = "DELETE FROM ligne_panier WHERE id_meuble = %s AND id_panier = %s AND id_couleur = %s;"
        mycursor.execute(sql_ligne, tuple_ligne)
        get_db().commit()

        # get stock:
        tuple_get_stock = (id_meuble, id_couleur)
        sql_get_stock = "SELECT stock FROM coloris WHERE id_meuble = %s AND id_couleur = %s;"
        mycursor.execute(sql_get_stock, tuple_get_stock)
        stock = mycursor.fetchone()

        # update stock:
        stock_after = stock['stock'] + qte_commande['qte']
        tuple_stock = (stock_after, id_meuble, id_couleur)
        sql_stock = "UPDATE coloris SET stock = %s WHERE id_meuble = %s AND id_couleur = %s;"
        mycursor.execute(sql_stock, tuple_stock)
        get_db().commit()


    return redirect('/client/meuble/show')

@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    # SQL
    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)
    print("word:" + filter_word + str(len(filter_word)))
    if filter_word or filter_word == "":
        if len(filter_word) > 1:
            if filter_word.isalpha():
                session['filter_word'] = filter_word
            else:
                flash(u'votre Mot recherché doit uniquement être composé de lettres')
        else:
            if len(filter_word) == 1:
                flash(u'votre Mot recherché doit être composé de au moins 2 lettres')
            else:
                session.pop('filter_word', None)
    if filter_prix_min or filter_prix_max:
        if filter_prix_min.isdecimal() and filter_prix_max.isdecimal():
            if int(filter_prix_min) < int(filter_prix_max):
                session['filter_prix_min'] = filter_prix_min
                session['filter_prix_max'] = filter_prix_max
            else:
                flash(u'min < max')
        else:
            flash(u'min et max doivent être des numériques')
    if filter_types and filter_types != []:
        print("filter_types:", filter_types)
        if isinstance(filter_types, list):
            check_filter_type = True
            for number_type in filter_types:
                print('test', number_type)
                if not number_type.isdecimal():
                    check_filter_type = False
            if check_filter_type:
                session['filter_types'] = filter_types
    return redirect('/client/meuble/show')

@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)
    print("suppr filtre")
    return redirect('/client/meuble/show')

