

class HTMLNode:
    def __init__(self, tag="", attributes=(), content=""):
        self.tag = tag
        self.attributes = attributes
        self.children = []
        self.content = content
        self.parent = None
    
    def add_child(self, child):
        self.children.append(child)
        self.children[-1].set_parent(self)

    def set_parent(self, parent):
        self.parent = parent

    def get_last_child(self):
        if len(self.children) > 0:
            return self.children[-1]
        return None

    def get_parent(self):
        return self.parent
        


class HTMLTree:
    def __init__(self):
        self.root = HTMLNode()
        self.current_node = self.root
        self.html = ""
        
    def add(self, node : HTMLNode):
        self.current_node.add_child(node)
        
    def go_down(self):
        self.current_node = self.current_node.get_last_child()
    
    def go_up(self):
        self.current_node = self.current_node.get_parent()

    """
    Creates HTML based on the content of the tree

    Param formatted: Whether the HTML should be formatted

    Returns str object with the html code
    """
    def create_html(self):
        self.hmtl = ""
        self._traverse_tree(self.root.children[0]) # not self.root, because self.root is an empty HTMLNode
        return self.html

    def _traverse_tree(self, node, depth=0): # depth is needed for proper indentation
        # These are needed because python complained about escape sequences in interpolated strings
        new_line = "\n"
        tab = "\t"

        # first it creates the html tag
        self.html += f"{depth*tab}<{node.tag}{' ' if len(node.attributes) > 0 else ''}"
        # then adds all the attributes to it
        for attribute in node.attributes:
            if attribute[0] == ".":
                self.html += f'class="{attribute[1:]}" '
            elif attribute[0] == "#":
                self.html += f'id="{attribute[1:]}" '
            else:
                self.html += attribute + " "
        self.html += f">{new_line}"

        # After the attributes it goes over all the children of a given node
        for child in node.children:
            # if the child is not a tag, just appends it to the HTML with the correct indentation
            if child.tag == "":
                self.html += f"{(depth+1)*tab}{child.content} {new_line}"
            # if the child is a tag, then it recursively traverses it too
            else:
                self._traverse_tree(child, depth+1)
        # after the children it closes the tag
        self.html += f"{depth*tab}</{node.tag}>{new_line}"





