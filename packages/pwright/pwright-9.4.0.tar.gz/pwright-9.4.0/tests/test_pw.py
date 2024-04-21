from contextlib import contextmanager
import time

from pwright import pw
from pwright.typealiases import BrowserTypeT


def test_pw_page(browser_type):
    def get_title(*, url: str):
        with pw.pw_page(browser_type=browser_type) as page:
            page.goto(url)
            title = page.title()
            return title

    assert 'Playwright' in get_title(url='https://playwright.dev/')


def _test_renew(*, browser_type: BrowserTypeT = 'firefox', headed=True):
    @contextmanager
    def gen_page():
        with pw.pw_page(browser_type=browser_type, headed=headed) as page:
            yield page

    gen_page_cm: pw.GeneratorContextManager[pw.Page] = gen_page

    def run(*, page_gen: pw.Generator[pw.Page]):
        for _ in range(5):
            page = next(page_gen)
            page.goto('https://playwright.dev/')
            print(id(page))
            if 0:
                time.sleep(0.2)
        page_gen.close()
        if 0:
            time.sleep(30)

    auto_renew_page_gen: pw.Generator[pw.Page] = pw.auto_renew(gen_page_cm, 3)
    run(page_gen=auto_renew_page_gen)

    renewing: pw.GeneratorContextManagerGenerator[pw.Page] = pw.renewing(gen_page_cm, 3)
    with renewing as page_gen:
        run(page_gen=page_gen)


def test_renew(browser_type):
    _test_renew(browser_type=browser_type, headed=False)


if __name__ == '__main__':
    _test_renew()
