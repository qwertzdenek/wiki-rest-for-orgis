from lxml.html import document_fromstring
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.routing import Route
from httpx import codes, get, ConnectError

from .auth import WikiAuthenticator


API_ENDPOINT = 'https://api.wikimedia.org/core/v1/wikipedia'

auth = WikiAuthenticator()

def get_first_paragraph(wikihtml: str):
    dom_root = document_fromstring(wikihtml)
    for node in dom_root.xpath('//section[@data-mw-section-id=\'0\']/p'):
        node_text = node.text_content()
        if len(node_text.strip()) > 0:
            return node_text
    return None

def find_by_title(lang, term):
    """
    return content of the article with title
    """
    bearer = auth.token()
    headers = {}
    if bearer:
        headers['Authorization'] = f'Bearer {bearer}'
    try:
        r = get(f'{API_ENDPOINT}/{lang}/page/{term}/html',
                headers=headers,
                follow_redirects=True)
    except ConnectError:
        return None

    if r.status_code == codes.OK:
        return get_first_paragraph(r.text)
    return None

def find_by_content(lang, term):
    """
    return list of article titles containing the term
    """
    bearer = auth.token()
    headers = {}
    if bearer:
        headers['Authorization'] = f'Bearer {bearer}'
    try:
        r = get(f'{API_ENDPOINT}/{lang}/search/page',
                headers=headers,
                params={
                    'q': term,
                    'limit': 10
                },
                follow_redirects=True)
    except ConnectError:
        return None

    if r.status_code == codes.OK:
        return r.json()['pages']
    return None


async def get_term(request: Request):
    term = request.path_params['term']
    lang = request.headers['Accept-Language'] or 'en'

    title_content = find_by_title(lang, term)
    if title_content is not None:
        return JSONResponse({'result': title_content}, status_code=codes.OK)
    
    article_names = find_by_content(lang, term)
    if article_names is not None and len(article_names) > 0:
        return JSONResponse({'result': None, 'articles': [a['title'] for a in article_names]}, status_code=codes.SEE_OTHER)

    return JSONResponse({'result': None}, status_code=codes.NOT_FOUND)

wiki_route = Route('/wiki/{term}', get_term, methods=['GET'])
