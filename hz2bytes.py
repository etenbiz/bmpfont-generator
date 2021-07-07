# To generate mapped bytes for embedded printing.
#
#   Author : Janvier Peng
#   Date   : JUN 16, 2021
#

import sys
import argparse

def main():

    # parsing arguments
    parser = argparse.ArgumentParser(description='To generate bytes for bitmap fonts printing.')
    parser.add_argument('-i', '--input', required=False, help="the input file which contains all the needed characters. default: input.txt")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-m', '--message', help="the string which contains chinese to be printed.")
    group.add_argument('-n', '--interactive', action="store_true", help="enter the interactive mode. (q for quit)")
    args = parser.parse_args()

    # init the default values
    input_file = "input.txt" if not args.input else args.input

    # read inputs from file
    with open(input_file, "r") as fin:
        chars_raw = fin.read().strip()
        chars_utf8 = ''. join(sorted(set(chars_raw), key=chars_raw.index))
        chars_gb2312 = chars_utf8.encode("gb2312")
    
    # calculate the positions in stripped font file.
    if args.interactive:
        print("Interactive mode. (q for quit)")
    while(True):
        if args.interactive:
            print("? ", end="")
            in_chars = input()
            if in_chars == "q" or in_chars == "Q":
                break
            else:
                in_chars = in_chars.encode("gb2312")
        else:
            in_chars = args.message.encode("gb2312")
        pos = 0xA0A0
        res = bytearray()
        i = 0
        while i < len(in_chars):
            if in_chars[i] >= 0xA0:
                n = chars_gb2312.find(in_chars[i:i+2])
                if n == -1:
                    err_char = in_chars[i:i+2].decode("gb2312")
                    print(f"Error: character(s) not present in input file. ({err_char})")
                    sys.exit(1)
                res.extend(int.to_bytes(pos + n // 2, length=2, byteorder="big"))
                i += 1
            else:
                res.extend(bytes([in_chars[i]]))
            i += 1
        print(bytes(res))
        if not args.interactive:
            break


if __name__ == "__main__":
    main()