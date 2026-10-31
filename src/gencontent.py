import os
from pathlib import Path


from blocknodes import markdown_to_html_node

def extract_title(markdown):
    block = markdown.split("\n")
    for x in block:
        if x.startswith("# "):
            sliced = x[2:]
            remove_whitespace = sliced.strip()
            return remove_whitespace
    raise Exception("there is no h1 header")



def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        contents = file.read()
    with open(template_path, "r") as file_template:
        contents_template = file_template.read()
    content = markdown_to_html_node(contents)
    new_content = content.to_html()
    title = extract_title(contents)
    replaced_content = contents_template.replace("{{ Title }}", title)
    replaced_all = replaced_content.replace("{{ Content }}", new_content)
    path = os.path.dirname(dest_path)
    os.makedirs(path, exist_ok=True)
    with open(dest_path, "w") as writing_to_file:
        writing_to_file.write(replaced_all)



def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for x in os.listdir(dir_path_content):
        path = os.path.join(dir_path_content, x)
        if os.path.isfile(path):
            path2 = os.path.join(dest_dir_path,x)
            p = Path(path2)
            new_p = p.with_suffix(".html")
            generate_page(path,template_path,new_p)
        else:
            folder_path = os.path.join(dest_dir_path,x)
            generate_pages_recursive(path,template_path,folder_path)
