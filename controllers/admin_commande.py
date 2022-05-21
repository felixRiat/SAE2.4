#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    id_user = session['user_id']
    id_cmd = request.form.get('idCommande', '')
    tuple_detail = (id_cmd)
    sql_detail = '''
        SELECT
        MEUBLE.libelle_meuble as libelle_meuble,
        ligne_commande.quantite as quantite,
        MEUBLE.prix_meuble as prix,
        SUM(ligne_commande.quantite * MEUBLE.prix_meuble) as prix_ligne
        FROM ligne_commande
        INNER JOIN MEUBLE ON MEUBLE.id_meuble = ligne_commande.id_meuble
        WHERE ligne_commande.id_commande = %s
        GROUP BY MEUBLE.id_meuble;
        '''
    mycursor.execute(sql_detail, tuple_detail)
    meubles_commande = mycursor.fetchall()

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
        GROUP BY COMMANDE.id_commande
        ORDER BY COMMANDE.date_achat DESC, COMMANDE.id_etat;
        '''
    mycursor.execute(sql)
    commandes = mycursor.fetchall()
    return render_template('admin/commandes/show.html', commandes=commandes, meubles_commande=meubles_commande)


@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    id_commande = request.form.get('idCommande', '')
    tuple_update = (2, id_commande)
    sql_update = "UPDATE COMMANDE SET id_etat = %s WHERE id_commande = %s;"
    mycursor.execute(sql_update, tuple_update)
    get_db().commit()

    return redirect('/admin/commande/show')