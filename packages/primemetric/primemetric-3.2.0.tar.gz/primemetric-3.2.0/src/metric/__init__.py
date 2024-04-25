import argparse
from src.metric.metric import get_metric


def main():
    """Entry point for the application script"""
    print("Call your main application code here")

    parser = argparse.ArgumentParser(
        prog='📐 Metric',
        description='📐 Metric',
        add_help=True
    )

    parser.add_argument('x', help='First Value')
    parser.add_argument('y', help='Second Value')

    args = parser.parse_args()

    out_metric = get_metric(args.x, args.y)
    print(out_metric)