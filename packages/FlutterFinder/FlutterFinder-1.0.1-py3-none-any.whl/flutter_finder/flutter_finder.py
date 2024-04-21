import argparse

from .utils import find_flutter_apps, output_to_file, print_flutter_apps

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Find Flutter apps in a directory')
    parser.add_argument('root_dir', help='Root directory to search for Flutter apps')
    parser.add_argument('-o', '--output', help='Output file for the results')
    args = parser.parse_args()
    flutter_apps = find_flutter_apps(args.root_dir)
    if args.output:
        output_to_file(flutter_apps, args.output)
    else:
        print_flutter_apps(flutter_apps)