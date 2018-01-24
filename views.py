from pyramid.view import view_config
from gdpr_permissions.services.pupils_service import PupilsService
from gdpr_permissions.services.user_service import UsersService

def convert_form_boolean(form_input):
    if form_input is None:
        return True
    return False


@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
def my_view(request):
    return {'project': 'gdpr_permissions'}


@view_config(route_name='list',renderer='templates/list.jinja2')
def list_view(request):
    pupils_list = PupilsService.get_pupils_list()
    return {'project': 'gdpr_permissions', 'pupils': pupils_list}


@view_config(route_name='users',renderer='templates/users.jinja2')
def user_view(request):
    users_list = UsersService.get_users_list()
    return {'project': 'gdpr_permissions', 'users': users_list}


@view_config(route_name='edit', renderer='templates/edit.jinja2',
             request_method='GET')
def edit_pupil(request):
    pupil_info = PupilsService.get_single_pupil(1)
    capability_list = PupilsService.capabilities()
    return {'project': 'gdpr_permissions', 'pupil': pupil_info, 'capability_list': capability_list}


@view_config(route_name='edit', renderer='templates/edit.jinja2',
             request_method='POST')
def store_pupil(request):
    attributes = PupilsService.all_attributes()
    pupil_data_to_store = {}
    for attribute in attributes:
        pupil_data_to_store[attribute] = convert_form_boolean(request.POST.get(attribute))
    print(f'pupil_data_to_store: {pupil_data_to_store}')
    pupil_info = PupilsService.get_single_pupil(1)
    return {'project': 'gdpr_permissions', 'pupil': pupil_info}
