import argparse
import utils
from python_ast import PythonAST
from levenstein import get_levenstein_distance_normalized

def main(input_file, output_file):
    output = open(output_file, "w")

    with open(input_file) as input:
        for line in input:
            [filename1, filename2] = line.strip().split(" ", 1)

            is_valid_filename1 = utils.file_exists(filename1)
            is_valid_filename2 = utils.file_exists(filename2)

            if (not (is_valid_filename1 and is_valid_filename2)):
                message = "Invalid path(s): "
                if (not is_valid_filename1):
                    message += f"{filename1!r}"
                if (not is_valid_filename2):
                    message += f", {filename2!r}"
                message += "\n"
                output.write(message)
                continue
            
            ast1 = PythonAST(filename1)
            ast2 = PythonAST(filename2)
            
            # ast preprocessing
            # ...


            # calculate the metric with processed programms
            result = get_levenstein_distance_normalized(
                ast1.get_programm_text(),
                ast2.get_programm_text(),
            )

            output.write(f"{1.0 - result}\n")
    
    output.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Argument parser")
    parser.add_argument("input_file", default="input.txt", help="Specify input filename")
    parser.add_argument("output_file", default="scores.txt", help="Specify output filename")
    args = parser.parse_args()

    utils.check_file_exists(args.input_file)
    main(args.input_file, args.output_file)
