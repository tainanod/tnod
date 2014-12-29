import datetime

import ckan.plugins as p
import ckan.plugins.toolkit as tk
import ckan.lib.navl.dictization_functions as df
import ckan.new_authz as new_authz

import db


schema = {
    'id': [tk.get_validator('ignore_empty'), unicode],
    'content': [tk.get_validator('ignore_missing'), unicode],
    'user_id': [tk.get_validator('ignore_missing'), unicode],
    'created': [tk.get_validator('ignore_missing'),
                tk.get_validator('isodate')],
}


def search_add(context, data_dict):
    '''
    Add an item to the search_history for the current user.

    :param content: Search query to add to history
    :type content: string
    '''
    try:
        tk.check_access('ckanext_search_history_add', context, data_dict)
    except tk.NotAuthorized:
        #JOE#
        #tk.abort(401, tk._('Not authorized to add history item'))
        pass
    if db.search_history_table is None:
        db.init_db(context['model'])

    content = tk.get_or_bust(data_dict, 'content')
    username = context.get('user')
    #JOE#
    #user_id = new_authz.get_user_id_for_username(username, allow_none=False)
    user_id = new_authz.get_user_id_for_username(username, allow_none=True)

    search_history = db.SearchHistory()
    search_history.content = content
    search_history.user_id = user_id
    session = context['session']
    session.add(search_history)
    session.commit()
    return db.table_dictize(search_history, context)


@tk.side_effect_free
def search_list(context, data_dict):
    '''
    List the search history

    :param limit: The number of items to show (optional, default: 10)
    :type limit: int
    '''
    tk.check_access('ckanext_search_history_list', context, data_dict)
    if db.search_history_table is None:
        db.init_db(context['model'])
    username = context.get('user')
    user = new_authz.get_user_id_for_username(username, allow_none=False)
    limit = data_dict.get('limt')
    history = db.SearchHistory.search_history(user_id=user, limit=limit)
    result = []
    if history:
        for item in history:
            result.append(db.table_dictize(item, context))
    return result
