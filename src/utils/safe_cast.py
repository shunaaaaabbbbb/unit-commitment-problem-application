from typing import Any, TypeVar, cast

T = TypeVar("T")


def ensure_type(value: Any, target_type: type[T]) -> T:
    """
    値を指定した型に変換して返す。
    - 変換できない場合は ValueError / TypeError を投げる
    - None は常にエラー
    """
    if value is None:
        raise ValueError(f"Cannot convert None to {target_type.__name__}")
    try:
        return cast(T, target_type(value))  # type: ignore
    except (ValueError, TypeError) as e:
        raise ValueError(f"Cannot convert {value!r} to {target_type.__name__}") from e
