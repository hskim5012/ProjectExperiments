from django.urls import path
from . import views

from django.urls import path, include
import oauth2_provider.views as oauth2_views
from django.conf import settings
from .views import ApiEndpoint

# OAuth2 provider endpoints
oauth2_endpoint_views = [
    path('authorize/', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    path('token/', oauth2_views.TokenView.as_view(), name="token"),
    path('revoke-token/', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

if settings.DEBUG:
    # OAuth2 Application Management endpoints
    oauth2_endpoint_views += [
        path('applications/', oauth2_views.ApplicationList.as_view(), name="list"),
        path('applications/register/', oauth2_views.ApplicationRegistration.as_view(), name="register"),
        path('applications/(?P<pk>\d+)/', oauth2_views.ApplicationDetail.as_view(), name="detail"),
        path('applications/(?P<pk>\d+)/delete/', oauth2_views.ApplicationDelete.as_view(), name="delete"),
        path('applications/(?P<pk>\d+)/update/', oauth2_views.ApplicationUpdate.as_view(), name="update"),
    ]

    # OAuth2 Token Management endpoints
    oauth2_endpoint_views += [
        path('authorized-tokens/', oauth2_views.AuthorizedTokensListView.as_view(), name="authorized-token-list"),
        path('authorized-tokens/(?P<pk>\d+)/delete/', oauth2_views.AuthorizedTokenDeleteView.as_view(),
            name="authorized-token-delete"),
    ]


urlpatterns = [
    path('', views.index),
    ##takes user to login and registraton page

    path('dashboard', views.dashboard),
    ##takes user to the dashboard "the home"

    path('login', views.login),
    ##processes the login(email+pw) to get to the dashboard

    path('registrationprocess', views.registrationprocess, name="registration"),
    #registeration processing with entered information

    path('logout', views.logout),
    #clears out session for logged in user

    path('api/hello', ApiEndpoint.as_view()),
    path('secret', views.secret_page, name='secret'),

]
