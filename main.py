# coding: utf-8

from flask import Flask
from flask import request, render_template, url_for

from flask_caching import Cache

import models


config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
}

app = Flask(__name__)
app.config.from_mapping(config)

cache = Cache(app)


@app.route('/')
def home():
    return render_template('home.html.jinja2')


@app.route('/me')
def me():
    return render_template('me.html.jinja2')


def _translate(key):
    language = cache.get('language') or 'fr-FR'
    cache.set('language', language)
    lang = {
        'fr-FR': {
            '//test': 'Test traduction en français',
        },
        'en-EN': {
            '//test': 'Test traduction in english',
        }
    }
    value = lang.get(language, dict()).get(key, 'Wrong translation key ! Please clean your cache (CTRL+SHIT+R)')
    return value


@app.route('/api/translate', methods=['POST'])
def translate():
    """
        Post parameters:
            route: the current browser route to get its current page
            tid: Translation id
        :return: Translated text required
    """
    route = request.form.get('route')
    tid = request.form.get('tid')
    return _translate('%s/%s' % (route, tid))


@app.route('/api/setLanguage', methods=['POST'])
def setLanguage():
    cache.set('language', request.form.get('language', 'fr-FR'))
    return {}


@app.route('/api/language', methods=['POST'])
def getLanguage():
    langs = models.Language().select()
    available = dict()
    for lang in langs:
        available[lang['key']] = url_for('static', filename=lang['image'])
    print(available)
    return {
        'current': cache.get('language'),
        'available': available
    }


app.run()
