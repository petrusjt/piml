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

def __print_list(lst):
    for item in lst:
        print(item)

def isTagLine(line):
    return len(line) >= 2 and line[-1] == ":" and line[-2:] != "\\:"

def GCD(numbers):
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

def create_node_from_line(line : str):
    tag_and_attributes = line.split()
    return HTMLNode(tag_and_attributes[0], tag_and_attributes[1:])

def interpret(lines : list, reset_html_tree=False):
    global htmlTree

    if reset_html_tree:
        htmlTree = HTMLTree()

    leading_spaces = []
    for line in lines:
        leading_spaces.append(len(line) - len(line.lstrip()))

    used_indentation = GCD(leading_spaces)

    indentation_line_pair = []
    for line in lines:
        indentation_line_pair += [((len(line) - len(line.lstrip())) // used_indentation, line.strip())]

    
    current_indentation = 0
    for pair in indentation_line_pair:
        #print(pair, current_indentation, sep="\t")

        if isTagLine(pair[1]):
            if pair[0] == current_indentation:
                current_indentation += 1

                htmlTree.add(create_node_from_line(pair[1][:-1]))

                htmlTree.go_down()

            elif pair[0] < current_indentation:
                for _ in range(current_indentation - pair[0]):
                    htmlTree.go_up()
                htmlTree.add(create_node_from_line(pair[1][:-1]))
                htmlTree.go_down()
                current_indentation = pair[0] + 1
        else:
            if pair[0] == current_indentation:
                htmlTree.add(HTMLNode(content=pair[1].replace("\\", "")))
            elif pair[0] < current_indentation:
                for _ in range(current_indentation - pair[0] ):
                    htmlTree.go_up()
                htmlTree.add(HTMLNode(content=pair[1].replace("\\", "")))
                current_indentation = pair[0]



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

    


