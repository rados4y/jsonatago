from .jsonatago import Jsonata, jeval

__all__ = ["Jsonata", "jeval"]

# Delete the reference to the golib_jsonatago
del jsonatago_capi  # type: ignore
del jsonatago  # type: ignore
