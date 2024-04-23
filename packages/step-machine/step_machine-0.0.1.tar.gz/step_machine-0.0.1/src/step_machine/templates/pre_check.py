import sys


def run():
    print('Checking environment for necessary dependencies')
    ok = True
    if ok:
        sys.exit(0)
    else:
        # Any non-zero exit code will stop all following script from running.
        sys.exit(10)


if __name__ == '__main__':
    run()
