from bs4 import BeautifulSoup

def parse_classes(html_sheet):
    classes = set()
    content = html_sheet.read()
    soup = BeautifulSoup(content, 'html.parser')
    elements_with_class = soup.find_all(class_=True)

    for element in elements_with_class:
        classes.update(element.get("class"))
    
    return classes


def check_folder_contents(path):
    html_count = 0
    other_file_count = 0
    for file_path in path.iterdir():
        if str(file_path).endswith(".html"):
            html_count += 1
        else:
            other_file_count += 1

    if other_file_count >= 0 and html_count == 0:
        return False
    elif html_count > 0:
        return True