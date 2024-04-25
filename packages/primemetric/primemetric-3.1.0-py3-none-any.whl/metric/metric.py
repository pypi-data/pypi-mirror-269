import argparse
import math


def get_metric(x, y):
    return math.sqrt(x*x + y*y)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='📐 Metric',
        description='📐 Metric',
        add_help=True
    )

    parser.add_argument('x', help='First Value')
    parser.add_argument('y', help='Second Value')

    args = parser.parse_args()
    get_metric(args.x, args.y)
