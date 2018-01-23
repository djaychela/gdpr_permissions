from pyramid.view import view_config
from gdpr_permissions.services.pupils_service import PupilsService
from gdpr_permissions.services.user_service import UsersService


@view_config(route_name='home', renderer='templates/mytemplate.jinja2')
def my_view(request):
    return {'project': 'gdpr_permissions'}


@view_config(route_name='list',renderer='templates/list.jinja2')
def list_view(request):
    pupils_list = PupilsService.get_pupils_list()
    print(pupils_list)
    # pupils_cap=['damers_web','damers_blog','damers_twitter','damers_class_photo','damers_prod_dvd','damers_newsletter', \
    #             'wistia_video','dasp_web','dasp_music_web','dor_echo','cel_pound_mag','cel_pound_web']
    # for pupil in pupils_list:
    #     print(f'got a pupil back - {pupil}')
    #     for cap in pupils_cap:
    #         print(eval('pupil.'+ cap)
    return {'project': 'gdpr_permissions', 'pupils': pupils_list}


@view_config(route_name='users',renderer='templates/users.jinja2')
def user_view(request):
    users_list = UsersService.get_users_list()
    print(users_list)
    return {'project': 'gdpr_permissions', 'users': users_list}