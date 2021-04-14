

class HTMLNode:
    def __init__(self, tag="", attributes=(), content=""):
        self.tag = tag
        self.attributes = attributes
        self.children = []
        self.content = content
        self.parent = None
    
    def addChild(self, child):
        self.children.append(child)
        self.children[-1].setParent(self)

    def setParent(self, parent):
        self.parent = parent

    def getFirstChild(self):
        if len(self.children) > 0:
            return self.children[0]
        return None

    def getLastChild(self):
        if len(self.children) > 0:
            return self.children[-1]
        return None

    def getParent(self):
        return self.parent
        


class HTMLTree:
    def __init__(self):
        self.root = HTMLNode()
        self.currentNode = self.root
        self.html = ""
        
    def add(self, node : HTMLNode):
        self.currentNode.addChild(node)
        
    def goDown(self):
        self.currentNode = self.currentNode.getLastChild()
    
    def goUp(self):
        self.currentNode = self.currentNode.getParent()

    """
    Creates HTML based on the content of the tree

    Param formatted: Whether the HTML should be formatted

    Returns str object with the html code
    """
    def createHtml(self):
        self.hmtl = ""
        self._traverseTree(self.root.getFirstChild()) # not self.root, because self.root is an empty HTMLNode
        return self.html

    def _traverseTree(self, node, depth=0): # depth is needed for proper indentation
        # These are needed because python complained about escape sequences in interpolated strings
        newLine = "\n"
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
        self.html += f">{newLine}"

        # After the attributes it goes over all the children of a given node
        for child in node.children:
            # if the child is not a tag, just appends it to the HTML with the correct indentation
            if child.tag == "":
                self.html += f"{(depth+1)*tab}{child.content} {newLine}"
            # if the child is a tag, then it recursively traverses it too
            else:
                self._traverseTree(child, depth+1)
        # after the children it closes the tag
        self.html += f"{depth*tab}</{node.tag}>{newLine}"





