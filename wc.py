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

@coroutine
def grep(pattern, casesensitive, child):
    if not casesensitive:
        pattern = pattern.lower()

    while True:
        text = (yield)
        child.send(text.count(pattern))

@coroutine
def count(pattern):
    n = 0
    try:
        while True:
            n += (yield)

    except GeneratorExit:
        print(pattern, n)




if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', action='store_true', dest='casesensitive')
    parser.add_argument("pattern", type=str)
    parser.add_argument("infile", type=argparse.FileType('r'))

    args = parser.parse_args()


    cat(args.infile, args.casesensitive, grep(args.pattern, args.casesensitive, count(args.pattern)))

