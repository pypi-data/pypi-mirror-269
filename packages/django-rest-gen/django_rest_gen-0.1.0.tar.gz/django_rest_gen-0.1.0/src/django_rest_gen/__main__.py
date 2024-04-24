import argparse
import os
from . import apigen


def main():
    parser = argparse.ArgumentParser(prog='django-rest-gen', description='Generate Django REST API code')
    parser.add_argument('--pythonpath', default=".", help="Python Path directory. ")
    parser.add_argument('--settings', required=True, help="The path to the django project settings")
    parser.add_argument('--apppath', required=True, help="The path to the app")
    parser.add_argument('--overwrite', action='store_true',
                        help="Whether to overwrite existing files if any")
    parser.add_argument('--dummy', action='store_true',
                        help="Whether to generate dummy data generator")
    args = parser.parse_args()
    print(f"args: {args}")
    base_path = os.path.abspath('.')
    apigen.workflow(python_path=base_path, settings_fpath=args.settings, app_path=args.apppath,
                    overwrite=args.overwrite, dummy=args.dummy)


main()
