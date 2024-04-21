from flutter_finder import find_flutter_apps, print_flutter_apps, output_to_file
import click

@click.command()
@click.argument('root_dir', nargs=1)
@click.option('--output', '-o', help='Output file')
def main(root_dir, output):
    """Find Flutter apps in a directory"""
    flutter_apps = find_flutter_apps(root_dir)
    if output:
        output_to_file(flutter_apps, output)
    else:
        print_flutter_apps(flutter_apps)

if __name__ == '__main__':
    main()