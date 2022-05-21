#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

admin_dataviz_article = Blueprint('admin_dataviz_article', __name__,
                        template_folder='templates')

@admin_dataviz_article.route('/admin/type-meubles/bilan-stock')
def show_type_article_stock():
    mycursor = get_db().cursor()
    sql_get_cout = '''SELECT 
    COUNT(MEUBLE.id_meuble) as nbr_articles,
    SUM(MEUBLE.prix_meuble) as cout_articles_stock,
    TYPE_MEUBLE.libelle_type_meuble as libelle,
    SUM(coloris.stock) as nbr_articles_stock
    FROM MEUBLE
    INNER JOIN TYPE_MEUBLE ON TYPE_MEUBLE.id_type_meuble = MEUBLE.id_type_meuble
    INNER JOIN coloris ON coloris.id_meuble = MEUBLE.id_meuble
    GROUP BY MEUBLE.id_type_meuble;'''
    mycursor.execute(sql_get_cout)
    types_articles_cout = mycursor.fetchall()
    labels = [str(row['libelle']) for row in types_articles_cout]
    values = [int(row['cout_articles_stock']) for row in types_articles_cout]
    cout_total = 0
    return render_template('admin/dataviz/etat_type_article_stock.html',
                           types_articles_cout=types_articles_cout, cout_total=cout_total
                           , labels=labels, values=values)


@admin_dataviz_article.route('/admin/article/bilan')
def show_article_bilan():
    mycursor = get_db().cursor()

    types_articles_cout = []
    labels = []
    values = []
    cout_total = 0
    return render_template('admin/dataviz/etat_article_vente.html',
                           types_articles_cout=types_articles_cout, cout_total=cout_total
                           , labels=labels, values=values)
