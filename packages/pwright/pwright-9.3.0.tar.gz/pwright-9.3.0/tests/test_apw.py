import asyncio
from contextlib import asynccontextmanager
import sys
import time

from pwright import apw as pw
from pwright.typealiases import BrowserTypeT


if sys.version_info < (3, 10):
    anext = pw.anext


def test_pw_page(browser_type):
    async def get_title(*, url: str):
        async with pw.pw_page(browser_type=browser_type) as page:
            await page.goto(url)
            title = await page.title()
            return title

    assert 'Playwright' in asyncio.run(get_title(url='https://playwright.dev/'))


async def _test_renew(*, browser_type: BrowserTypeT = 'firefox', headed=True):
    @asynccontextmanager
    async def gen_page():
        async with pw.pw_page(browser_type=browser_type, headed=headed) as page:
            yield page

    gen_page_cm: pw.AsyncGeneratorContextManager[pw.Page] = gen_page

    async def run(*, page_gen: pw.AsyncGenerator[pw.Page]):
        for _ in range(5):
            page = await anext(page_gen)
            await page.goto('https://playwright.dev/')
            print(id(page))
            if 0:
                time.sleep(0.2)
        await page_gen.aclose()
        if 0:
            await asyncio.sleep(30)

    auto_renew_page_gen: pw.AsyncGenerator[pw.Page] = pw.auto_renew(gen_page_cm, 3)
    await run(page_gen=auto_renew_page_gen)

    renewing: pw.AsyncGeneratorContextManagerAsyncGenerator[pw.Page] = pw.renewing(gen_page_cm, 3)
    async with renewing as agen:
        await run(page_gen=agen)


def test_renew(browser_type):
    asyncio.run(_test_renew(browser_type=browser_type, headed=False))


if __name__ == '__main__':
    asyncio.run(_test_renew())
