from django.http import HttpRequest
from django.utils import translation

from core.logging import getDebugLogger

from tales_django.models import Author


authors_limit= 20

logger = getDebugLogger()


def get_authors_list_context(request: HttpRequest):

    language = translation.get_language()

    # Will produce params:
    # 1. For data display (eg, for `src/assets/common-blocks/big-authors-list/big-authors-list.django`):
    # - authors
    # 2. For pagination (`src/assets/template-columns/pagination.django`):
    # - authors_count
    # - authors_offset
    # - authors_limit
    # Regex:
    # \<\(authors\|authors_count\|authors_offset\|authors_limit\)\>

    authors_offset = int(request.GET.get('authors_offset', 0))

    authors = Author.objects.order_by(f'name_{language}').all()

    authors_end = authors_offset + authors_limit
    authors_set = authors[authors_offset:authors_end]
    authors_count = len(authors)
    # has_prev_authors = authors_offset > 0
    # has_next_authors = authors_count > authors_end
    # authors_page_no = math.floor(authors_offset / authors_limit) + 1
    # authors_pages_count = math.ceil(authors_count / authors_limit)

    # debugData = {
    #     'language': language,
    #     'authors_offset': authors_offset,
    #     'authors_set': authors_set,
    # }
    # debugStr = debugObj(debugData)
    # logger.info(f'get_authors_list_context\n{debugStr}')

    context = {
        # Tracks...
        'authors': authors_set,
        'authors_count': authors_count,
        'authors_offset': authors_offset,
        'authors_limit': authors_limit,
        # 'has_prev_authors': has_prev_authors,
        # 'has_next_authors': has_next_authors,
        # 'authors_page_no': authors_page_no,
        # 'authors_pages_count': authors_pages_count,
    }
    return context
