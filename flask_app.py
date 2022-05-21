from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from flask import Blueprint

from controllers.auth_security import *

from controllers.client_meuble import *
from controllers.client_panier import *
from controllers.client_commande import *

from controllers.admin_meuble import *
from controllers.admin_commande import *
from controllers.admin_type_meuble import *
from controllers.admin_dataviz_meuble import *

flask_app = Flask(__name__)
flask_app.secret_key = 'une cle(token) : grain de sel(any random string)'

@flask_app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@flask_app.route('/')
def show_accueil():
    return render_template('auth/layout.html')

##################
# Authentification
##################

# Middleware de sécurité

@flask_app.before_request
def before_request():
     if request.path.startswith('/admin') or request.path.startswith('/client'):
        if 'role' not in session:
            return redirect('/login')
            #return redirect(url_for('auth_login'))
        else:
            if (request.path.startswith('/client') and session['role'] != 'ROLE_client') or (request.path.startswith('/admin') and session['role'] != 'ROLE_admin'):
                print('pb de route : ', session['role'], request.path.title(), ' => deconnexion')
                session.pop('username', None)
                session.pop('role', None)
                return redirect('/login')
                #return redirect(url_for('auth_login'))

flask_app.register_blueprint(auth_security)

flask_app.register_blueprint(client_meuble)
flask_app.register_blueprint(client_panier)
flask_app.register_blueprint(client_commande)

flask_app.register_blueprint(admin_meuble)
flask_app.register_blueprint(admin_commande)
flask_app.register_blueprint(admin_dataviz_article)
flask_app.register_blueprint(admin_type_meuble)

if __name__ == '__main__':
    flask_app.run()
