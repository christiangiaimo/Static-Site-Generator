from markdown_to_html import markdown_to_html_node
from htmlnode import *
from extract_title import *
import os



def generate_page(from_path,template_path,dest_path):
    expanded_from_path = os.path.expanduser(from_path)
    full_from_path = os.path.abspath(expanded_from_path)
    expanded_temp_path = os.path.expanduser(template_path)
    full_temp_path = os.path.abspath(expanded_temp_path)
    expanded_dest_path = os.path.expanduser(dest_path)
    full_dest_path = os.path.abspath(expanded_dest_path)
    dest_dir = os.path.dirname(full_dest_path)
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(full_from_path,'r',encoding='utf-8') as file:
        content = file.read()
    temp_file = open(full_temp_path,'r',encoding='utf-8')
    temp_content = temp_file.read()
    node = markdown_to_html_node(content)
    title = extract_title(content)
    text = node.to_html()
    
    modified_template = temp_content.replace("{{ Title }}",title).replace("{{ Content }}",text)
    
    if not os.path.exists(full_dest_path):
        os.makedirs(dest_dir,exist_ok= True)
    with open (full_dest_path,'w',encoding='utf-8') as dest_file:
        dest_file.write(modified_template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    expanded_from_path = os.path.expanduser(dir_path_content)
    full_from_path = os.path.abspath(expanded_from_path)
    expanded_dest_path = os.path.expanduser(dest_dir_path)
    full_dest_path = os.path.abspath(expanded_dest_path)

    list_of_dirs = os.listdir(full_from_path)
    os.makedirs(full_dest_path, exist_ok=True)
    for file in list_of_dirs:
        full_path = os.path.join(full_from_path,file)
        full_dest_file_path = os.path.join(full_dest_path,os.path.splitext(file)[0]+ ".html")
        if os.path.isdir(full_path):   
            generate_pages_recursive(full_path,template_path,os.path.join(full_dest_path,file))
        elif os.path.isfile(full_path) and os.path.splitext(file)[1] == ".md": 
            print(f"creating {file}.html file")     
            generate_page(full_path,template_path,full_dest_file_path)
        else:
            print("skipping unknown file")     



