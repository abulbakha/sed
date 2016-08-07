from django.conf.urls import url, include
# our views
from django.utils.functional import curry
from django.views.defaults import permission_denied
from website.view.execution import CreateExecutionView, DeleteExecutionView
from website.view.user import CreateUserView, DeleteUserView, ListUserView, UpdateUserView, ContactUserView
from website.view.department import CreateDepartmentView, DeleteDepartmentView, ListDepartmentView, UpdateDepartmentView
from website.view.unit import CreateUnitView, DeleteUnitView, ListUnitView, UpdateUnitView
from website.view.post import CreatePostView, DeletePostView, ListPostView, UpdatePostView
from website.view.role import CreateRoleView, DeleteRoleView, ListRoleView, UpdateRoleView
from website.view.file import CreateFileView, DeleteFileView, DownloadFileView
from website.view.document import CreateDocumentView, DeleteDocumentView, ListDocumentView, UpdateDocumentView
from website.view.resolution import CreateResolutionView, DeleteResolutionView, UpdateResolutionView
from website.view.meeting import CreateMeetingView, DeleteMeetingView, ListMeetingView, UpdateMeetingView
from website.view.notification import ListNotificationView, CheckNotificationView
from website.view.home import HomeView
from website.view.account import UserLogin, UserLogout
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from website.view.room import CreateRoomView , DeleteRoomView, ListRoomView, UpdateRoomView

handler403 = curry(permission_denied, template_name='account/logout.html')

urlpatterns = [

    # login/logout etc.
    url(r'^account/login/$', UserLogin, name='login'),
    url(r'^account/logout/$', UserLogout, name='logout'),

    # actions with users
    url(r'^user/list/$', ListUserView.as_view(), name='user-list'),
    url(r'^user/new/$', CreateUserView.as_view(), name='user-new', ),
    url(r'^user/edit/(?P<pk>\d+)/$', UpdateUserView.as_view(), name='user-edit', ),
    url(r'^user/delete/(?P<pk>\d+)/$', DeleteUserView.as_view(), name='user-delete', ),
    url(r'^user/contact/(?P<pk>\d+)/$', ContactUserView.as_view(), name='user-contact', ),

    # actions with departments
    url(r'^department/list/$', ListDepartmentView.as_view(), name='department-list'),
    url(r'^department/new/$', CreateDepartmentView.as_view(), name='department-new', ),
    url(r'^department/edit/(?P<pk>\d+)/$', UpdateDepartmentView.as_view(), name='department-edit', ),
    url(r'^department/delete/(?P<pk>\d+)/$', DeleteDepartmentView.as_view(), name='department-delete', ),

    # actions with units
    url(r'^unit/list/$', ListUnitView.as_view(), name='unit-list'),
    url(r'^unit/new/$', CreateUnitView.as_view(), name='unit-new', ),
    url(r'^unit/edit/(?P<pk>\d+)/$', UpdateUnitView.as_view(), name='unit-edit', ),
    url(r'^unit/delete/(?P<pk>\d+)/$', DeleteUnitView.as_view(), name='unit-delete', ),

    # actions with posts
    url(r'^post/list/$', ListPostView.as_view(), name='post-list'),
    url(r'^post/new/$', CreatePostView.as_view(), name='post-new', ),
    url(r'^post/edit/(?P<pk>\d+)/$', UpdatePostView.as_view(), name='post-edit', ),
    url(r'^post/delete/(?P<pk>\d+)/$', DeletePostView.as_view(), name='post-delete', ),

    # actions with roles
    url(r'^role/list/$', ListRoleView.as_view(), name='role-list'),
    url(r'^role/new/$', CreateRoleView.as_view(), name='role-new', ),
    url(r'^role/edit/(?P<pk>\d+)/$', UpdateRoleView.as_view(), name='role-edit', ),
    url(r'^role/delete/(?P<pk>\d+)/$', DeleteRoleView.as_view(), name='role-delete', ),

    # actions with documents
    url(r'^document/list/$', ListDocumentView.as_view(), name='document-list'),
    url(r'^document/new/$', CreateDocumentView.as_view(), name='document-new', ),
    url(r'^document/edit/(?P<pk>\d+)/$', UpdateDocumentView.as_view(), name='document-edit', ),
    url(r'^document/delete/(?P<pk>\d+)/$', DeleteDocumentView.as_view(), name='document-delete', ),
    # actions with files
    url(r'^document/(?P<doc_id>\d+)/file/new/$', CreateFileView.as_view(), name='file-new', ),
    url(r'^document/(?P<doc_id>\d+)/file/delete/(?P<pk>\d+)/$', DeleteFileView.as_view(),
        name='file-delete', ),
    url(r'^document/(?P<doc_id>\d+)/file/download/(?P<pk>\d+)/$', DownloadFileView.as_view(),
        name='file-download', ),
    # actions with resolution
    url(r'^document/(?P<doc_id>\d+)/resolution/new/$', CreateResolutionView.as_view(), name='resolution-new', ),
    url(r'^resolution/edit/(?P<pk>\d+)/$', UpdateResolutionView.as_view(), name='resolution-edit', ),
    url(r'^document/(?P<doc_id>\d+)/resolution/delete/(?P<pk>\d+)/$', DeleteResolutionView.as_view(), name='resolution-delete', ),
    # actions with execution
    url(r'^document/(?P<doc_id>\d+)/execution/new/$', CreateExecutionView.as_view(), name='execution-new', ),
    url(r'^document/(?P<doc_id>\d+)/execution/delete/(?P<pk>\d+)/$', DeleteExecutionView.as_view(), name='execution-delete', ),

    # actions with meeting
    url(r'^meeting/list/$', ListMeetingView.as_view(), name='meeting-list'),
    url(r'^meeting/new/$', CreateMeetingView.as_view(), name='meeting-new', ),
    url(r'^meeting/edit/(?P<pk>\d+)/$', UpdateMeetingView.as_view(), name='meeting-edit', ),
    url(r'^meeting/delete/(?P<pk>\d+)/$', DeleteMeetingView.as_view(), name='meeting-delete', ),

    # actions with notification
    url(r'^notification/list/$', ListNotificationView.as_view(), name='notification-list'),
    url(r'^notification/check/(?P<pk>\d+)/$', CheckNotificationView.as_view(),
        name='notification-check', ),


    # actions with room
    url(r'^room/list/$', ListRoomView.as_view(), name='room-list'),
    url(r'^room/new/$', CreateRoomView.as_view(), name='room-new', ),
    url(r'^room/edit/(?P<pk>\d+)/$', UpdateRoomView.as_view(), name='room-edit', ),
    url(r'^room/delete/(?P<pk>\d+)/$', DeleteRoomView.as_view(), name='room-delete', ),

    url(r'', HomeView.as_view()),
    url(r'^#', HomeView.as_view(), name='home'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

