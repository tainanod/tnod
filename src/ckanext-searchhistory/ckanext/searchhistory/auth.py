import ckan.plugins as p
import ckan.new_authz as new_authz


def search_add(context, data_dict):
    username = context.get('user')
    user = new_authz.get_user_id_for_username(username, allow_none=True)
    #JOE#
    #if user is None:
    #    return {'success': False, 'msg': 'Not authorized'}
    return {'success': True}

def search_list(context, data_dict):
    return search_add(context, data_dict)
