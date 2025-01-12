from django.urls import path, include

from ..api import track_api_router

# from ..views import track_application

track_urlpatterns = [
    # path(
    #     'track/apply',
    #     track_application,
    #     name='track_application',
    # ),
    path(r'api/', include(track_api_router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
