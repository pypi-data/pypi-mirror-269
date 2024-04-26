import re
import sys
from pathlib import Path
import os

from redundantcss.validateArgs import parse_classes, check_folder_contents

def main():
    usage = """USAGE: python redundantcss.py 'stylesheet_path' 'template_path_or_template_paths'

Description:
  This script analyzes a stylesheet and identifies redundant CSS rules not used by the templates provided.

Arguments:
  - 'stylesheet_path': Path to the CSS stylesheet to be analyzed.
  - 'template_path_or_template_paths': Path to a folder containing HTML templates or paths to individual template files.

Examples:
  1. Analyze a single template:
     python redundantcss.py 'styles.css' 'template.html'

  2. Analyze multiple templates in a folder:
     python redundantcss.py 'styles.css' 'templates/'

  3. Analyze multiple templates provided as separate arguments:
     python redundantcss.py 'styles.css' 'template1.html' 'template2.html' 'template3.html'"""
    
    if len(sys.argv) < 3:
        print(usage)
        sys.exit()

    elif len(sys.argv) == 3: 
        # Check if filepath for 2nd arg exists
        if not os.path.exists(sys.argv[2]):
            print("Your folder or filepath does not exist, run 'redundantcss' on its own for usage.")
            sys.exit()
        template_info = sys.argv[2]

    # Multiple args accepts multiple html files instead of folder path. 
    elif len(sys.argv) > 3:
        template_info = sys.argv[2:]
        # Check each filepath for validity before continuing
        for file in template_info:
            if not file.endswith(".html"):
                print(f"Error with '{file}', please end filename with '.html' and ensure it exists.")
                sys.exit()
            if not os.path.exists(file):
                print(f"'{file}' does not exist, please ensure this is the correct path and try again.")
                sys.exit()

    if not os.path.exists(sys.argv[1]):
        print("Stylesheet path does not exist, run 'redundantcss' on its own for usage.")
        sys.exit()
    stylesheet_path = sys.argv[1]

    css_classes: list = get_css_classes(stylesheet_path)
    html_classes: set = get_html_classes(template_info)
    unused_classes: list = compare_classes(css_classes, html_classes)

    print(f"You have {len(unused_classes)} unused classes out of {len(css_classes)}.")
    print(f"All unused CSS classes:")
    for item in unused_classes:
        print(item)


def get_css_classes(stylesheet: str):
    with open(stylesheet, 'r') as file:
        content = file.readlines() # Read the contents of CSS file

    classes = [] # Create list that includes each CSS class
    for line in content:
        if line.startswith("."): # Find the classes created within the stylesheet
            # Remove class indicator and opening brackets
            css_class = line.strip().lstrip(".").rstrip(" {")
            if not re.search(r"^.*(\s|:)+.*$", css_class):
                classes.append(css_class)

    return classes


def get_html_classes(path):
    classes_used = set()
    # If multiple template files are including in calling arguments.
    if type(path) == list:
        for item in path:
            with open(item, 'r') as html_sheet:
                classes_used.update(parse_classes(html_sheet))
    # If only a single template argument is passed and is a template file.
    elif path.endswith(".html"):
        with open(path, 'r') as html_sheet:
            classes_used.update(parse_classes(html_sheet))
    # If only a single template argument is passed and is a folder path.
    else:
        folder_path = Path(path)
        if not check_folder_contents(folder_path):
            print("There are no HTML files in this folder")
            sys.exit()

        for file_path in folder_path.iterdir():
            if file_path.is_file() and str(file_path).endswith(".html"):
                with open(file_path, 'r') as html_sheet:
                    classes_used.update(parse_classes(html_sheet)) 

    return classes_used 


def compare_classes(css_classes: list, html_classes: list):
    unused_classes = []
    for item in css_classes:
        if item not in html_classes:
            unused_classes.append(item)

    return unused_classes


if __name__ == "__main__":
    main()