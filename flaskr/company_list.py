from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('company_list', __name__)

@bp.route('/')
def index():
    db = get_db()
    ticker_symbols = db.execute(
        'SELECT t.id, ticker_symbol, created'
        ' FROM ticker_symbols t JOIN user u on t.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('company_list/index.html', ticker_symbols=ticker_symbols)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        ticker_symbol = request.form['ticker_symbol']
        error = None

        if not ticker_symbol:
            error = 'Ticker symbol is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO ticker_symbols (ticker_symbol, author_id)'
                ' VALUES (?, ?)',
                (ticker_symbol,g.user['id'],)
            )
            db.commit()
            return redirect(url_for('company_list.index'))

    return render_template('company_list/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT t.ticker_symbol, created, author_id'
        ' FROM ticker_symbols t JOIN user u ON author_id = u.id'
        ' WHERE t.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    ticker_symbols = get_post(id)

    if request.method == 'POST':
        ticker_symbol = request.form['ticker_symbol']
        error = None

        if not ticker_symbol:
            error = 'Ticker Symbol is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE ticker_symbols SET ticker_symbol = ?'
                ' WHERE id = ?',
                (ticker_symbol, id)
            )
            db.commit()
            return redirect(url_for('company_list.index'))

    return render_template('company_list/update.html', ticker_symbols=ticker_symbols)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('company_list.index'))
