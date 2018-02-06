from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember,forget
from gdpr_permissions.services.pupils_service import PupilsService
from gdpr_permissions.services.user_service import UsersService
from gdpr_permissions.services.classes_service import ClassesService
from gdpr_permissions.services.accounts_service import AccountsService
from gdpr_permissions.services.sheets_import import SheetsImport
import threading


class MyThread(threading.Thread):
    def run(self):
        SheetsImport.import_from_sheets()


def convert_form_boolean(form_input):
    if form_input is None:
        return True
    return False


@view_config(route_name='home', renderer='templates/home.jinja2')
def my_view(request):
    return {'project': 'gdpr_permissions'}


@view_config(route_name='users', renderer='templates/users.jinja2', permission='edit')
def user_view(request):
    users_list = UsersService.get_users_list()
    return {'users': users_list}


@view_config(route_name='edit', renderer='templates/edit.jinja2',
             request_method='GET', permission='edit')
def edit_pupil(request):
    pupil_id = int(request.GET.get('id'))
    pupil_info = PupilsService.get_single_pupil(pupil_id)
    capability_list = PupilsService.capabilities()
    capability_current = PupilsService.current_capabilities(pupil_id)
    return {'pupil': pupil_info, 'capability_list': capability_list, 'capability_current': capability_current}


@view_config(route_name='edit', renderer='templates/edit.jinja2',
             request_method='POST', permission='edit')
def store_pupil(request):
    pupil_id = int(request.GET.get('id'))
    save_return = request.POST.get('save_return')
    save = request.POST.get('save')
    delete_pupil = request.POST.get('delete_pupil')
    pupil_data_to_store = {}
    for attribute in PupilsService.attributes():
        pupil_data_to_store[attribute] = request.POST.get(attribute)
    for capability in PupilsService.capabilities():
        pupil_data_to_store[capability] = convert_form_boolean(request.POST.get(capability))
    PupilsService.store_pupil_data(pupil_data_to_store)
    pupil_info = PupilsService.get_single_pupil(pupil_id)
    capability_list = PupilsService.capabilities()
    capability_current = PupilsService.current_capabilities(pupil_id)
    if save:
        return {'pupil': pupil_info, 'capability_list': capability_list, 'capability_current': capability_current}
    elif save_return:
        return HTTPFound(location=request.route_url('list_2'))
    elif delete_pupil:
        return HTTPFound(location=request.route_url('delete_pupil'))


@view_config(route_name='list_2', renderer='templates/list_2.jinja2', permission='view')
def list_2(request):
    PupilsService.capabilities_dict()
    sort_order = request.GET.get('sort')
    if sort_order is None or sort_order == 'last_name':
        sort_order = 'last_name.asc()'
    else:
        sort_order += '.desc()'
    class_filter = request.GET.get('class_filter')
    if class_filter is None:
        class_filter = 'None'
    pupils_list = PupilsService.get_pupils_list(sort_order, class_filter)
    capability_list = PupilsService.capabilities()
    capability_dict = PupilsService.capabilities_dict()
    classes_dict = ClassesService.get_all_classes()
    return {'pupils': pupils_list, 'capability_list': capability_list,
            'capabilities_nice': capability_dict, 'classes_dict': classes_dict, 'filter': filter,
            'class_filter': class_filter}


@view_config(route_name='classes_list', renderer='templates/classes_list.jinja2')
def classes_list(request):
    print(ClassesService.get_all_classes())
    return {}


@view_config(route_name='class_list_capabilities', renderer='templates/class_list_capabilities.jinja2', permission='view')
def class_list_capabilities(request):
    class_filter = request.GET.get('class_filter')
    classes_dict = ClassesService.get_all_classes()
    class_capability_dict = PupilsService.get_pupils_overview(class_filter)
    return {'classes_dict': classes_dict, 'class_filter': class_filter, 'class_capability_dict': class_capability_dict}


@view_config(route_name='class_list_year_capabilities', renderer='templates/class_list_year_capabilities.jinja2', permission='view')
def class_list_year_capabilities(request):
    year_filter = request.GET.get('year_filter')
    year_group_list = ClassesService.get_all_year_groups()
    year_group_list = list(set(year_group_list))
    year_group_list = sorted(year_group_list)
    year_capability_dict = PupilsService.get_pupils_year_overview(year_filter)
    return {'year_group_list': year_group_list, 'year_filter': year_filter, 'year_capability_dict': year_capability_dict}


@view_config(route_name='update_overview', renderer='templates/update_overview.jinja2')
def update_overview(request):
    for i in range(PupilsService.get_number_of_pupils()):
        _ = PupilsService.create_pupil_overview(i + 1)
    return {}


@view_config(route_name='import_from_sheets_1', renderer='templates/import_from_sheets_1.jinja2', permission='edit')
def import_from_sheets_1(request):
    return {}


@view_config(route_name='import_from_sheets_2', renderer='templates/import_from_sheets_2.jinja2', permission='edit')
def import_from_sheets_2(request):
    MyThread().start()
    return {}


@view_config(route_name='auth', match_param='action=out', renderer='string')
def sign_in_out(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username:
        user = UsersService.by_name(username)
        if user and AccountsService.check_password_hash(password, user.password_hash):
            headers = remember(request, user.username)
        else:
            headers = forget(request)
    else:
        headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)


@view_config(route_name='signin', renderer='templates/signin.jinja2')
def sign_in(request):
    return {}


@view_config(route_name='year_group_update_1', renderer='templates/year_group_update_1.jinja2', permission='edit')
def year_group_update_1(request):
    return {}


@view_config(route_name='year_group_update_2', renderer='templates/year_group_update_2.jinja2', permission='edit')
def year_group_update_2(request):
    _ = PupilsService.pupil_year_update()
    return {}


@view_config(route_name='delete_pupil', renderer='templates/delete_pupil.jinja2', permission='edit')
def delete_pupil(request):
    return {}