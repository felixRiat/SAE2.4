#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

client_meuble = Blueprint('client_meuble', __name__,
                        template_folder='templates')

@client_meuble.route('/client/index')
@client_meuble.route('/client/meuble/show')      # remplace /client
def client_meuble_show():                                 # remplace client_index
    #Affichege meuble avec filtre
    sql = "SELECT * FROM MEUBLE INNER JOIN IMAGES ON IMAGES.id_meuble = MEUBLE.id_meuble"
    list_param = []
    condition_and = ""
    if "filter_word" in session or "filter_prix_min" in session or "filter_prix_max" in session or "filter_types" in session:
        sql = sql + " WHERE "
    if "filter_word" in session:
        sql = sql + " MEUBLE.libelle_meuble LIKE %s "
        recherche = "%" + session["filter_word"] + "%"
        list_param.append(recherche)
        condition_and = " AND "
    if "filter_prix_min" in session or "filter_prix_max" in session:
        sql = sql + condition_and + " MEUBLE.prix_meuble BETWEEN %s AND %s "
        list_param.append(session["filter_prix_min"])
        list_param.append(session["filter_prix_max"])
        condition_and = " AND "
    if "filter_types" in session:
        sql = sql + condition_and + "("
        last_item = session['filter_types'][-1]
        for item in session['filter_types']:
            sql = sql + "MEUBLE.id_type_meuble = %s"
            if item != last_item:
                sql = sql + " or "
            list_param.append(item)
        sql = sql + ")"
    tuple_select = tuple(list_param)
    sql = sql + " GROUP BY IMAGES.id_meuble;"
    mycursor = get_db().cursor()
    mycursor.execute(sql, tuple_select)
    meubles = mycursor.fetchall()
    for meuble in meubles:
        tuple_couleur = (meuble['id_meuble'])
        sql_couleur = '''SELECT COULEUR.id_couleur as id_couleur, COULEUR.libelle_couleur, coloris.stock as stock
                FROM coloris
                INNER JOIN COULEUR ON COULEUR.id_couleur = coloris.id_couleur
                WHERE coloris.id_meuble = %s'''
        mycursor.execute(sql_couleur, tuple_couleur)
        meuble['stock_couleur'] = mycursor.fetchall()
        stock = 0
        for couleur in meuble['stock_couleur']:
            stock += couleur['stock']
        meuble['stock_meuble'] = stock
    #type de meuble
    sql2 = "SELECT * FROM TYPE_MEUBLE;"
    mycursor.execute(sql2)
    types_meuble = mycursor.fetchall()
    #PANIER
    tuple_select_3 = (session['user_id'])
    sql3 = '''SELECT 
    MEUBLE.libelle_meuble as nom, 
    ligne_panier.quantite as qte,
    ligne_panier.id_couleur as id_couleur,
    MEUBLE.prix_meuble as prix,
    COULEUR.libelle_couleur as libelle_couleur,
    MEUBLE.id_meuble as id_meuble
    FROM ligne_panier
    INNER JOIN MEUBLE ON MEUBLE.id_meuble = ligne_panier.id_meuble
    INNER JOIN PANIER ON PANIER.id_panier = ligne_panier.id_panier
    INNER JOIN COULEUR ON COULEUR.id_couleur = ligne_panier.id_couleur
    WHERE PANIER.id_user = %s;'''
    mycursor.execute(sql3, tuple_select_3)
    articles_panier = mycursor.fetchall()

    for meuble in articles_panier:
        tuple_stock = (meuble['id_couleur'], meuble['id_meuble'])
        sql_stock = '''
        SELECT stock FROM coloris
        WHERE id_couleur = %s
        AND id_meuble = %s;
        '''
        mycursor.execute(sql_stock, tuple_stock)
        meuble['stock'] = mycursor.fetchone()['stock']
        print( meuble['stock'])

    tuple_prix_total = (session['user_id'])
    sql_prix_total = '''SELECT SUM(ligne_panier.quantite * MEUBLE.prix_meuble) as prix_total 
    FROM ligne_panier
    INNER JOIN MEUBLE ON MEUBLE.id_meuble = ligne_panier.id_meuble
    INNER JOIN PANIER ON PANIER.id_panier = ligne_panier.id_panier
    WHERE PANIER.id_user = %s;'''
    mycursor.execute(sql_prix_total, tuple_prix_total)
    prix_total = mycursor.fetchone()['prix_total']

    return render_template('client/boutique/panier_meuble.html', MEUBLES=meubles, articlesPanier=articles_panier, prix_total=prix_total, itemsFiltre=types_meuble)

@client_meuble.route('/client/meuble/details/<int:id>', methods=['GET'])
def client_article_details(id):
    tuple_id_meuble = (id)
    mycursor = get_db().cursor()
    sql = '''SELECT
    MEUBLE.id_meuble,
    MEUBLE.dimension_meuble,
    MEUBLE.poids_meuble,
    MEUBLE.prix_meuble,
    MEUBLE.libelle_meuble,
    IMAGES.url_image,
    IMAGES.id_image,
    MARQUE.libelle_marque,
    TYPE_MEUBLE.libelle_type_meuble
    FROM MEUBLE 
    INNER JOIN IMAGES ON IMAGES.id_meuble = MEUBLE.id_meuble 
    INNER JOIN MARQUE ON MARQUE.id_marque = MEUBLE.id_marque
    INNER JOIN TYPE_MEUBLE ON TYPE_MEUBLE.id_type_meuble = MEUBLE.id_type_meuble
    WHERE MEUBLE.id_meuble = %s 
    GROUP BY IMAGES.id_meuble;'''
    mycursor.execute(sql, tuple_id_meuble)
    meubles=mycursor.fetchone()

    tuple_couleur = (meubles['id_meuble'])
    sql_couleur = '''SELECT COULEUR.id_couleur as id_couleur, COULEUR.libelle_couleur, coloris.stock as stock
            FROM coloris
            INNER JOIN COULEUR ON COULEUR.id_couleur = coloris.id_couleur
            WHERE coloris.id_meuble = %s'''
    mycursor.execute(sql_couleur, tuple_couleur)
    meubles['stock_couleur'] = mycursor.fetchall()
    stock = 0
    for couleur in meubles['stock_couleur']:
        stock += couleur['stock']
    meubles['stock_meuble'] = stock
    sql2 = "SELECT * FROM IMAGES WHERE id_meuble = %s;"
    mycursor.execute(sql2, tuple_id_meuble)
    images=mycursor.fetchall()
    avis=None
    commentaires=None
    return render_template('client/boutique/meuble_details.html', MEUBLE=meubles, IMAGES=images, commentaires=commentaires, avis=avis)