__author__ = 'Tim Shaffer'
__email__ = 'timshaffer@me.com'
__version__ = '0.1.0'

import click
from flask import cli
from flask import current_app


def route_iter(app):
    for rule in app.url_map.iter_rules():
        yield {
            'url': rule.rule,
            'methods': ','.join(rule.methods - {'HEAD', 'OPTIONS'}),
            'endpoint': rule.endpoint
        }


def get_routes(app):
    return sorted(route_iter(app), key=lambda r: r['url'])


@click.command()
@cli.with_appcontext
def command():
    for route in get_routes(current_app):
        txt_url = click.style(route['url'], fg='green', bold=True)
        txt_endpoint = click.style(route['endpoint'], fg='red')
        txt_methods = click.style(route['methods'], fg='white')

        click.echo('{} {} ({})'.format(txt_url, txt_endpoint, txt_methods))
