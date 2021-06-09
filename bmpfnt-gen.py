import numpy as np
import os
import re
import sys
import argparse

def get_bmp_font(bmpfnt, bmpsym, single_char, font_height):
    result = b''
    if len(single_char) == 2 and type(single_char) == bytes:
        if font_height == 12:
            font_length = (font_height + 4) // 8 * font_height
        else:
            font_length = font_height // 8 * font_height
        area = single_char[0] - 0xA0
        index = single_char[1] - 0xA0
        if font_height in [24, 40, 48]:
            if area - 1 >= 15:
                offset = (94 * (area - 1 - 15) + (index - 1)) * font_length
                result = bmpfnt[offset : offset + font_length]
            else:
                offset = (94 * (area - 1) + (index - 1)) * font_length
                result = bmpsym[offset : offset + font_length]
        else:
            offset = (94 * (area - 1) + (index - 1)) * font_length
            result = bmpfnt[offset : offset + font_length]
        if font_height == 24:
            result = np.packbits(
                    np.flip(
                        np.rot90(
                            np.reshape(
                                np.unpackbits(
                                    np.frombuffer(result, dtype=np.dtype('B'))
                                ),
                                (font_height, font_height)
                            ),
                            k=3
                        ),
                        axis=1
                    ).flatten()
                ).tobytes()
    return result

def main():

    # parsing arguments
    parser = argparse.ArgumentParser(description='To generate bitmap font file for specific simplified Chinese characters. (GB2312 only)')
    parser.add_argument('-f', '--font-file', required=False, help="the font file. default: fonts/HZK12")
    parser.add_argument('-i', '--input', required=False, help="the input file which contains all the needed characters. default: input.txt")
    parser.add_argument('-o', '--output', required=False, help="the output file of bitmap font. default: hzk12.fnt")
    args = parser.parse_args()

    # check if the font file is exist
    font_file = "fonts/HZK12" if not args.font_file else args.font_file
    m = re.match('^.*HZK([\d]+)[FHKS]?$', font_file)
    if not m or not os.access(font_file, os.R_OK):
        print("Unable to read font file: {}".format(font_file))
        sys.exit(2)
    else:
        font_bits = int(m.group(1))

    # init the default values
    input_file = "input.txt" if not args.input else args.input
    output_dir = "dist"
    output_bin = "{}/hzk{}.fnt".format(output_dir, font_bits) if not args.output else args.output
    output_txt = "{}/hzk{}.txt".format(output_dir, font_bits) if not args.output else args.output + ".txt"

    # read inputs from file
    with open(input_file, "r") as fin:
        chars_raw = fin.read().strip()
        chars_utf8 = ''. join(sorted(set(chars_raw), key=chars_raw.index))
        chars_gb2312 = chars_utf8.encode("gb2312")

    # read the font file
    with open(font_file, "rb") as ffnt:
        bmpfnt = ffnt.read()

    # read the symbol file if necessary
    bmpsym = None
    if font_bits in [24, 40, 48]:
        with open(font_file[:-1] + "T", "rb") as ffnt:
            bmpsym = ffnt.read()

    # create the distributable directory if does not exist
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir, mode=0o755)

    # generate the bitmap font file which is just contains the input characters.
    with open(output_txt, "w") as fout_txt:
        fout_txt.write("       ０ １ ２ ３ ４ ５ ６ ７ ８ ９ Ａ Ｂ Ｃ Ｄ Ｅ Ｆ\n")
        with open(output_bin, "wb") as fout_bin:
            for i in range(0, len(chars_gb2312)//2):
                fout_bin.write(get_bmp_font(bmpfnt, bmpsym, chars_gb2312[i*2:i*2+2], font_height=font_bits))
                if i % 16 == 0:
                    fout_txt.write("0x%04x " % i)
                fout_txt.write(chars_utf8[i])
                fout_txt.write(" ")
                if (i + 1) % 16 == 0:
                    fout_txt.write("\n")
        fout_txt.write("\n")
    
    # print the result of characters map and output file
    with open(output_txt, "r") as fin_txt:
        print(fin_txt.read())
    print("Output bin: {}, map file: {}".format(output_bin, output_txt))

if __name__ == '__main__':
    main()
