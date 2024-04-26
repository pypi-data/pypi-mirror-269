# RedundantCSS
##### Current Version: V0.0.3

### **Contents:**
- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)

## **Description:**
This script analyzes a stylesheet and identifies redundant CSS classes not used by the templates provided. The script prints the names of all unused classes to the terminal, at which point you can go to the stylesheet and delete unused classes.
<br>
Currently this package only detects unused classes, [more features](#coming-soon) are on the way!

## **Installation:**
    pip install redundantcss

## **Usage:**
    redundantcss 'stylesheet_path' 'template_path_or_template_paths'

Arguments:
  - 'stylesheet_path': Path to the CSS stylesheet to be analyzed.
    - If your styles.css sheet is within another folder, please specify this folder first, eg *static/styles.css*.
  - 'template_path_or_template_paths': Path to a folder containing HTML templates or paths to individual template files.

Examples:
  1. Analyze a single template:
     python redundantcss.py 'styles.css' 'template.html'

  2. Analyze multiple templates in a folder:
     python redundantcss.py 'styles.css' 'templates/'

  3. Analyze multiple templates provided as separate arguments:
     python redundantcss.py 'styles.css' 'template1.html' 'template2.html' 'template3.html'

<hr>

## **COMING SOON:** 
- Use argparse for specific arguments, eg --usage, --dil, --rc
- Give option to rewrite CSS file without redundant classes.
- Create detect_inline_styling(). Dict with value being list of tuples.
- Refactor functions and create more specific functions for current actions.
- Provide clear documentation.
- Detect media queries, id styles, and element styles.
- Allow user to pass just the folder name containing .css file.
- Parameterize ‘.html’ stuff.