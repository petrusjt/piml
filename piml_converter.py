from math import gcd

from htmltree import HTMLTree, HTMLNode
from helpers import GCD, isTagLine, createNodeFromTagLine, getFileLines

class PIMLConverter:
    """Handles the parsing of .piml files"""

    def __init__(self):
        self.htmlTree = HTMLTree()
        self.currentIndentation = 0

    def parse(self, fileName : str):
        # So on every call the class is in the correct state to handle it
        self.htmlTree = HTMLTree()
        self.currentIndentation = 0

        lines = getFileLines(fileName)

        self.buildHTMLTree(self.createIndentationLinePairs(lines))

    def buildHTMLTree(self, indentationLinePair : list):
        for pair in indentationLinePair:
            if isTagLine(pair[1]):
                self.handleTagLine(pair)
            else:
                self.handleNonTagLine(pair)

    def handleTagLine(self, pair):
        line = pair[1]

        if pair[0] == self.currentIndentation:
            self.currentIndentation += 1
            self.htmlTree.add(createNodeFromTagLine(line))
            self.htmlTree.goDown()
        elif pair[0] < self.currentIndentation:
            for _ in range(self.currentIndentation - pair[0]):
                self.htmlTree.goUp()

            self.htmlTree.add(createNodeFromTagLine(line))
            self.htmlTree.goDown()
            self.currentIndentation = pair[0] + 1

    def handleNonTagLine(self, pair):
        content = pair[1].replace("\\", "")

        if pair[0] == self.currentIndentation:
            self.htmlTree.add(HTMLNode(content=content))
        elif pair[0] < self.currentIndentation:
            for _ in range(self.currentIndentation - pair[0] ):
                self.htmlTree.goUp()

            self.htmlTree.add(HTMLNode(content=content))
            self.currentIndentation = pair[0]

    def calculateLeadingSpaces(self, lines : list):
        """Returns the number of leading spaces of the lines in a list"""
        return [len(line) - len(line.lstrip()) for line in lines]

    def calculateUsedIndentation(self, lines : list):
        """Returns the used indentation of the lines"""
        return GCD(self.calculateLeadingSpaces(lines))        

    def createIndentationLinePairs(self, lines : list):
        """Creates a list of pairs of indentations and the lines indentations belong to"""
        used_indentation = self.calculateUsedIndentation(lines)
        return [((len(line) - len(line.lstrip())) // used_indentation, line.strip()) 
                        for line in lines]

    def createHtml(self):
        """Calls self.htmlTree's create_html method"""
        return self.htmlTree.createHtml()
