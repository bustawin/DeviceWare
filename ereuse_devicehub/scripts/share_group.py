import argparse
import json

from pydash import find

from ereuse_devicehub import DeviceHub
from ereuse_devicehub.security.perms import READ
from ereuse_devicehub.tests import Client
from ereuse_devicehub.utils import Naming


def share_group(app: DeviceHub, email: str, password: str, group_type: str, receiver_email: str, perm=READ,
                group_id: str = None, group_name=None):
    """
    Sets the permission for the user in the group, known as sharing. If the user had an existing permission,
    this is replaced.

    To use this method, you will need to create a file:

        from app import app
        from ereuse_devicehub

    :param email: Email of the person sharing the group.
    :param password: Password of the person sharing the group.
    :param app: DeviceHub app, needed for the configs (database info, etc).
    :param group_type: Ex: ``Lot``.
    :param receiver_email: The e-mail of the user to share the group to.
    :param perm:
    :param group_id: Optional. The identifier of the group. Name xor group id needed.
    :param group_name: Optional. The name of the group. Name xor group id needed.
    """
    if not group_id and not group_name:
        raise ValueError('Group name xor group_id needed.')
    c = Client(app=app)
    c.prepare()
    token = c.login(email, password)['token']
    kwargs = {'params': {'where': json.dumps({'label': group_name})}} if group_name else {'item': group_id}
    kwargs['token'] = token
    group = c.get_200(Naming.resource(group_type), **kwargs)['_items'][0]
    account_params = {'where': json.dumps({'email': receiver_email})}
    receiver = c.get_200(c.ACCOUNTS, params=account_params, token=token)['_items'][0]
    existing_perm = find(group.setdefault('perms', []), {'_id': receiver['_id']})
    if existing_perm:
        existing_perm['perm'] = perm
    else:
        group['perms'].append({'account': receiver['_id'], 'perm': perm})
    group_patch = {'@type': group_type, 'perms': group['perms']}
    return c.patch_200(Naming.resource(group_type), item=group['_id'], data=group_patch, token=token)


def main(app):
    """
    Create a python file with the following contents::

        from app import app  # Where your ``DeviceHub()`` is defined
        from ereuse_devicehub.scripts.share_group import main
        main(app)

    And execute it.
    """
    desc = 'Share a group.'
    epilog = 'Minimum example: python share_group.py a@a.a 1234 Lot b@b.b -i identifier'
    parser = argparse.ArgumentParser(description=desc, epilog=epilog)
    parser.add_argument('email', help='The email of the person sharing this.')
    parser.add_argument('password', help='The password of the person sharing this.')
    parser.add_argument('group_type')
    parser.add_argument('receiver_email', help='The email of the user that this is being shared to.')
    parser.add_argument('-i', '--group_id', help='The group id.')
    parser.add_argument('-n', '--group_name', help='The group name. If set, this is used over the id. '
                                                   'Note that names are not unique, use the id when possible.')
    parser.add_argument('-p', '--perm', help='The permission the user will have. READ by default.')
    args = vars(parser.parse_args())
    response = share_group(app, **args)
    print('Response:')
    print(json.dumps(response, indent=4))
