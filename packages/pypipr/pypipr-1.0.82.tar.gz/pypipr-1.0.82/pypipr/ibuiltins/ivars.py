import inspect


def ivars(obj):
    """
    Membuat dictionary berdasarkan kategori untuk setiap
    member dari object.

    ```python
    iprint(ivars(__import__('pypipr')))
    ```
    """
    result = {
        "module": {},
        "class": {},
        "function": {},
        "property": {},
        "variable": {},
        "method": {},
        "__module__": {},
        "__class__": {},
        "__function__": {},
        "__property__": {},
        "__variable__": {},
        "__method__": {},
    }
    uu = lambda x: "__" if x.startswith("__") or x.endswith("__") else ""
    for i, v in vars(obj).items():
        u = uu(i)
        if inspect.ismodule(v):
            result[f"{u}module{u}"][i] = v
        elif inspect.isclass(v):
            result[f"{u}class{u}"][i] = v
        elif inspect.ismethod(v):
            result[f"{u}method{u}"][i] = v
        elif inspect.isfunction(v):
            result[f"{u}function{u}"][i] = v
        else:
            if isinstance(v, property):
                result[f"{u}property{u}"][i] = v
            else:
                result[f"{u}variable{u}"][i] = v
    return result
