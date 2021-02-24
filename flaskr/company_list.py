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
        'SELECT id,ticker_symbol FROM post ORDER BY ticker_symbol ASC'
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


def get_post(id):
    post = get_db().execute(
        'SELECT id, ticker_symbol'
        ' FROM post'
        ' WHERE id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))


    return post           


@bp.route('/<int:id>/delete', methods=('POST','GET'))
def delete(id):
    get_post(id)
    db = get_db()
    db.execute(
        'DELETE FROM post'
        ' WHERE id = ?',
        (id,)
    )
    db.commit()
    return redirect(url_for('company_list.index'))