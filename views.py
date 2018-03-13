from pyramid.view import view_config, forbidden_view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from gdpr_permissions.services.pupils_service import PupilsService
from gdpr_permissions.services.user_service import UsersService
from gdpr_permissions.services.classes_service import ClassesService
from gdpr_permissions.services.accounts_service import AccountsService
from gdpr_permissions.services.capabilities_service import CapabilitiesService
from gdpr_permissions.services.sheets_import import SheetsImport
from gdpr_permissions.services.logging_service import LoggingService
from gdpr_permissions.services.groups_service import GroupsService
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
@forbidden_view_config(renderer='templates/signin.jinja2')
def user_view(request):
    users_list = UsersService.get_users_list()
    return {'users': users_list}


@view_config(route_name='edit', renderer='templates/edit.jinja2',
             request_method='GET', permission='edit')
def edit_pupil(request):
    pupil_id = int(request.GET.get('id'))
    pupil_info = PupilsService.get_single_pupil(pupil_id)
    capability_list = CapabilitiesService.get_capabilities()
    capability_current = PupilsService.current_capabilities(pupil_id)
    classes_dict = ClassesService.get_all_classes()
    capability_names = CapabilitiesService.get_capabilities(mode='nice')
    return {'pupil': pupil_info, 'capability_list': capability_list, 'capability_current': capability_current,
            'classes_dict': classes_dict, 'capability_names': capability_names}


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
    for capability in CapabilitiesService.get_capabilities():
        pupil_data_to_store[capability] = convert_form_boolean(request.POST.get(capability))
    print(str(request.POST.get('groups')))
    pupil_data_to_store['groups'] = str(request.POST.get('groups'))
    PupilsService.store_pupil_data(pupil_data_to_store)
    pupil_info = PupilsService.get_single_pupil(pupil_id)
    capability_list = CapabilitiesService.get_capabilities()
    capability_current = PupilsService.current_capabilities(pupil_id)
    classes_dict = ClassesService.get_all_classes()
    capability_names = CapabilitiesService.get_capabilities(mode='nice')
    if save:
        return {'pupil': pupil_info, 'capability_list': capability_list, 'capability_current': capability_current,
                'classes_dict': classes_dict, 'capability_names': capability_names}
    elif save_return:
        return HTTPFound(location=request.route_url('class_view_detail'))
    elif delete_pupil:
        return HTTPFound(location=request.route_url('delete_pupil'))


@view_config(route_name='class_view_detail', renderer='templates/class_view_detail.jinja2', permission='view')
def list_pupils(request):
    class_filter = request.GET.get('class_filter')
    if class_filter is None:
        class_filter = 'None'
    pupils_list = PupilsService.get_pupils_list(class_filter)
    capability_list = CapabilitiesService.get_capabilities()
    capability_nice = CapabilitiesService.get_capabilities(mode='nice')
    classes_dict = ClassesService.get_all_classes()
    capabilities_keys = CapabilitiesService.get_capabilities_keys()
    return {'pupils': pupils_list, 'capability_list': capability_list,
            'capabilities_nice': capability_nice, 'classes_dict': classes_dict, 'filter': filter,
            'class_filter': class_filter, 'capabilities_keys': capabilities_keys}


@view_config(route_name='class_summary_view', renderer='templates/class_summary_view.jinja2',
             permission='view')
def class_list_capabilities(request):
    class_filter = request.GET.get('class_filter')
    classes_dict = ClassesService.get_all_classes()
    class_capability_dict = PupilsService.get_pupils_overview(class_filter)
    return {'classes_dict': classes_dict, 'class_filter': class_filter, 'class_capability_dict': class_capability_dict}


@view_config(route_name='class_list_year_capabilities', renderer='templates/class_list_year_capabilities.jinja2',
             permission='view')
def class_list_year_capabilities(request):
    year_filter = request.GET.get('year_filter')
    year_group_list = ClassesService.get_all_year_groups()
    year_group_list = set(year_group_list)
    year_group_list = sorted(year_group_list)
    year_capability_dict = PupilsService.get_pupils_year_overview(year_filter)
    return {'year_group_list': year_group_list, 'year_filter': year_filter,
            'year_capability_dict': year_capability_dict}


@view_config(route_name='import_from_sheets', renderer='templates/import_from_sheets.jinja2', permission='edit')
def import_from_sheets(request):
    confirm = request.POST.get('confirm')
    if confirm:
        MyThread().start()
    return {'confirm': confirm}


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
    pupil_id = request.GET.get('id')
    mode = request.GET.get('mode')
    pupil_info = PupilsService.get_single_pupil(pupil_id)
    pupil_name = pupil_info['first_name'] + ' ' + pupil_info['last_name']
    if mode == 'confirm':
        PupilsService.delete_single_pupil(pupil_id)
        LoggingService.delete_user_entries(pupil_id)
        return HTTPFound(location=request.route_url('list'))
    return {'pupil_id': pupil_id, 'pupil_name': pupil_name}


@view_config(route_name='create_user', renderer='templates/create_user.jinja2', permission='edit')
def create_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    password_confirm = request.POST.get('password_confirm')
    cancel = request.POST.get('cancel')
    if cancel:
        return HTTPFound(location=request.route_url('users'))
    current_user_list = UsersService.get_users_list()
    error_list = []
    for user in current_user_list:
        if user['username'] == username:
            error_list.append('That username is already in use')
    if password != password_confirm:
        error_list.append('Passwords do not match')
    if password and not error_list and password == password_confirm:
        UsersService.create_new_user(username, password)
        return HTTPFound(location=request.route_url('users'))
    return {'error_list': error_list}


@view_config(route_name='delete_user', renderer='templates/delete_user.jinja2', permission='edit')
def delete_user(request):
    user_id = request.GET.get('user_id')
    confirm = request.GET.get('confirm')
    cancel = request.GET.get('cancel')
    if cancel:
        return HTTPFound(location=request.route_url('users'))
    if confirm:
        UsersService.delete_user(user_id)
        return HTTPFound(location=request.route_url('users'))
    current_user_dict = UsersService.get_current_user_info(user_id)
    username = current_user_dict['username']
    return {'user_id': user_id, 'username': username}


@view_config(route_name='set_password', renderer='templates/set_password.jinja2', permission='view')
def set_password(request):
    error = ''
    user_id = request.GET.get('user_id')
    confirm = request.GET.get('confirm')
    cancel = request.GET.get('cancel')
    password = request.GET.get('password')
    password_confirm = request.GET.get('password_confirm')
    if cancel:
        return HTTPFound(location=request.route_url('users'))
    current_user_dict = UsersService.get_current_user_info(user_id)
    username = current_user_dict['username']
    if password != password_confirm:
        error = "Passwords don't match!"
    if password and password == password_confirm:
        UsersService.change_user_password(user_id, password)
        return HTTPFound(location=request.route_url('users'))
    return {'user_id': user_id, 'error': error, 'username': username}


@view_config(route_name='create_pupil', renderer='templates/create_pupil.jinja2', permission='edit')
def create_pupil(request):
    cancel = request.POST.get('cancel')
    save = request.POST.get('save')
    if cancel:
        return HTTPFound(location=request.route_url('list'))
    if save:
        pupil_data_to_store = {}
        for attribute in PupilsService.attributes():
            pupil_data_to_store[attribute] = request.POST.get(attribute)
        for capability in CapabilitiesService.get_capabilities():
            pupil_data_to_store[capability] = convert_form_boolean(request.POST.get(capability))
        PupilsService.create_new_pupil(pupil_data_to_store)
        return HTTPFound(location=request.route_url('list'))
    capability_keys = CapabilitiesService.get_capabilities_keys()
    capability_names = CapabilitiesService.get_capabilities(mode='nice')
    classes_dict = ClassesService.get_all_classes()
    return {'capability_keys': capability_keys, 'classes_dict': classes_dict, 'capability_names': capability_names}


@view_config(route_name='logfile_read', renderer='templates/logfile_read.jinja2', permission='edit')
def logfile_read(request):
    logfile_contents = LoggingService.read_logfile()
    return {'logfile_contents': logfile_contents}


@view_config(route_name='logfile_pupil_history', renderer='templates/logfile_pupil_history.jinja2', permission='edit')
def logfile_pupil_history(request):
    pupil_id = int(request.GET.get('id'))
    logfile_contents = LoggingService.read_logfile_by_id(pupil_id)
    capability_dict = PupilsService.capabilities_dict()
    capability_list = CapabilitiesService.get_capabilities()
    return {'logfile_contents': logfile_contents, 'capabilities_nice': capability_dict,
            'capability_list': capability_list}


@view_config(route_name='classes_list', renderer='templates/classes_list.jinja2', permission='edit')
def classes_list(request):
    all_class_info = ClassesService.get_all_class_info()
    attributes = ['id', 'class_strand', 'class_year', 'class_teacher']
    return {'all_class_info': all_class_info, 'attributes': attributes}


@view_config(route_name='class_edit', renderer='templates/class_edit.jinja2', permission='edit')
def class_edit(request):
    class_id = request.GET.get('class_id')
    cancel = request.GET.get('cancel')
    submit = request.GET.get('submit')
    attributes = ClassesService.attributes()
    if cancel:
        return HTTPFound(location=request.route_url('classes_list'))
    if submit:
        class_strand = request.GET.get('class_strand')
        class_year = request.GET.get('class_year')
        class_teacher = request.GET.get('class_teacher')
        class_to_store = {'id': class_id}
        for attribute in attributes[1:]:
            class_to_store[attribute] = eval(attribute)
        ClassesService.store_single_class_info(class_to_store)
        return HTTPFound(location=request.route_url('classes_list'))
    class_info = ClassesService.get_single_class_info(class_id)
    return {'class_info': class_info, 'attributes': attributes}


@view_config(route_name='class_create', renderer='templates/class_create.jinja2', permission='edit')
def class_create(request):
    cancel = request.GET.get('cancel')
    submit = request.GET.get('submit')
    attributes = ClassesService.attributes()[1:]
    if cancel:
        return HTTPFound(location=request.route_url('classes_list'))
    if submit:
        class_strand = request.GET.get('class_strand')
        class_year = request.GET.get('class_year')
        class_teacher = request.GET.get('class_teacher')
        class_to_store = {}
        for attribute in attributes:
            class_to_store[attribute] = eval(attribute)
        ClassesService.create_new_class(class_to_store)
        return HTTPFound(location=request.route_url('classes_list'))

    return {'attributes': attributes}


@view_config(route_name='class_delete', renderer='templates/class_delete.jinja2', permission='edit')
def class_delete(request):
    cancel = request.GET.get('cancel')
    confirm = request.GET.get('confirm')
    class_id = request.GET.get('class_id')
    new_class_id = request.GET.get('new_class_id')
    if cancel:
        return HTTPFound(location=request.route_url('classes_list'))
    if confirm:
        PupilsService.update_pupil_classes(class_id, new_class_id)
        ClassesService.delete_class(class_id)
        return HTTPFound(location=request.route_url('classes_list'))
    classes_dict = ClassesService.get_all_classes()
    class_info = ClassesService.get_single_class_info(class_id)
    del classes_dict[int(class_id)]
    return {'class_id': class_id, 'class_info': class_info, 'classes_dict': classes_dict}


@view_config(route_name='capabilities_list', renderer='templates/capabilities_list.jinja2', permission='edit')
def capability_list(request):
    all_capabilities = CapabilitiesService.get_all_capabilities()
    columns = CapabilitiesService.list_all_attributes()
    return {'all_capabilities': all_capabilities, 'columns': columns}


@view_config(route_name='capability_edit', renderer='templates/capability_edit.jinja2', permission='edit')
def capability_edit(request):
    cap_id = request.GET.get('cap_id')
    submit = request.GET.get('submit')
    cancel = request.GET.get('cancel')
    if cancel:
        return HTTPFound(location=request.route_url('capabilities_list'))
    if submit:
        capability = request.GET.get('capability')
        capability_nice = request.GET.get('capability_nice')
        active = request.GET.get('active')
        if active is None:
            active = True
        else:
            active = False
        cap_to_store = {'id': cap_id}
        for attribute in CapabilitiesService.list_all_attributes()[1:]:
            cap_to_store[attribute] = eval(attribute)
        CapabilitiesService.update_capability(cap_to_store)
        return HTTPFound(location=request.route_url('capabilities_list'))
    capability_info = CapabilitiesService.get_single_capability(cap_id)
    attributes = CapabilitiesService.list_all_attributes()
    return {'capability_info': capability_info, 'attributes': attributes}


@view_config(route_name='groups_list', renderer='templates/groups_list.jinja2', permission='edit')
def groups_list(request):
    group_attr_list = GroupsService.list_all_attributes()
    groups_list = GroupsService.get_all_groups()
    return {'group_attr_list': group_attr_list, 'groups_list': groups_list}


@view_config(route_name='group_edit', renderer='templates/group_edit.jinja2', permission='edit')
def group_edit(request):
    cancel = request.GET.get('cancel')
    submit = request.GET.get('submit')
    group_id = request.GET.get('group_id')
    attributes = GroupsService.list_all_attributes()
    if cancel:
        return HTTPFound(location=request.route_url('groups_list'))
    if submit:
        group_name = request.GET.get('group_name')
        group_desc = request.GET.get('group_desc')
        group_to_store={}
        group_to_store['id'] = group_id
        for attribute in attributes[1:]:
            group_to_store[attribute] = eval(attribute)
        GroupsService.store_group_info(group_to_store)
        return HTTPFound(location=request.route_url('groups_list'))
    group_info = GroupsService.get_single_group_info(group_id)
    return {'group_info': group_info, 'attributes': attributes}


@view_config(route_name='group_delete', renderer='templates/group_delete.jinja2', permission='edit')
def group_delete(request):
    cancel = request.GET.get('cancel')
    confirm = request.GET.get('confirm')
    group_id = request.GET.get('group_id')
    if cancel:
        return HTTPFound(location=request.route_url('groups_list'))
    if confirm:
        GroupsService.delete_group(group_id)
        return HTTPFound(location=request.route_url('groups_list'))
    return {'group_id': group_id}


@view_config(route_name='group_create', renderer='templates/group_create.jinja2', permission='edit')
def group_create(request):
    cancel = request.GET.get('cancel')
    submit = request.GET.get('submit')
    attributes = GroupsService.list_all_attributes()
    if cancel:
        return HTTPFound(location=request.route_url('groups_list'))
    if submit:
        group_name = request.GET.get('group_name')
        group_desc = request.GET.get('group_desc')
        group_to_create = {}
        for attribute in attributes[1:]:
            group_to_create[attribute] = eval(attribute)
        print(group_to_create)
        GroupsService.create_new_group(group_to_create)
        return HTTPFound(location=request.route_url('groups_list'))
    return {'attributes': attributes}


@view_config(route_name='groups_view_summary', renderer='templates/groups_view_summary.jinja2', permission='edit')
def groups_view_summary(request):
    group_filter = request.GET.get('group_filter')
    if group_filter is None:
        group_filter = 'None'
    groups_dict = GroupsService.get_group_names()
    group_capability_dict = PupilsService.get_pupils_with_groups_overview(group_filter)
    return {'groups_dict': groups_dict, 'group_capability_dict': group_capability_dict, 'group_filter': group_filter}


@view_config(route_name='groups_view_detail', renderer='templates/groups_view_detail.jinja2', permission='edit')
def groups_view_detail(request):
    group_filter = request.GET.get('group_filter')
    if group_filter is None:
        group_filter = 'None'
    groups_dict = GroupsService.get_group_names()
    pupil_capability_dict = PupilsService.get_pupils_with_groups(group_filter)
    capabilities_keys = CapabilitiesService.get_capabilities_keys()
    for pupil in pupil_capability_dict:
        print(pupil)
    capability_nice = CapabilitiesService.get_capabilities(mode='nice')
    return {'groups_dict': groups_dict, 'pupil_capability_dict': pupil_capability_dict, 'group_filter': group_filter,
            'capabilities_keys': capabilities_keys, 'capabilities_nice': capability_nice,}