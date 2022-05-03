# Jinja

- declare a block: `{% block block-name %}{% endblock %}`

- extend a template: `{% extends 'template-filename' %}`

- loop through an array: `{% for val in array %} ... {% endfor %}`

- execute on condition: `{% if condition %} ... {% else if condition %} ... {% else %} ... {% endif %}`

- get URL from route: `{{ url_for('route') }}` can take parameters for each value in the route

- get a URL from static: `{{ url_for('static', filename='relpath-to-file') }}` \
`'relpath-to-file'` is in `'static'`, a subfolder the the application
