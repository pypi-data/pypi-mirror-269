# RedundantCSS
#### Video Demo: Coming soon

### **Contents:**
- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)

## **Description:**
This script analyzes a stylesheet and identifies redundant CSS classes not used by the templates provided. The script prints the names of all unused classes to the terminal, at which point you can go to the stylesheet and delete unused classes.
<br>

**COMING IN V2:** Remove the manual aspect of removing the CSS and give user the option for this process to be done automatically.
<hr>

## **Installation:**
**COMING SOON**

<hr>

## **Usage:**
    python3 redundantcss.py 'stylesheet_path' 'template_path_or_template_paths'

Arguments:
  - 'stylesheet_path': Path to the CSS stylesheet to be analyzed.
  - 'template_path_or_template_paths': Path to a folder containing HTML templates or paths to individual template files.

Examples:
  1. Analyze a single template:
     python redundantcss.py 'styles.css' 'template.html'

  2. Analyze multiple templates in a folder:
     python redundantcss.py 'styles.css' 'templates/'

  3. Analyze multiple templates provided as separate arguments:
     python redundantcss.py 'styles.css' 'template1.html' 'template2.html' 'template3.html'