from django.urls import include, path

# from ..views import api_application

api_urlpatterns = [
    # @see https://www.django-rest-framework.org/
    path('api-auth/', include('rest_framework.urls')),
    # path(
    #     'api/apply',
    #     api_application,
    #     name='api_application',
    # ),
]
