from headlesspreview.models import PagePreview


def review_url_builder(token):
    page = token.page_revision.page.specific

    page_preview = page.create_page_preview()
    page_preview.save()
    PagePreview.garbage_collect()

    url = page.get_preview_url(page_preview.token) + '&review_token=' + token.encode()

    if token.review_request_id is not None:
        url += '&allow_responses=true'

    return url
