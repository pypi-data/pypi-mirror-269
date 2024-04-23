import sys


def run():
    print('Validating setup.')
    ok = True
    if ok:
        sys.exit(0)
    else:
        # Any non-zero exit code will create an error status.
        sys.exit(10)


if __name__ == '__main__':
    run()
