_enabled = True


def en_print():
    global _enabled
    _enabled = True


def dis_print():
    global _enabled
    _enabled = False


def zprint(*args, **kwargs):
    if _enabled:
        print(*args, **kwargs)


def zdebug(*args, **kwargs):
    print(*args, **kwargs)
