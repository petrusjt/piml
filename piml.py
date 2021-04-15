from sys import argv, exit
import io

from piml_converter import PIMLConverter

if __name__ == "__main__":
    if len(argv) not in [2, 3]:
        print(
        f"""
        Usage:
            python {argv[0]} <input file>
            python {argv[0]} <input file> <output file>
        """)
        exit(0)

    pimlConverter = PIMLConverter()
    pimlConverter.parse(argv[1])

    if len(argv) == 2:
        print(pimlConverter.createHtml())
    elif len(argv) == 3:
        with io.open(argv[2], "w", encoding="UTF-8") as file:
            file.write(pimlConverter.createHtml())

    


