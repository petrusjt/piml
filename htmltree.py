

class HTMLNode:
    def __init__(self, tag="", attributes=(), content="", inline=False):
        self.tag = tag
        self.attributes = attributes
        self.children = []
        self.content = content
        self.parent = None
        self.inline = inline
    
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

    def getChildren(self):
        return self.children

    def getParent(self):
        return self.parent
    
    def isInline(self):
        return self.inline
        


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

    def createHtml(self):
        """
        Creates HTML based on the content of the tree

        Returns str object with the html code
        """
        self.hmtl = ""
        self._traverseTree(self.root.getFirstChild()) # not self.root, because self.root is an empty HTMLNode
        return self.html

    def _traverseTree(self, node, depth=0): 
        self._createOpeningTag(node, depth)
        self._handleChildren(node.getChildren(), depth)
        self._addClosingTag(node, depth)

    def _createOpeningTag(self, node, depth):
        self._appendOpeningTag(node, depth)
        self._addAttributesToOpeningTag(node)
        self._closeOpeningTag(node)

    def _appendOpeningTag(self, node, depth):
        tab = "\t"
        self.html += f"{depth*tab if not node.getParent().isInline() else ''}<{node.tag}{' ' if len(node.attributes) > 0 else ''}"

    def _closeOpeningTag(self, node):
        newLine = "\n"
        self.html += f">{newLine if not node.isInline() else ''}"

    def _addAttributesToOpeningTag(self, node):
        for attribute in node.attributes:
            if attribute[0] == ".":
                self.html += f'class="{attribute[1:]}" '
            elif attribute[0] == "#":
                self.html += f'id="{attribute[1:]}" '
            else:
                self.html += attribute + " "

    def _addClosingTag(self, node, depth):
        tab = "\t"
        newLine = "\n"
        self.html += f"{depth*tab if not node.isInline() else ''}</{node.tag}>{newLine if not node.getParent().isInline() else ''}"

    def _handleChildren(self, children, depth):
        tab = "\t"
        newLine = "\n"
        for child in children:
            if child.tag == "":
                self.html += f"{(depth+1)*tab if (not child.getParent().isInline()) and (not child.isInline()) else ''}{child.content} {newLine if not child.getParent().isInline() else ''}"
            else:
                self._traverseTree(child, depth+1)

    





