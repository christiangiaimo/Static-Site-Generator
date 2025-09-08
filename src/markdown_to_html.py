from htmlnode import *
from markdown_blocks import *
from split_delimiter import *
from textnode import *





def divide_blocks(markdown):
    blocks = markdown_to_blocks(markdown) #Divide into blocks
    block_list = []
    for block in blocks:
        block_type = block_to_block_type(block) # Determine the type of block and create a HTML node
        if block_type == BlockType.QUOTE:
            lines = block.split("\n")
            stripped_lines = [l[2:] if l.startswith("> ") else l[1:] for l in lines if l]
            text = " ".join(stripped_lines)
            children = text_to_children(text) 
            block_list.append(ParentNode("blockquote",children))            
        if block_type == BlockType.ULIST:
            lines = block.split("\n")
            li_nodes = []
            for line in lines:
                if not line:
                    continue
                text = line[2:]
                li_nodes.append(ParentNode("li",text_to_children(text)))
            block_list.append(ParentNode("ul",li_nodes))    
            
        if block_type == BlockType.OLIST:
            lines = block.split("\n")
            li_nodes = []
            for line in lines:
                if not line: continue
                m = re.match(r"^\d+\.\s(.*)$", line)
                text = m.group(1) if m else line
                li_nodes.append(ParentNode("li", text_to_children(text)))
            block_list.append(ParentNode("ol", li_nodes))

        if block_type == BlockType.CODE:
            raw = "\n".join(block.split("\n")[1:-1]) + "\n"
            code_node = LeafNode("code", raw)
            block_list.append(ParentNode("pre", [code_node]))
        if block_type == BlockType.HEADING:
            head_block = parse_heading(block)
            if head_block:           
                block_list.append(head_block)
        if block_type == BlockType.PARAGRAPH:
            if not block.strip():
                continue
            joined = " ".join(line.strip() for line in block.split("\n") if line.strip())
            joined = re.sub(r"\s+", " ", joined)
            
            children = text_to_children(joined)
            block_list.append(ParentNode("p", children))    
    return block_list


def text_to_children(text):
    text_nodes = text_to_text_nodes(text)
    children_html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children_html_nodes.append(html_node)
    return children_html_nodes


def parse_heading(block):
    i = 0
    n = len(block)
    while i < n and i < 6 and block[i] == "#":
        i+=1
    if i == 0:
        return None    
    if i >= n or block[i] != " ":
        return None
    level = i
    text = block[i+1:]
    tag = f"h{level}"
    children = text_to_children(text)
    return ParentNode(tag,children)
    
def block_to_leaf_nodes(blocks):
    leaf_nodes = []
    for block in blocks:
        leaf_nodes.append(LeafNode(block))
    return leaf_nodes

def blocks_to_div_children(nodes): #this takes a list of blocks and make them children of asingle div parent block
    div_block = ParentNode("div",nodes)
    return div_block         


def final_html(parent_node):
    return parent_node.to_html()
    
    

def markdown_to_html_node(markdown):   
    nodes = divide_blocks(markdown)
    return ParentNode("div",nodes)
    

         






