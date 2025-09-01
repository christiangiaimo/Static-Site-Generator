from textnode import*
from extract_links import *
import re



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    valid_delimiters = ["`","**","_"]
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise Exception("invalid markdown, formatted section not closed")
        if delimiter not in valid_delimiters:
            raise Exception("invalid markdown, delimiter is not a valid markdown format")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes 



def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = re.split(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",old_node.text)
        
        for i in range(0,len(sections),3):

            text = sections[i]
            if text:
                split_nodes.append(TextNode(text,TextType.TEXT))
            
            if i + 2 < len(sections):
                alt = sections[i+1]
                url = sections[i+2]
                split_nodes.append(TextNode(alt,TextType.IMAGE, url))
            
            
        new_nodes.extend(split_nodes)
    return new_nodes     

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = re.split(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",old_node.text)
        
        for i in range(0,len(sections),3):

            text = sections[i]
            if text:
                split_nodes.append(TextNode(text,TextType.TEXT))
            
            if i + 2 < len(sections):
                alt = sections[i+1]
                url = sections[i+2]
                split_nodes.append(TextNode(alt,TextType.LINK, url))
            
            
        new_nodes.extend(split_nodes)

    return new_nodes        




def text_to_text_nodes(text):
    new_nodes = []
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes,"_",TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    return new_nodes 




     
            



