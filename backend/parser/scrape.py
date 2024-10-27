import asyncio
import logging
import urllib.parse
from typing import AsyncGenerator, Optional, Tuple, Union

from aiohttp import ClientSession, TCPConnector, ClientTimeout, ClientResponseError, ClientConnectionError
from fake_useragent import UserAgent
from loguru import logger
from tenacity import retry_if_exception_type, retry, wait_exponential, stop_after_delay, before_sleep_log

from config import backend_config


semaphore = asyncio.Semaphore(backend_config.parsing.concurrent_requests)


@retry(
    retry=retry_if_exception_type((ClientConnectionError, asyncio.TimeoutError)),
    wait=wait_exponential(multiplier=1, min=2, max=backend_config.parsing.retry_delay),
    stop=stop_after_delay(backend_config.parsing.retry_attempts),
    before_sleep=before_sleep_log(logger, logging.WARNING)
)
async def scrape_target_url(
        url: str,
        context: Optional[dict] = None,
        as_json: bool = False
) -> Union[Tuple[Optional[Union[dict, str]], Optional[dict]], Optional[Union[dict, str]]]:
    """
    Асинхронная функция для получения содержимого страницы по URL.

    Параметры:
    - url (str): URL страницы для скрапинга.
    - context (Optional[dict]): Дополнительный контекст для возвращения с результатом (по умолчанию None).
    - as_json (bool): Если True, возвращает ответ в формате JSON, иначе в виде текста (по умолчанию False).

    Возвращает:
    - Если передан контекст, возвращает кортеж (содержимое страницы, контекст).
      Если контекст не передан, возвращает только содержимое страницы.
    - Если произошла ошибка, возвращает (None, None) или None в зависимости от наличия контекста.
    """
    async with semaphore:
        async with ClientSession(
                connector=TCPConnector(ssl=False, limit=backend_config.parsing.concurrent_requests),
                headers={"User-Agent": UserAgent().chrome},
                cookies={"schedule-group-cache": "2.0"},
                timeout=ClientTimeout(total=backend_config.parsing.retry_delay)
        ) as session:
            try:
                response = await session.get(url)
                response.raise_for_status()
            except (ClientResponseError, ClientConnectionError, asyncio.TimeoutError) as exception:
                logger.error(f"Ошибка запроса: '{url}' ({exception})")
                raise  # Повторно возбуждаем исключение для обработки ретраев

            try:
                if as_json:
                    content = await response.json()
                else:
                    content = await response.text()
            except Exception as e:
                logger.error(f"Ошибка обработки ответа: {e}")
                return (None, None) if context else None

            return (content, context) if context else content


async def scrape_target_urls(
        urls_with_context: list[Tuple[str, Optional[dict]]],
        as_json: bool = False
) -> AsyncGenerator[Union[Tuple[Optional[Union[dict, str]], Optional[dict]], Optional[Union[dict, str]]], None]:
    """
    Асинхронная функция для параллельного скрапинга списка URL с контекстом.

    Параметры:
    - urls_with_context (list[Tuple[str, Optional[dict]]]): Список URL и связанных с ними контекстов.
    - as_json (bool): Если True, возвращает ответ в формате JSON, иначе в виде текста (по умолчанию False).

    Возвращает:
    - Асинхронный генератор, который возвращает содержимое страницы с контекстом или без.
    """
    tasks = []
    for url, context in urls_with_context:
        tasks.append(scrape_target_url(url, context, as_json))

    for task in asyncio.as_completed(tasks):
        result = await task
        yield result


def url_with_parameters(url: str, **kwargs) -> str:
    """
    Функция для добавления параметров к URL в виде query-строки.

    Параметры:
    - url (str): Базовый URL.
    - kwargs: Параметры, которые нужно добавить к URL.

    Возвращает:
    - str: URL с добавленными параметрами.
    """
    return f"{url}{'?' if kwargs else ''}{urllib.parse.urlencode(kwargs)}"
