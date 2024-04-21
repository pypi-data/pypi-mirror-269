import pytest


@pytest.fixture(params=['chromium', 'firefox', 'webkit'])
def browser_type(request):
    return request.param
