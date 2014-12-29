import logging
from pylons import config

import ckan.plugins as p
import ckan.lib.helpers as h

import actions
import auth

log = logging.getLogger(__name__)

def latest_news(*args):
    #result = {}
    #result['limit'] = limit
    return p.toolkit.get_action('ckanext_pages_latest')(None,{'limit':args[0] or 2})
    

class PagesPlugin(p.SingletonPlugin):
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.ITemplateHelpers, inherit=True)
    p.implements(p.IConfigurable, inherit=True)
    p.implements(p.IRoutes, inherit=True)
    p.implements(p.IActions, inherit=True)
    p.implements(p.IAuthFunctions, inherit=True)

    def update_config(self, config):
        p.toolkit.add_template_directory(config, 'theme/templates_main')



    def configure(self, config):
        return

    def get_helpers(self):
        return {
            'latestnews': latest_news
        }

    def after_map(self, map):
        controller = 'ckanext.pages.controller:PagesController'

        map.connect('pages_delete', '/pages_delete{page:/.*|}',
                    action='pages_delete', ckan_icon='delete', controller=controller)
        map.connect('pages_edit', '/pages_edit{page:/.*|}',
                    action='pages_edit', ckan_icon='edit', controller=controller)
        map.connect('pages_show', '/pages{page:/.*|}',
                    action='pages_show', ckan_icon='file', controller=controller, highlight_actions='pages_edit pages_show')
        return map

    def get_actions(self):
        actions_dict = {
            'ckanext_pages_show': actions.pages_show,
            'ckanext_pages_update': actions.pages_update,
            'ckanext_pages_delete': actions.pages_delete,
            'ckanext_pages_list': actions.pages_list,
            'ckanext_pages_latest' : actions.latest_news
        }
        return actions_dict

    def get_auth_functions(self):
        return {
            'ckanext_pages_show': auth.pages_show,
            'ckanext_pages_update': auth.pages_update,
            'ckanext_pages_delete': auth.pages_delete,
            'ckanext_pages_list': auth.pages_list
       }
