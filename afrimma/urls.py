from django.conf.urls import url
from django.urls import path, re_path ,include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('',views.home,name = 'home'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/',views.edit_profile,name='edit'),
    path('new/', views.upload, name='upload'),
    path('project/<project_id>',views.project,name='project'),
    path('search/', views.search,name='search'),
    path('account/', include('django.contrib.auth.urls')),
    path('logout',views.home,{'next_page': 'accounts/login'}, name='logout'),
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)