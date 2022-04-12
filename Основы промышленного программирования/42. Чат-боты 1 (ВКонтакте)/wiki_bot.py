import logging
import os
import random

import requests
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

TOKEN = os.getenv("TOKEN")
CLUB_ID = os.getenv("CLUB_ID")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

datastore = {}  # user_id: 1/0 (новое сообщение или нет)


class WikiNotFound(Exception):
    ...


class WikiSuggestionOnly(Exception):
    ...


class WikiPageInfo:

    def __init__(self, pageid, title, suggestion, url):
        self.pageid = pageid
        self.title = title
        self.suggestion = suggestion
        self.url = url


class WikiSummary:

    def __init__(self, text_summary, url, is_suggested=False):
        self.summary = text_summary
        self.url = url
        self.is_suggested = is_suggested


def _wiki_request(params):
    API_URL = 'http://ru.wikipedia.org/w/api.php'
    USER_AGENT = "wikipedia (https://github.com/goldsmith/Wikipedia/)"

    params['format'] = 'json'
    if 'action' not in params:
        params['action'] = 'query'

    headers = {
        'User-Agent': USER_AGENT
    }

    r = requests.get(API_URL, params=params, headers=headers)

    return r.json()


def search(query, results=10, suggestion=False):
    search_params = {
        'list': 'search',
        'srprop': '',
        'srlimit': results,
        'limit': results,
        'srsearch': query
    }

    if suggestion:
        search_params['srinfo'] = 'suggestion'

    raw_results = _wiki_request(search_params)

    if 'error' in raw_results:
        if raw_results['error']['info'] in ('HTTP request timed out.', 'Pool queue is full'):
            raise requests.exceptions.Timeout(query)
        else:
            raise requests.HTTPError(raw_results['error']['info'])

    search_results = (d['title'] for d in raw_results['query']['search'])

    if suggestion:
        if raw_results['query'].get('searchinfo'):
            return list(search_results), raw_results['query']['searchinfo']['suggestion']
        else:
            return list(search_results), None

    return list(search_results)


def get_wiki_page(title, suggestion=False):
    query_params = {'prop': 'info|pageprops', 'inprop': 'url', 'ppprop': 'disambiguation',
                    'redirects': '', 'titles': title}
    request = _wiki_request(query_params)

    query = request['query']
    pageid = list(query['pages'].keys())[0]
    wiki_page = query['pages'][pageid]
    if "missing" in wiki_page:
        raise WikiNotFound(wiki_page["title"])
    url = wiki_page["fullurl"]
    return WikiPageInfo(**{"pageid": pageid, "title": wiki_page["title"],
                           "suggestion": suggestion, "url": url})


def page(title=None, auto_suggest=True):
    if title is not None:
        if auto_suggest:
            results, suggestion = search(title, results=1, suggestion=True)
            try:
                title = suggestion or results[0]
            except IndexError:
                # if there is no suggestion or search results, the page doesn't exist
                raise WikiNotFound(title)
            if title != suggestion:
                auto_suggest = False
        return get_wiki_page(title, suggestion=auto_suggest)
    else:
        raise ValueError("Either a title or a pageid must be specified")


def summary(title, sentences=0, chars=0, auto_suggest=True):
    page_info = page(title, auto_suggest=auto_suggest)
    title = page_info.title
    pageid = page_info.pageid

    query_params = {
        'prop': 'extracts',
        'explaintext': '',
        'titles': title
    }

    if sentences:
        query_params['exsentences'] = sentences
    elif chars:
        query_params['exchars'] = chars
    else:
        query_params['exintro'] = ''

    request = _wiki_request(query_params)
    wiki_summary = request['query']['pages'][pageid]['extract']

    wiki_summary = WikiSummary(wiki_summary, page_info.url, page_info.suggestion)

    return wiki_summary


def handle_message(vk, event):
    logger.info(event)
    logger.info('Новое сообщение:')
    user_id = event.obj.message['from_id']
    logger.info('Для меня от: %s', user_id)
    text = event.obj.message['text']
    logger.info('Текст: %s', text)
    if not datastore.get(user_id):
        datastore[user_id] = 1
        msg = "Введите понятие, и я найду его объяснение."
    else:
        try:
            wiki_summary = summary(text)
        except WikiNotFound:
            msg = "Ничего не найдено, поробуйте еще раз"
            logger.error("not found")
        except requests.HTTPError:
            msg = "Ошибка сервера wikipedia, попробуйте позже"
            logger.error("wikipedia error")
        except Exception as e:
            msg = f"Ошибка бота: {e}"
            logger.error(e)
        else:
            logger.info("found info")
            msg = f"{wiki_summary.url}\n{wiki_summary.summary}"
            if wiki_summary.is_suggested:
                msg = f"Найдено похожее:\n\n{msg}"
    vk.messages.send(user_id=user_id,
                     message=msg,
                     random_id=random.randint(0, 2 ** 64))


def main():
    vk_session = vk_api.VkApi(
        token=TOKEN)

    longpoll = VkBotLongPoll(vk_session, CLUB_ID)
    vk = vk_session.get_api()

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            handle_message(vk, event)


if __name__ == '__main__':
    main()
