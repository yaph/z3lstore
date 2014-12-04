# -*- coding: utf-8 -*-
from flask import Flask, abort, request, render_template
from lib.z3l import Z3L
from lib.cache import cachedrequest

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('store.cfg', silent=True)


@cachedrequest(app.config['CACHE_DIR'], app.config['CACHE_LIFETIME'])
def request_zazzle(params):
    return Z3L(app.config['STORE_ID']).get_products(params)


def get_params(params=None):
    default_params = {
        'bg': 'F5F5F5',
        'ps': 9,
        'pg': 1,
        'qs': '',
        'st': 'popularity',
        'sp': 30}
    default_params.update(list(request.args.items()))
    if params is not None:
        default_params.update(params)
    return default_params


def get_result(params=None):
    result = request_zazzle(get_params(params))
    if len(result):
        return result
    abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404


@app.route('/')
def home():
    return render_template('home.html', feed=get_result())


@app.route('/tag/<tag>/')
def tag(tag=None):
    return render_template('tag.html', feed=get_result({'qs': tag}))


@app.route('/search/<search>')
def search(search=None):
    return render_template('search.html', feed=get_result({'qs': search}))


@app.route('/about/')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run()
