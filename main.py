#!/usr/bin/python3

import argparse
from algorithms import algorithms

def main():
    parser = argparse.ArgumentParser(description="A program to encode files using different algorithms")

    actions = parser.add_argument_group("actions")
    algorithm_options = [ "huffman" ]
    actions.add_argument("-a", "--algorithm",
                        help="Specifies the algorithm to use.",
                        metavar='algorithm', 
                        choices=algorithm_options
                        
                        )
    actions.add_argument("-d", "--decode", action="store_true")
    actions.add_argument("input", nargs="?", help="Input file.")
    actions.add_argument("output", nargs="?", help="Output file.")

    listings = parser.add_argument_group("listings")
    listings.add_argument("--list-algorithms", action="store_true", help="List all available algorithms.")

    args = parser.parse_args()

    if args.list_algorithms:
        print("Available algorithm options are:")
        for a in algorithm_options:
            print(f"    - \"{a}\"")
        return
    if not args.algorithm: 
        print("Must provide an algorithm. Run with --list-algorithms to see available options.")
        return
    if not args.input:
        print("Must provide an input file")
        return

    if not args.decode:
        if (args.output):
            output_file = args.output
        else:
            parts = args.input.split(".")
            if len(parts) > 1:
                parts.pop(-1)
            output_file = ".".join(parts) + algorithms[args.algorithm].extension

        encoder = algorithms[args.algorithm].encoder

        encode(args.input, output_file, encoder)

    else:
        if not args.output:
            raise Exception("If decoding file an output filename must be provided")

        decoder = algorithms[args.algorithm].decoder
        decode(args.input, args.output, decoder)

    

def encode(input_file, output_file, encoder):
    with open(input_file, "r") as f_in:
        input = f_in.read()

    output = encoder.encode(input)

    with open(output_file, "wb") as f_out:
        f_out.write(output)

def decode(input_file, output_file, decoder):
    with open(input_file, "rb") as f_in:
        input = f_in.read()

    output = decoder.decode(input)

    with open(output_file, "wb") as f_out:
        f_out.write(output)


if __name__ == "__main__":
    main()
