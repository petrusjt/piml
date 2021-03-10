from sys import argv, exit
from math import gcd
import io

from htmltree import HTMLTree, HTMLNode

if __name__ == "__main__":
    if len(argv) not in [2, 3]:
        print(
        f"""
        Usage:
            python {argv[0]} <input file>
            python {argv[0]} <input file> <output file>
        """)
        exit(0)

htmlTree = HTMLTree()
"""
Determines whether the given line is a tag
"""
def isTagLine(line):
    return len(line) >= 2 and line[-1] == ":" and line[-2:] != "\\:"

"""
Computes Greatest Common Divisor of the numbers in the list

Since gcd(a, b, c, d) = gcd(a, gcd(b, gcd(c, d)))
"""
def GCD(numbers : list):
    numbers = sorted(numbers)

    if len(numbers) == 0:
        return None
    elif len(numbers) == 1:
        return numbers[0]
    elif len(numbers) == 2:
        return gcd(numbers[0], numbers[2])
    
    gcd_ = gcd(numbers[0], numbers[1])
    for i in range(2, len(numbers)):
        gcd_ = gcd(gcd_, numbers[i])

    return gcd_

"""
Creates a node from the given line
"""
def create_node_from_line(line : str):
    tag_and_attributes = line.split()
    return HTMLNode(tag_and_attributes[0], tag_and_attributes[1:])

"""
Builds the HTMLTree from the input
"""
def interpret(lines : list):
    global htmlTree

    # Creates a new HTMLTree object
    htmlTree = HTMLTree()

    #Calculates the amount of leading spaces for each line of the input
    leading_spaces = []
    for line in lines:
        leading_spaces.append(len(line) - len(line.lstrip()))

    # Calculates how many spaces are used as indentation
    used_indentation = GCD(leading_spaces)

    # Creates a list of pairs of indentations and the lines indentations belong to
    indentation_line_pair = []
    for line in lines:
        indentation_line_pair += [((len(line) - len(line.lstrip())) // used_indentation, line.strip())]

    # Sets current indentation to 0
    current_indentation = 0
    for pair in indentation_line_pair:
        # checks if current line is a tag
        if isTagLine(pair[1]):
            # if the current indentation equals to the line's indentation, adds the line to the HTMLTree as an HTMLNode and 
            # tells the tree that the current node is the recently added one
            if pair[0] == current_indentation:
                current_indentation += 1
                htmlTree.add(create_node_from_line(pair[1][:-1]))
                htmlTree.go_down()
            # if the current indentation is greater than the line's, tells the tree to go to the current line's parent
            # and adds the line to the HTMLTree as an HTMLNode, then tells the tree that the current node is the recently added one
            # 
            elif pair[0] < current_indentation:
                for _ in range(current_indentation - pair[0]):
                    htmlTree.go_up()
                htmlTree.add(create_node_from_line(pair[1][:-1]))
                htmlTree.go_down()
                current_indentation = pair[0] + 1
        # the pair[1][:-1] is used, because ':' at the end of the lines signals that the current line is a tag
        
        # if current line isn't a tag
        else:
            # if the current line's indentation is equal to the current_indentation
            # it just adds it to the HTMLTree
            if pair[0] == current_indentation:
                htmlTree.add(HTMLNode(content=pair[1].replace("\\", "")))
            # if the current line's indentation is less than the current_indentation,
            # it tells the HTMLTree to go up to the current line's parent
            # and adds it to the HTMLTree
            elif pair[0] < current_indentation:
                for _ in range(current_indentation - pair[0] ):
                    htmlTree.go_up()
                htmlTree.add(HTMLNode(content=pair[1].replace("\\", "")))
                current_indentation = pair[0]
            # the .replace("\\","") is used, because : is escaped via \ in order to not be classified as a tag


"""
Calls HTMLTree's create_html method
"""
def create_html():
    global htmlTree

    return htmlTree.create_html()

if __name__ == "__main__":
    lines = [line.rstrip() for line in io.open(argv[1], "r", encoding="UTF-8").readlines()]
    interpret(lines)
    if len(argv) == 2:
        print(create_html())
    elif len(argv) == 3:
        with io.open(argv[2], "w", encoding="UTF-8") as file:
            file.write(create_html())

    


