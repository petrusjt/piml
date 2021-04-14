from math import gcd
import io

from htmltree import HTMLNode

def GCD(numbers : list):
    """Computes Greatest Common Divisor of the numbers in the list

    Since gcd(a, b, c, d) = gcd(a, gcd(b, gcd(c, d)))
    """
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

def isTagLine(line):
    """Determines whether the given line is a tag"""
    return len(line) >= 2 and line[-1] == ":" and line[-2:] != "\\:"

def createNodeFromLine(line : str):
    """Creates a node from the given line"""
    tag_and_attributes = line.split()
    return HTMLNode(tag_and_attributes[0], tag_and_attributes[1:])

def getFileLines(fileName : str):
    return [str(line).rstrip() for line in io.open(fileName, "r", encoding="UTF-8").readlines()]