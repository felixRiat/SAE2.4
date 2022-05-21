#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__,
                        template_folder='templates')


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()
    ##RECUPERATION DE LA DATE:
    sql_date = "SELECT DATE(NOW()) AS date;"
    mycursor.execute(sql_date)
    date = mycursor.fetchall()
    date = date[0]['date']
    ## CREATION D'UNE NOUVELLE COMMANDE :
    id_etat = 1
    id_user = session['user_id']
    tuple_crea = (date, id_etat, id_user)
    sql_crea = "INSERT INTO COMMANDE(date_achat, id_etat, id_user) VALUES (%s, %s, %s)"
    mycursor.execute(sql_crea, tuple_crea)
    get_db().commit()
    ## RECUPERATION DE L'ID DE LA COMMANDE:
    sql_id_cmd = "SELECT last_insert_id() as id_cmd;"
    mycursor.execute(sql_id_cmd)
    id_cmd = mycursor.fetchone()
    id_cmd = id_cmd['id_cmd']
    ## RECUPERATION DE L'ID DU PANIER DE L'UTILISATEUR
    tuple_id_panier = (id_user)
    sql_id_panier = "SELECT id_panier FROM PANIER WHERE id_user = %s;"
    mycursor.execute(sql_id_panier, tuple_id_panier)
    id_panier = mycursor.fetchone()
    id_panier = id_panier['id_panier']
    ## RECUPERATION DES LIGNES DU PANIER:
    tuple_panier = (id_panier)
    sql_panier = "SELECT * FROM ligne_panier WHERE id_panier = %s;"
    mycursor.execute(sql_panier, tuple_panier)
    panier = mycursor.fetchall()

    for ligne in panier:
        id_meuble = ligne['id_meuble']
        qte = ligne['quantite']
        color = ligne['id_couleur']
        tuple_insert = (id_meuble, id_cmd, qte, color)
        sql_insert = "INSERT INTO ligne_commande(id_meuble, id_commande, quantite, id_couleur) VALUES (%s, %s, %s, %s);"
        mycursor.execute(sql_insert, tuple_insert)
        tuple_delete = (id_meuble, id_panier, color)
        sql_delete = "DELETE FROM ligne_panier WHERE id_meuble = %s AND id_panier = %s AND id_couleur = %s;"
        mycursor.execute(sql_delete, tuple_delete)
        get_db().commit()



    flash(u'Commande ajoutée')
    return redirect('/client/meuble/show')
    #return redirect(url_for('client_index'))

@client_commande.route('/client/commande/show', methods=['GET','POST'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_user = session['user_id']
    id_cmd = request.form.get('idCommande', '')
    tuple_detail = (id_cmd)
    sql_detail = '''
    SELECT
    MEUBLE.libelle_meuble as libelle_meuble,
    ligne_commande.quantite as quantite,
    MEUBLE.prix_meuble as prix,
    ligne_commande.id_couleur as id_couleur,
    COULEUR.libelle_couleur,
    SUM(ligne_commande.quantite * MEUBLE.prix_meuble) as prix_ligne
    FROM ligne_commande
    INNER JOIN MEUBLE ON MEUBLE.id_meuble = ligne_commande.id_meuble
    INNER JOIN COULEUR ON COULEUR.id_couleur = ligne_commande.id_couleur
    WHERE ligne_commande.id_commande = %s
    GROUP BY MEUBLE.id_meuble, ligne_commande.id_couleur;
    '''
    mycursor.execute(sql_detail, tuple_detail)
    meubles_commande = mycursor.fetchall()

    tuple_select = (id_user)
    sql = '''SELECT
    COMMANDE.id_commande as id_cmd,
    COMMANDE.date_achat as date_achat, 
    ETAT.libelle_etat as libelle_etat,
    ETAT.id_etat as etat_id,
    SUM(ligne_commande.quantite)as nbr_meuble,
    SUM(ligne_commande.quantite * MEUBLE.prix_meuble) as prix_total
    FROM COMMANDE
    INNER JOIN ETAT ON ETAT.id_etat = COMMANDE.id_etat
    INNER JOIN ligne_commande ON ligne_commande.id_commande = COMMANDE.id_commande
    INNER JOIN MEUBLE ON MEUBLE.id_meuble = ligne_commande.id_meuble
    WHERE COMMANDE.id_user = %s
    GROUP BY COMMANDE.id_commande
    ORDER BY COMMANDE.date_achat DESC;
    '''
    mycursor.execute(sql, tuple_select)
    commandes = mycursor.fetchall()
    return render_template('client/commandes/show.html', commandes=commandes, meubles_commande=meubles_commande)

