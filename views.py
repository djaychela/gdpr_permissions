from pyramid.view import view_config
from gdpr_permissions.services.pupils_service import PupilsService
from gdpr_permissions.services.user_service import UsersService
from gdpr_permissions.services.classes_service import ClassesService


def convert_form_boolean(form_input):
    if form_input is None:
        return True
    return False


@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
def my_view(request):
    return {'project': 'gdpr_permissions'}


@view_config(route_name='list', renderer='templates/list.jinja2')
def list_view(request):
    PupilsService.capabilities_dict()
    sort_order = request.GET.get('sort')
    if sort_order is None or sort_order == 'last_name':
        sort_order = 'last_name.asc()'
    else:
        sort_order += '.desc()'
    filter = request.GET.get('filter')
    class_filter = request.GET.get('class_filter')
    if class_filter is None:
        class_filter = '*'
    pupils_list = PupilsService.get_pupils_list(sort_order, class_filter)
    capability_list = PupilsService.capabilities()
    capability_dict = PupilsService.capabilities_dict()
    classes_dict = ClassesService.get_all_classes()
    return {'pupils': pupils_list, 'capability_list': capability_list,
            'capabilities_nice': capability_dict, 'classes_dict': classes_dict, 'filter': filter,
            'class_filter': class_filter}


@view_config(route_name='users', renderer='templates/users.jinja2')
def user_view(request):
    users_list = UsersService.get_users_list()
    return {'users': users_list}


@view_config(route_name='edit', renderer='templates/edit.jinja2',
             request_method='GET')
def edit_pupil(request):
    pupil_id = int(request.GET.get('id'))
    pupil_info = PupilsService.get_single_pupil(pupil_id)
    capability_list = PupilsService.capabilities()
    capability_current = PupilsService.current_capabilities(pupil_id)
    return {'pupil': pupil_info, 'capability_list': capability_list, 'capability_current': capability_current}


@view_config(route_name='edit', renderer='templates/edit.jinja2',
             request_method='POST')
def store_pupil(request):
    pupil_id = int(request.GET.get('id'))
    form_return = request.GET.get('save_return')
    print(form_return)
    pupil_data_to_store = {}
    for attribute in PupilsService.attributes():
        pupil_data_to_store[attribute] = request.POST.get(attribute)
    for capability in PupilsService.capabilities():
        pupil_data_to_store[capability] = convert_form_boolean(request.POST.get(capability))
    PupilsService.store_pupil_data(pupil_data_to_store)
    pupil_info = PupilsService.get_single_pupil(pupil_id)
    capability_list = PupilsService.capabilities()
    capability_current = PupilsService.current_capabilities(pupil_id)
    return {'pupil': pupil_info, 'capability_list': capability_list, 'capability_current': capability_current}


@view_config(route_name='list_2', renderer='templates/list_2.jinja2')
def list_2(request):
    PupilsService.capabilities_dict()
    sort_order = request.GET.get('sort')
    if sort_order is None or sort_order == 'last_name':
        sort_order = 'last_name.asc()'
    else:
        sort_order += '.desc()'
    class_filter = request.GET.get('class_filter')
    if class_filter is None:
        class_filter = '*'
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


@view_config(route_name='class_list_capabilities', renderer='templates/class_list_capabilities.jinja2')
def class_list_capabilities(request):
    class_filter = request.GET.get('class_filter')
    classes_dict = ClassesService.get_all_classes()
    class_capability_dict = PupilsService.get_pupils_overview(class_filter)
    return {'classes_dict': classes_dict, 'class_filter': class_filter, 'class_capability_dict': class_capability_dict}


@view_config(route_name='update_overview', renderer='templates/update_overview.jinja2')
def update_overview(request):
    for i in range(PupilsService.get_number_of_pupils()):
        _ = PupilsService.create_pupil_overview(i + 1)
    return {}


@view_config(route_name='import_from_sheets', renderer='templates/import_from_sheets.jinja2')
def import_from_sheets(request):
    return {}
