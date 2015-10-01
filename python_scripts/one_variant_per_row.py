"""this script takes a vcf file, read each row, if the ALT field contains more than 
one item, it will create multiple variant row based on that row
"""

import vcf
import sys
import argparse
from copy import deepcopy

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input")
    parser.add_argument("-o", "--output")
    args = parser.parse_args()
    return args


def main():
    args = arg_parse()
    vcf_reader = vcf.Reader(open(args.input, "r"), strict_whitespace=True)
    vcf_writer = vcf.Writer(open(args.output, 'w'), vcf_reader)
    write_err = 0

    for record in vcf_reader:
        n = len(record.ALT)
        if n == 1:
            vcf_writer.write_record(record)
        else:
            for i in range(n):
                new_record = deepcopy(record) 
                new_record.ALT = [record.ALT[i]]
                for key in record.INFO.keys():
                    value = record.INFO[key]
                    if type(value) == list and len(value) == n:
                        new_record.INFO[key] = [value[i]]
                try:
                    vcf_writer.write_record(new_record)
                except:
                    write_err += 1
    print "number of vcf_write.write_record() error is: ", write_err

if __name__=="__main__":
    main()