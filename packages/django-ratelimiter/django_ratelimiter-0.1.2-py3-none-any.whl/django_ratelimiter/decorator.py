from typing import Callable, Literal, Sequence, Union, Optional
from functools import wraps, partial

from django.db import models
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from limits.strategies import STRATEGIES, RateLimiter
from limits.storage import Storage
from limits import parse
from django_ratelimiter.storage import CacheStorage
from django_ratelimiter.types import ViewFunc, P


def build_identifiers(
    func: ViewFunc, methods: Union[str, Sequence[str], None] = None
) -> list[str]:
    """Build view identifiers for storage cache key using function signature and list of methods."""
    if isinstance(func, partial):
        # method_decorator scenario
        identifiers = [
            func.func.__self__.__class__.__module__,
            f"{func.func.__self__.__class__.__qualname__}.{func.func.__name__}",
        ]
    else:
        identifiers = [func.__module__, func.__qualname__]
    if methods:
        methods_ = methods if isinstance(methods, str) else "|".join(sorted(methods))
        identifiers.append(methods_)
    return identifiers


def get_storage() -> Storage:
    """Returns a default storage backend instance, defined by either `DJANGO_RATELIMITER_CACHE`
    or `DJANGO_RATELIMITER_STORAGE`."""
    cache_name: Optional[str] = getattr(settings, "DJANGO_RATELIMITER_CACHE", None)
    storage: Optional[Storage] = getattr(settings, "DJANGO_RATELIMITER_STORAGE", None)
    if cache_name and storage:
        raise ValueError(
            "DJANGO_RATELIMITER_CACHE and DJANGO_RATELIMITER_STORAGE can't be used together"
        )
    return storage or CacheStorage(cache_name or "default")


def get_rate_limiter(strategy: str, storage: Optional[Storage] = None) -> RateLimiter:
    """Return a ratelimiter instance for given strategy."""
    if strategy not in STRATEGIES:
        raise ValueError(
            f"Unknown strategy {strategy}, must be one of {STRATEGIES.keys()}"
        )
    storage = storage or get_storage()
    return STRATEGIES[strategy](storage)


def ratelimit(
    rate: Union[str, Callable[[HttpRequest], str]],
    key: Union[str, Callable[[HttpRequest], str], None] = None,
    methods: Union[str, Sequence[str], None] = None,
    strategy: Literal[
        "fixed-window",
        "fixed-window-elastic-expiry",
        "moving-window",
    ] = "fixed-window",
    response: Optional[HttpResponse] = None,
    storage: Optional[Storage] = None,
    cache: Optional[str] = None,
) -> Callable[[ViewFunc], ViewFunc]:
    """Rate limiting decorator for wrapping views.

    Arguments:
        rate: rate string (i.e. `5/second`) or a callable that takes a request and returns a rate
        key: request attribute or callable that returns a string to be used as identifier
        methods: only rate limit specified method(s)
        strategy: a name of rate limiting strategy
        response: custom rate limit response instance
        storage: override default rate limit storage
        cache: override default cache name if using django cache storage backend
    """
    if storage and cache:
        raise ValueError("Can't use both cache and storage")
    rate_limiter = get_rate_limiter(strategy, storage)

    def decorator(func: ViewFunc) -> ViewFunc:
        @wraps(func)
        def wrapper(
            request: HttpRequest, *args: P.args, **kwargs: P.kwargs
        ) -> HttpResponse:
            rate_str = rate(request) if callable(rate) else rate
            parsed_rate = parse(rate_str)
            if getattr(settings, "DJANGO_RATELIMITER_CACHE", True) and (
                not methods or request.method in methods
            ):
                identifiers = build_identifiers(func, methods)

                if key:
                    value = key(request) if callable(key) else getattr(request, key)
                    value = str(value.pk if isinstance(value, models.Model) else value)
                    identifiers.append(value)

                if not rate_limiter.hit(parsed_rate, *identifiers):
                    return response or HttpResponse(
                        "Too Many Requests",
                        status=429,
                    )
            return func(request, *args, **kwargs)

        return wrapper

    return decorator
