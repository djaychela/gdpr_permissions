from pyramid.view import view_config
from gdpr_permissions.services.pupils_service import PupilsService


@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
def my_view(request):
    return {'project': 'gdpr_permissions'}


@view_config(route_name='list',renderer='templates/list.jinja2')
def list_view(request):
    pupils_list = PupilsService.get_pupils()
    for pupil in pupils_list:
        print(f'got a pupil back - {pupil}')
        print(pupil.first_name, pupil.last_name, pupil.cap_web_photo,
              pupil.cap_web_video, pupil.cap_ext_photo, pupil.cap_ext_video)
    return {'project': 'gdpr_permissions', 'pupils': pupils_list}