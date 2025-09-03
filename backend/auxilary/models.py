from typing import Any, Optional


class SingletonMetaclass(type):
    _instance: Optional[Any] = None

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if not cls._instance:
            cls._instance = super().__call__(*args, **kwds)
            return cls._instance
        raise RuntimeError("Attempt to re-instantiate singleton instance")