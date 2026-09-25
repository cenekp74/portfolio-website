from app import app
from flask import g, request, render_template, send_from_directory, url_for, abort
from jinja2 import TemplateNotFound

# english stays on the original URLs, czech lives under /cs/
LANGS = {'en': '', 'cs': '/cs'}
app.url_map.redirect_defaults = False  # otherwise / redirects to /index

UI = {
    'en': {
        'about': 'About',
        'work': 'Work experience',
        'projects': 'Projects',
        'lang_switch': 'Čeština',
        'og_locale': 'en_US',
        'og_description': 'Full stack web developer and Python developer based in Prague, Czech Republic.',
    },
    'cs': {
        'about': 'O mně',
        'work': 'Pracovní zkušenosti',
        'projects': 'Projekty',
        'lang_switch': 'English',
        'og_locale': 'cs_CZ',
        'og_description': 'Full stack webový vývojář a Python vývojář z Prahy.',
    },
}

def route(*rules):
    """Registers the view under every rule for each language in LANGS."""
    def deco(f):
        for lang, prefix in LANGS.items():
            for rule in rules:
                app.add_url_rule(prefix + rule, view_func=f, defaults={'lang': lang})
        return f
    return deco

def render(template):
    return render_template(f"{g.lang}/{template}")

@app.url_value_preprocessor
def pull_lang(endpoint, values):
    g.lang = values.pop('lang', 'en') if values else 'en'

@app.url_defaults
def add_lang(endpoint, values):
    if 'lang' not in values and app.url_map.is_endpoint_expecting(endpoint, 'lang'):
        values['lang'] = g.get('lang', 'en')

@app.context_processor
def inject_lang():
    lang = g.get('lang', 'en')
    other = 'cs' if lang == 'en' else 'en'
    alternates, switch_url = {}, None
    if request.url_rule and app.url_map.is_endpoint_expecting(request.endpoint, 'lang'):
        alternates = {l: url_for(request.endpoint, lang=l, _external=True, **request.view_args) for l in LANGS}
        switch_url = url_for(request.endpoint, lang=other, **request.view_args)
    return {'lang': lang, 't': UI[lang], 'alternates': alternates, 'switch_url': switch_url}

@app.route('/favicon.ico')
def send_favicon():
    return send_from_directory('static/img', 'favicon.ico')

@route('/', '/index')
def index():
    return render("index.html")

@route('/about')
def about():
    return render("about.html")

@route('/work')
def work():
    return render("work.html")

@route('/projects')
def projects():
    return render("projects.html")

@route('/projects/<project_name>')
def project(project_name):
    try:
        return render(f"projects/{project_name}.html")
    except TemplateNotFound:
        abort(404)
