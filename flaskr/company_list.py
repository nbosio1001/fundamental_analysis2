from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

# from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('company_list', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT ticker_symbol FROM post ORDER BY ticker_symbol ASC'
    ).fetchall()
    return render_template('company_list/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
# @login_required
def create():
    # post = get_post(id)
    if request.method == 'POST':
        ticker_symbol = request.form['ticker_symbol'].upper()
        db = get_db()
        error = None

        if not ticker_symbol: # Executes if there any kind of empty container
            error = 'Ticker symbol is required.'
            # print(error)
        # print(success)
        # post = db.execute(
        #     'SELECT id FROM post WHERE ticker_symbol = ?', (ticker_symbol,)
        # ).fetchone()
        elif db.execute(
            'SELECT ticker_symbol FROM post WHERE ticker_symbol = ?', (ticker_symbol,)
        ).fetchone() is not None:
            error = 'Ticker Symbol {} is already registered.'.format(ticker_symbol)
        #     post = db.execute(
        #     'SELECT id FROM post WHERE ticker_symbol = ?', (ticker_symbol,)
        # ).fetchone()
        #     print(post)

        if error is None:
            # session.clear()
            # print('This is id: ',id(1))
            # session['author_id'] = post['id']
            db.execute(
                'INSERT INTO post (ticker_symbol) VALUES (?)',
                (ticker_symbol,)
            )
            db.commit()


            return redirect(url_for('company_list.index'))
        flash(error)
    return render_template('company_list/create.html')


# def get_post(id, check_author=True):
#     post = get_db().execute(
#         #'SELECT id, ticker_symbol, body, created, author_id'#, username'
#         'SELECT id, ticker_symbol, created, author_id'
#         ' FROM post'# p JOIN user u ON p.author_id = u.id'
#         ' WHERE id = ?',
#         (id,)
#     ).fetchone()

#     if post is None:
#         abort(404, "Post id {0} doesn't exist.".format(id))

    # if check_author and post['author_id'] != g.user['id']:
    #     abort(403)

    # return post

# @bp.route('/<int:id>/update', methods=('GET', 'POST'))
# # @login_required
# def update(id):
#     post = get_post(id)

#     if request.method == 'POST':
#         ticker_symbol = request.form['ticker_symbol']
#         # body = request.form['body']
#         error = None

#         if not ticker_symbol:
#             error = 'Ticker Symbol is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'UPDATE post SET ticker_symbol = ?'#, body = ?'
#                 ' WHERE id = ?',
#                 (ticker_symbol, body, id)
#             )
#             db.commit()
#             return redirect(url_for('company_list.index'))

#     return render_template('company_list/update.html', post=post)

# @bp.route('/<int:id>/delete', methods=('POST',))
# # @login_required
# def delete(id):
#     get_post(id)
#     db = get_db()
#     db.execute('DELETE FROM post WHERE id = ?', (id,))
#     db.commit()
#     return redirect(url_for('company_list.index'))

# _________________________________________________________






# @bp.before_app_request
# def load_logged_in_user():
#     user_id = session.get('user_id')

#     if user_id is None:
#         g.user = None
#     else:
#         g.user = get_db().execute(
#             'SELECT * FROM user WHERE id = ?', (user_id,)
#         ).fetchone()