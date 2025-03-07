import traceback

from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _

from rest_framework import viewsets, status
from rest_framework import pagination

from core.helpers.errors import errorToString
from core.helpers.utils import debugObj
from core.logging import getDebugLogger

from tales_django.core.helpers.check_csrf import check_csrf
from tales_django.core.model_helpers import get_currrent_django_language

from .tag_serializers import TagSerializer

from ..models import Tag, Rubric, Author

logger = getDebugLogger()


defaultTagsLimit = 5
defaultTagsOffset = 0

content_type = 'application/json; charset=utf-8'
default_headers = {
    # 'Content-Type': content_type,
}


class DefaultPagination(pagination.LimitOffsetPagination):
    default_limit = defaultTagsLimit


# NOTE: No `viewsets.ModelViewSet` -- we don't use modification methods, only our custom `retrieve` and `list` (see below)
class TagViewSet(viewsets.GenericViewSet):
    language = get_currrent_django_language()
    queryset = Tag.objects.order_by(f'text_{language}').all()
    serializer_class = TagSerializer
    pagination_class = DefaultPagination

    def retrieve(self, request, *args, **kwargs):
        """
        Overrided single tag retrieve method
        """

        # Check session or csrf
        if not check_csrf(request):
            errorDetail = {'detail': _('Client session not found')}
            return JsonResponse(
                errorDetail, headers=default_headers, content_type=content_type, status=status.HTTP_403_FORBIDDEN
            )

        instance = self.get_object()
        serializer = TagSerializer(instance=instance)
        result = serializer.data
        return JsonResponse(result, headers=default_headers, content_type=content_type)

    def list(self, request):
        """
        Overrided authors list retrieve method
        """

        try:
            # Check session or csrf
            if not check_csrf(request):
                errorDetail = {'detail': _('Client session not found')}
                return JsonResponse(
                    errorDetail, headers=default_headers, content_type=content_type, status=status.HTTP_403_FORBIDDEN
                )

            limit = int(request.query_params.get('limit', defaultTagsLimit))
            offset = int(request.query_params.get('offset', defaultTagsOffset))

            # TODO: Extract sort/filter params and modify results below?

            language = get_currrent_django_language()
            query = Tag.objects.order_by(f'text_{language}')
            subset = query.all()
            if offset or limit:
                subset = query.all()[offset : offset + limit]

            result = {
                'count': len(query),
                'results': TagSerializer(subset, many=True).data,
            }

            return JsonResponse(result, headers=default_headers, content_type=content_type)
        except Exception as err:
            sError = errorToString(err)
            sTraceback = str(traceback.format_exc())
            debugData = {
                'err': err,
                'traceback': sTraceback,
            }
            logger.error(f'Caught error {sError} (returning in response):\n{debugObj(debugData)}')
            errorDetail = {'detail': sError}
            return JsonResponse(
                errorDetail,
                headers=default_headers,
                content_type=content_type,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
