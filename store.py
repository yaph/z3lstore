# -*- coding: utf-8 -*-
from flask import Flask, abort, request, render_template
from lib.z3l import Z3L

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('store.cfg', silent=True)


def get_params(params):
    default_params = {'bg': 'F5F5F5', 'ps': 9, 'pg': 1}
#    for k,v in request.args.items():
#        default_params[k] = v
    print default_params
    default_params.update(request.args.items())
    print default_params
    default_params.update(params)
    print default_params
    return default_params


def get_result(params):
    result = Z3L(app.config['STORE_ID']).get_products(get_params(params))
    if len(result): return result
    abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404


@app.route('/')
def home():
    return render_template('home.html', feed=get_result({'qs': ''}))


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

