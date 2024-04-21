from datetime import timedelta
import typing as t


BrowserTypeT = t.Literal['chromium', 'firefox', 'webkit']
SecondsT = t.Union[float, timedelta]


T = t.TypeVar('T')

Generator = t.Generator[T, None, None]
AsyncGenerator = t.AsyncGenerator[T, None]

GeneratorContextManager = t.Callable[..., t.ContextManager[T]]
AsyncGeneratorContextManager = t.Callable[..., t.AsyncContextManager[T]]

GeneratorContextManagerGenerator = t.ContextManager[Generator[T]]
AsyncGeneratorContextManagerAsyncGenerator = t.AsyncContextManager[AsyncGenerator[T]]
