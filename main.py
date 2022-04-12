# coding: utf-8

from flask import Flask
from flask import redirect, request, render_template, session, url_for

import models


config = {
    "DEBUG": True,
    "SECRET_KEY": 'secretlol',
}

app = Flask(__name__)
app.config.from_mapping(config)


def build_page(page):
    context = {'is_admin': False}
    if user_logged_in():
        context['is_admin'] = True
    return render_template(page, **context)


@app.route('/')
def home():
    session.permanent = False
    return build_page('home.html.jinja2')


@app.route('/me')
def me():
    return build_page('me.html.jinja2')


def _translate(key):
    language = session.get('language') or 'fr-FR'
    return models.Translation().get_translation(language, key)


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
    return _translate('%s%s' % (route, tid))


@app.route('/api/translate/edit', methods=['POST'])
def edit_translation():
    """
        Post parameters:
            route: the current browser route to get its current page
            tid: Translation id
            content: Translated text
        :return: Nothing
    """
    if not user_logged_in():
        return ""
    route = request.form.get('route')
    tid = request.form.get('tid')
    content = request.form.get('content')
    language = session.get('language') or 'fr-FR'

    models.Translation().apply_translations(language, route, tid, content)
    return redirect(route)


@app.route('/api/setLanguage', methods=['POST'])
def set_language():
    session['language'] = request.form.get('language', 'fr-FR')
    return {}


@app.route('/api/language', methods=['POST'])
def get_language():
    langs = models.Language().select()
    available = dict()
    for lang in langs:
        available[lang['key']] = url_for('static', filename=lang['image'])
    return {
        'current': session.get('language', 'fr-FR'),
        'available': available
    }


@app.route('/login')
def login_page():
    if user_logged_in():
        return redirect('/')
    return build_page('login.html.jinja2')


@app.route('/api/login', methods=['POST'])
def login():
    """
        Post parameters:
            login: the current browser route to get its current page
            password: Translation id
        :return: "refresh" if correct credentials else "no"
    """
    user = request.form.get('user')
    password = request.form.get('password')
    if models.User().check_password(user, password):
        session["username"] = user
        session["password"] = password
    return redirect('/')


def user_logged_in():
    user = session.get("username")
    password = session.get("password")
    return models.User().check_password(user, password)


app.run()
