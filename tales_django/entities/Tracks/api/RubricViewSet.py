import traceback

from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from rest_framework import pagination, status, viewsets

from core.helpers.errors import errorToString
from core.helpers.utils import debugObj
from core.logging import getDebugLogger
from tales_django.core.constants.common_constants import data_content_type, default_headers
from tales_django.core.helpers.check_csrf import check_csrf
from tales_django.core.model_helpers import get_current_language

from ..models import Rubric
from .rubric_serializers import RubricSerializer

logger = getDebugLogger()


defaultRubricsLimit = 5
defaultRubricsOffset = 0

# class DefaultPagination(pagination.LimitOffsetPagination):
#     default_limit = defaultRubricsLimit


# NOTE: No `viewsets.ModelViewSet` -- we don't use modification methods, only our custom `retrieve` and `list` (see below)
class RubricViewSet(viewsets.GenericViewSet):
    language = get_current_language()
    queryset = Rubric.objects.order_by(f'text_{language}').all()
    serializer_class = RubricSerializer
    # pagination_class = DefaultPagination

    def retrieve(self, request, *args, **kwargs):
        """
        Overrided single rubric retrieve method
        """

        # Check session or csrf
        if not check_csrf(request):
            errorDetail = {'detail': _('Client session not found')}
            return JsonResponse(
                errorDetail, headers=default_headers, content_type=data_content_type, status=status.HTTP_403_FORBIDDEN
            )

        instance = self.get_object()
        serializer = RubricSerializer(instance=instance)
        result = serializer.data
        return JsonResponse(result, headers=default_headers, content_type=data_content_type)

    def list(self, request):
        """
        Overrided authors list retrieve method
        """

        try:
            # Check session or csrf
            if not check_csrf(request):
                errorDetail = {'detail': _('Client session not found')}
                return JsonResponse(
                    errorDetail,
                    headers=default_headers,
                    content_type=data_content_type,
                    status=status.HTTP_403_FORBIDDEN,
                )

            limit = int(request.query_params.get('limit', defaultRubricsLimit))
            offset = int(request.query_params.get('offset', defaultRubricsOffset))

            # TODO: Extract sort/filter params and modify results below?

            language = get_current_language()
            query = Rubric.objects.order_by(f'text_{language}')
            subset = query.all()
            if offset or limit:
                subset = query.all()[offset : offset + limit]

            result = {
                'count': len(query),
                'results': RubricSerializer(subset, many=True).data,
            }

            return JsonResponse(result, headers=default_headers, content_type=data_content_type)
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
                content_type=data_content_type,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
