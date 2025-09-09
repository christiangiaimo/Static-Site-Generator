from textnode import TextNode, TextType
import os
import shutil
from generate_page import *
import sys


if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = "/"   


def main():
     
    copy_files_to_dir("~/Desktop/workspace/github.com/christiangiaimo/Static-Site-Generator/static","~/Desktop/workspace/github.com/christiangiaimo/Static-Site-Generator/docs")
    generate_pages_recursive("content", "template.html","docs",basepath)


def copy_files_to_dir(source_dir,dest_dir):

    root_dir = os.getcwd()
    expanded_dest_path = os.path.expanduser(dest_dir)
    expanded_source_path = os.path.expanduser(source_dir)
    full_source_path =os.path.abspath(expanded_source_path)
    full_dest_path = os.path.abspath(expanded_dest_path)   
    if not os.path.exists(full_dest_path):
        os.makedirs(full_dest_path,exist_ok= True)
    try:
        shutil.rmtree(full_dest_path)
        print(f"Directory '{full_dest_path}' and its contents were successfully removed. ")
        
    except FileNotFoundError:
        print(f"Directory '{full_dest_path}' does not exists, so nothing was removed.")
    
    list_dir = os.listdir(full_source_path)
    os.makedirs(full_dest_path, exist_ok=True)
    for file in list_dir:
        full_file_path = os.path.join(full_source_path,file)
        dest_dir_path = os.path.join(full_dest_path,file)
        
        if os.path.isdir(full_file_path): 
                
            copy_files_to_dir(full_file_path,dest_dir_path)
        elif os.path.isfile(full_file_path):
            print (f"copying {file}")
            shutil.copy(full_file_path,dest_dir_path)
        else:
            print(f"skipping unknown item {file}")    
        


main()

