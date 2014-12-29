import ckan.plugins as p
import ckan.new_authz as new_authz

import db


def sysadmin(context, data_dict):
    return {'success':  False}

def anyone(context, data_dict):
    return {'success': True}


def page_privacy(context, data_dict):
    if db.pages_table is None:
        db.init_db(context['model'])
    org_id = data_dict.get('org_id')
    page = data_dict.get('page')
    out = db.Page.get(group_id=org_id, name=page)
    if out and out.private == False:
        return {'success':  True}
    # no org_id means it's a universal page
    if not org_id:
        if out and out.private:
            return {'success': False}
        return {'success': True}
    group = context['model'].Group.get(org_id)
    user = context['user']
    authorized = new_authz.has_user_permission_for_group_or_org(group.id,
                                                                user,
                                                                'read')
    if not authorized:
        return {'success': False,
                'msg': p.toolkit._(
                    'User %s not authorized to read this page') % user}
    else:
        return {'success': True}

# Starting from 2.2 you need to explicitly flag auth functions that allow
# anonymous access
if p.toolkit.check_ckan_version(min_version='2.2'):
    anyone = p.toolkit.auth_allow_anonymous_access(anyone)
    page_privacy = p.toolkit.auth_allow_anonymous_access(page_privacy)


pages_show = page_privacy
pages_update = sysadmin
pages_delete = sysadmin
pages_list = anyone

