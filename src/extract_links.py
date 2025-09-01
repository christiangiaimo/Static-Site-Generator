import re
from textnode import *
from htmlnode import *


def extract_markdown_images(text):
    if text is None:
        raise Exception ("There is no text")
    else:
        list = []
        regular_expr = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
        matches = re.findall(regular_expr,text)
        if matches == []:
            raise Exception ("The text does not have have a valid markdown image")
    
        else:
            list.extend(matches)
        return list

def extract_markdown_links(text):
    if text is None:
        raise Exception ("There is no text")
    else:
        list = []
        regular_expr = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
        matches = re.findall(regular_expr,text)
        if matches == []:
            raise Exception ("The text does not have a valid markdown link")
        else:
            list.extend(matches)
        return list


