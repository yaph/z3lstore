# -*- coding: utf-8 -*-
from flask import Flask, abort, request, render_template, flash
from models import db, User, Feed, FeedItem

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('store.cfg', silent=True)


def get_params(params):
    default_params = {}
    for k,v in request.args.items():
        default_params[k] = v
    default_params.update(params)
    return default_params


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/user/<username>')
def user_show(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_show.html', user=user)


@app.route('/feed/all/')
def feed_all():
    return render_template('feed_all.html',
        feeds=Feed.query.order_by(Feed.created.desc()).all()
    )


@app.route('/feed/add/', methods=['GET', 'POST'])
def feed_add():
    if request.method == 'POST':
        if not request.form['url']:
            flash('URL is required', 'error')
        elif not request.form['type']:
            flash('Type is required', 'error')
        else:
            feed = Feed(request.form['url'], request.form['type'])
            db.session.add(feed)
            db.session.commit()
            flash(u'Feed was successfully created')
            return redirect(url_for('feed_all'))
    return render_template('feed_add.html')


@app.route('/feed/update', methods=['POST'])
def feed_update():
    pass


@app.route('/feed/delete/<int:id>')
def feed_delete():
#    if DELETE
#    db.session.delete(feed)
#    db.session.commit()
    return render_template('feed_delete.html')


if __name__ == '__main__':
#    app.run()
    app.run(debug=True)

