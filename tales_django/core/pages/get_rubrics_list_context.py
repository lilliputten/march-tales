from django.http import HttpRequest
from django.utils import translation
from django.db.models import Count

from core.logging import getDebugLogger

from tales_django.models import Rubric


rubrics_limit = 20

logger = getDebugLogger()


def get_rubrics_list_context(request: HttpRequest):

    language = translation.get_language()

    # Will produce params:
    # 1. For data display (eg, for `src/assets/common-blocks/big-rubrics-list/big-rubrics-list.django`):
    # - rubrics
    # 2. For pagination (`src/assets/template-columns/pagination.django`):
    # - rubrics_count
    # - rubrics_offset
    # - rubrics_limit
    # Regex:
    # \<\(rubrics\|rubrics_count\|rubrics_offset\|rubrics_limit\)\>

    rubrics_offset = int(request.GET.get('rubrics_offset', 0))

    # rubrics = Rubric.objects.order_by(f'text_{language}').all()
    rubrics = (
        Rubric.objects.annotate(t_count=Count('tracks'))
        .filter(t_count__gt=0)
        .order_by('-t_count', f'text_{language}')
        .all()
    )

    rubrics_end = rubrics_offset + rubrics_limit
    rubrics_set = rubrics[rubrics_offset:rubrics_end]
    rubrics_count = len(rubrics)
    # has_prev_rubrics = rubrics_offset > 0
    # has_next_rubrics = rubrics_count > rubrics_end
    # rubrics_page_no = math.floor(rubrics_offset / rubrics_limit) + 1
    # rubrics_pages_count = math.ceil(rubrics_count / rubrics_limit)

    # debugData = {
    #     'language': language,
    #     'rubrics_offset': rubrics_offset,
    #     'rubrics_set': rubrics_set,
    # }
    # debugStr = debugObj(debugData)
    # logger.info(f'get_rubrics_list_context\n{debugStr}')

    context = {
        # Tracks...
        'rubrics': rubrics_set,
        'rubrics_count': rubrics_count,
        'rubrics_offset': rubrics_offset,
        'rubrics_limit': rubrics_limit,
        # 'has_prev_rubrics': has_prev_rubrics,
        # 'has_next_rubrics': has_next_rubrics,
        # 'rubrics_page_no': rubrics_page_no,
        # 'rubrics_pages_count': rubrics_pages_count,
    }
    return context
