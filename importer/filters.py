import filters as f


@f.filter_macro
def NonEmptyString():
    return f.Unicode | f.Strip | f.Required
