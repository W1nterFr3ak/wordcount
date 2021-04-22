import argparse

def coroutine(fn):
    def wrapper(*args, **kwargs):
        c = fn(*args, **kwargs)
        next(c)
        return c
    return wrapper


def cat (f, casesensitive, child):
    if casesensitive:
        process = lambda k: k
    else:
        process = lambda k: k.lower()

    for l in f:
        child.send(process(l))


def grep(pattern, casesensitive, child):
    if not casesensitive:
        pattern = pattern.lower()

    while True:
        text = (yield)
        child.send(text.count(pattern))


