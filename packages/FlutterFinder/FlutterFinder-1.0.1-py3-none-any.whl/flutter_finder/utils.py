import datetime
import os


def find_flutter_apps(root_dir):
    flutter_apps = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file == 'pubspec.yaml':
                app_dir = os.path.dirname(os.path.join(root, file))
                app_name = os.path.basename(app_dir)
                last_edited = None
                flutter_version = None
                try:
                    timestamp = os.path.getmtime(os.path.join(app_dir, 'pubspec.yaml'))
                    last_edited = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                except OSError:
                    pass
                try:
                    with open(os.path.join(app_dir, 'pubspec.yaml'), 'r') as f:
                        for line in f:
                            if 'sdk:' in line:
                                flutter_version = line.split(':')[1].strip()
                                break
                except FileNotFoundError:
                    pass
                flutter_apps.append({
                    'app_name': app_name,
                    'app_dir': app_dir,
                    'last_edited': last_edited,
                    'flutter_version': flutter_version
                })
    return flutter_apps

def print_flutter_apps(flutter_apps):
    print("Flutter Apps:")
    print("------------")
    print(f"Total Apps: {len(flutter_apps)}")
    flutter_versions = {}
    for app in flutter_apps:
        if app['flutter_version']:
            if app['flutter_version'] in flutter_versions:
                flutter_versions[app['flutter_version']] += 1
            else:
                flutter_versions[app['flutter_version']] = 1
    print("Flutter Versions:")
    for version, count in flutter_versions.items():
        print(f"  {version}: {count}")
    print("------------")
    for app in flutter_apps:
        print(f"App Name: {app['app_name']}")
        print(f"App Dir: {app['app_dir']}")
        if app['last_edited']:
            print(f"Last Edited: {app['last_edited']}")
        if app['flutter_version']:
            print(f"Flutter Version: {app['flutter_version']}")
        print("------------")

def output_to_file(flutter_apps, output_file):
    with open(output_file, 'w') as f:
        f.write("Flutter Apps:\n")
        f.write("------------\n")
        f.write(f"Total Apps: {len(flutter_apps)}\n")
        flutter_versions = {}
        for app in flutter_apps:
            if app['flutter_version']:
                if app['flutter_version'] in flutter_versions:
                    flutter_versions[app['flutter_version']] += 1
                else:
                    flutter_versions[app['flutter_version']] = 1
        f.write("Flutter Versions:\n")
        for version, count in flutter_versions.items():
            f.write(f"  {version}: {count}\n")
        f.write("------------\n")
        for app in flutter_apps:
            f.write(f"App Name: {app['app_name']}\n")
            f.write(f"App Dir: {app['app_dir']}\n")
            if app['last_edited']:
                f.write(f"Last Edited: {app['last_edited']}\n")
            if app['flutter_version']:
                f.write(f"Flutter Version: {app['flutter_version']}\n")
            f.write("------------\n")
