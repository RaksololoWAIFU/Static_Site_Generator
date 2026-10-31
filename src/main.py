from textnode import TextNode,TextType
import os
import shutil
from gencontent import generate_page,generate_pages_recursive



def main():
    source_to_destination("static","public")
    generate_pages_recursive("content","template.html","public")

def source_to_destination(source,destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    for x in os.listdir(source):
        path = os.path.join(source,x)
        if os.path.isfile(path):
            shutil.copy(path,destination)
        else:
            folder_path = os.path.join(destination,x)
            source_to_destination(path,folder_path)
        








main()