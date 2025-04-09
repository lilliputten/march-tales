from django.http import HttpRequest
from django.utils import translation

from core.logging import getDebugLogger
from tales_django.models import Tag

tags_limit = 20

logger = getDebugLogger()


def get_tags_list_context(request: HttpRequest):

    language = translation.get_language()

    # Will produce params:
    # 1. For data display (eg, for `src/assets/common-blocks/big-tags-list/big-tags-list.django`):
    # - tags
    # 2. For pagination (`src/assets/template-columns/pagination.django`):
    # - tags_count
    # - tags_offset
    # - tags_limit
    # Regex:
    # \<\(tags\|tags_count\|tags_offset\|tags_limit\)\>

    tags_offset = int(request.GET.get('tags_offset', 0))

    tags = Tag.objects.order_by(f'text_{language}').all()

    tags_end = tags_offset + tags_limit
    tags_set = tags[tags_offset:tags_end]
    tags_count = len(tags)
    # has_prev_tags = tags_offset > 0
    # has_next_tags = tags_count > tags_end
    # tags_page_no = math.floor(tags_offset / tags_limit) + 1
    # tags_pages_count = math.ceil(tags_count / tags_limit)

    # debugData = {
    #     'language': language,
    #     'tags_offset': tags_offset,
    #     'tags_set': tags_set,
    # }
    # debugStr = debugObj(debugData)
    # logger.info(f'get_tags_list_context\n{debugStr}')

    context = {
        # Tracks...
        'tags': tags_set,
        'tags_count': tags_count,
        'tags_offset': tags_offset,
        'tags_limit': tags_limit,
        # 'has_prev_tags': has_prev_tags,
        # 'has_next_tags': has_next_tags,
        # 'tags_page_no': tags_page_no,
        # 'tags_pages_count': tags_pages_count,
    }
    return context
