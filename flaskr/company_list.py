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
    posts = db.execute(
        'SELECT p.id, ticker_symbol, body, created, author_id, username'
        ' FROM post p JOIN user u on p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('company_list/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        ticker_symbol = request.form['ticker_symbol']
        body = request.form['body']
        error = None

        if not ticker_symbol:
            error = 'Ticker symbol is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (ticker_symbol, body, author_id)'
                ' VALUES (?, ?, ?)',
                (ticker_symbol, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('company_list.index'))

    return render_template('company_list/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, ticker_symbol, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
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
    post = get_post(id)

    if request.method == 'POST':
        ticker_symbol = request.form['ticker_symbol']
        body = request.form['body']
        error = None

        if not ticker_symbol:
            error = 'Ticker Symbol is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET ticker_symbol = ?, body = ?'
                ' WHERE id = ?',
                (ticker_symbol, body, id)
            )
            db.commit()
            return redirect(url_for('company_list.index'))

    return render_template('company_list/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('company_list.index'))
