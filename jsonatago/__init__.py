from .jsonatago import Jsonata

__all__ = ["Jsonata"]

# Delete the reference to the golib_jsonatago
del jsonatago_capi  # type: ignore
del jsonatago  # type: ignore
