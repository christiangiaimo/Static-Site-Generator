from markdown_blocks import *

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    line = blocks[0].split("\n")
    if line[0].startswith("#"):
        if line[0].startswith("# "):
            return line[0].strip("# ")
        else:
            return line[0].strip("#")
    else:
        raise Exception("Not a valid header")






    #if markdown[0] != "#":
     #   raise Exception("Not a valid header")
    #elif markdown[1] == "#" or markdown[1] != "":
    #    raise Exception("Not a valid header"):
    #elif markdown[1]=="":
    #    return markdown[2:].strip()
    #else:
    #    return markdown[1:].strip()
    
