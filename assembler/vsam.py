#!/usr/bin/env python3
"""
Toy implementation of an assembler for VMLANG. VMLANG is specified in the
specifications directory of this repository.

@author Paul Campbell
"""
import argparse
import json
import re
import sys

from pprint import pprint

register_set = ['zero', 'at', 'sp', 'fp', 'pc', 'ra', 'v0', 'v1', 'g0', 'g1',
                'g2', 'g3', 'g4', 'g5', 'g6', 'g7']

class Types(object):
    def __init__(self):
        raise Exception('Do not instantiate an instance of this class.')

    @staticmethod
    def is_reg(val):
        valid = True
        if val[0] != '$':
            valid = False
        # TODO: Add more checks
        return valid

    @staticmethod
    def is_immed(val):
        pass

    @staticmethod
    def is_shamt(val):
        pass

    @staticmethod
    def reg_to_num(val):
        num = -1
        index = 0
        if val[0] == '$':
            val = val[1:]
        for i in range(0, len(register_set)):
            if val == register_set[i]:
                num = i
                break
        return num

def create(mapping, arguments):
    # mnemonic: name
    # size: in bytes
    # opcode: binary value
    # args: RD, RS, RT, SHAMT, IMM16
    if mapping['size'] == 1:
        create1(mapping, arguments)
    elif mapping['size'] == 2:
        create2(mapping, arguments)
    elif mapping['size'] == 3:
        create3(mapping, arguments)
    elif mapping['size'] == 4:
        create4(mapping, arguments)
    else:
        print('Unsupported instruction mapping: {}'.format(mapping))


def create1(mapping, arguments):
    '''
    first byte = `0xxxxxxx`
    +--------+--------+
    | 1-bit  | 7-bits |
    +--------+--------+
    | marker | opcode |
    +--------+--------+
    '''
    instruction = 0x7f & int(mapping['opcode'], 2)
    print('0x{:02x}'.format(instruction))

def create2(mapping, arguments):
    '''
    first byte = `110xxxxx`
    +--------+--------+--------+--------+
    | 3-bits | 5-bits | 4-bits | 4-bits |
    +--------+--------+--------+--------+
    | marker | opcode | rd     | rs     |
    +--------+--------+--------+--------+
    '''
    opcode = 0xc0 | (0x1f & int(mapping['opcode'], 2))
    registers = arguments.split(',')
    # Make sure we have the correct amount
    if len(registers) != len(mapping['args']):
        print('Incorrect number of arguments for {}'.format(mapping['mnemonic']))
    # Next we need to make sure they match
    # Types.reg_to_num
    rd = 0
    rs = 0
    for (reg,field) in zip(registers, mapping['args']):
        reg = reg.strip()
        field = field.strip()
        # print('reg: {}, field: {}'.format(reg, field))
        if field == 'RD':
            rd = Types.reg_to_num(reg)
        elif field == 'RS':
            rs = Types.reg_to_num(reg)
        else:
            print('Invalid field for a 2-byte encoding.')
    # Build the final instruction
    instruction = (opcode << 8) | (0xf & rd) << 4 | (0xf & rs)
    # Print the instruction hex value
    print('0x{:04x}'.format(instruction))



def create3(mapping, arguments):
    '''
    opcode = `1110xxxx`
    +--------+--------+--------+--------+--------+--------+
    | 4-bits | 4-bits | 4-bits | 4-bits | 4-bits | 4-bits |
    +--------+--------+--------+--------+--------+--------+
    | marker | opcode | rd     | rs     | rt     | shamt  |
    +--------+--------+--------+--------+--------+--------+
    '''
    opcode = 0xe0 | (0x0f & int(mapping['opcode'], 2))
    registers = arguments.split(',')
    # Make sure we have the correct amount
    if len(registers) != len(mapping['args']):
        print('Incorrect number of arguments for {}'.format(mapping['mnemonic']))
    # Next we need to make sure they match
    # Types.reg_to_num
    rd = 0
    rs = 0
    rt = 0
    shamt = 0
    for (reg,field) in zip(registers, mapping['args']):
        reg = reg.strip()
        field = field.strip()
        # print('reg: {}, field: {}'.format(reg, field))
        if field == 'RD':
            rd = Types.reg_to_num(reg)
        elif field == 'RS':
            rs = Types.reg_to_num(reg)
        elif field == 'RT':
            rt = Types.reg_to_num(reg)
        elif field == 'SHAMT':
            shamt = int(reg) & 0xf
        else:
            print('Invalid field for a 3-byte encoding.')
    # Build the final instruction
    instruction = (opcode << 16) | (0xf & rd) << 12 | (0xf & rs) << 8 | (0xf & rt) << 4 | shamt
    # Print the instruction hex value
    print('0x{:06x}'.format(instruction))


def create4(mapping, arguments):
    '''
    opcode = `11110xxx`
    +--------+--------+--------+--------+-----------+
    | 5-bits | 3-bits | 4-bits | 4-bits | 16-bits   |
    +--------+--------+--------+--------+-----------+
    | marker | opcode | rd     | rs     | immediate |
    +--------+--------+--------+--------+-----------+
    '''
    opcode = 0xf0 | (0x07 & int(mapping['opcode'], 2))
    registers = arguments.split(',')
    # Make sure we have the correct amount
    if len(registers) != len(mapping['args']):
        print('Incorrect number of arguments for {}'.format(mapping['mnemonic']))
    # Next we need to make sure they match
    # Types.reg_to_num
    rd = 0
    rs = 0
    imm16 = 0
    for (reg,field) in zip(registers, mapping['args']):
        reg = reg.strip()
        field = field.strip()
        # print('reg: {}, field: {}'.format(reg, field))
        if field == 'RD':
            rd = Types.reg_to_num(reg)
        elif field == 'RS':
            rs = Types.reg_to_num(reg)
        elif field == 'IMM16':
            imm16 = int(reg)
        else:
            print('Invalid field for a 2-byte encoding.')
    # Build the final instruction
    instruction = (opcode << 24) | (0xf & rd) << 20 | (0xf & rs) << 16 | imm16
    # Print the instruction hex value
    print('0x{:08x}'.format(instruction))

def main(args):
    with open(args.source_file, 'r') as source_file, open(args.instruction_set, 'r') as is_set:
        # Get a list of the instructions
        instruction_set = json.load(is_set)
        # pprint(instruction_set)
        # Start parsing the source file
        lineno = 1
        for line in source_file:
            # Remove surrounding whitespace
            mline = line.strip()
            # Next check for comments and extract them
            if mline.find('#') > -1:
                mline = line[:mline.find('#') + 1]
            mline = mline.strip()
            # If theres anything left after extracting the comment continue
            if len(mline):
                # Check for labels and direcctives
                if mline.find(':') > -1:
                    # TODO: Handle a define label
                    print('Found label: \'{}\''.format(mline))
                elif mline.find('.') > -1:
                    # TODO: Handle a .text or .data label
                    print('Found directive: \'{}\''.format(mline))
                else:
                    # Have a possible instruction
                    parts = mline.split(' ', 1)
                    mnemonic = parts[0].strip()
                    body = None
                    if len(parts) > 1:
                        body = parts[1].strip()
                    if mnemonic not in instruction_set:
                        print('Line {}: mnemonic \'{}\' does not exist.. exiting'.format(lineno, mnemonic))
                        sys.exit(1)
                    # We found the instruction lets validate it and build it
                    create(instruction_set[mnemonic], body)
                    # print('{}: {}'.format(lineno, mline))
            # Increment the line number
            lineno = lineno + 1

if __name__ == "__main__":
    # Build a list of help text to be given to the argument parser.
    help_debug = """
    Turns on debug logging statements to help with identifying and validating
    any issues that may exist in vasm.
    """

    help_source = """
    The file to be assembeled. Should have a .s extension.
    """

    help_output = """
    The name of the output file to be created. If none is given, the output file
    will be named the same as the given .s file but with a .o extension instead.
    """

    help_is = """
    A .json file containing all the instruction mappings and expected values.
    """
    # Begin creating the command line argument parser
    parser = argparse.ArgumentParser(description='vasm')
    parser.add_argument('-d', dest='debug', action='store_true', default=False, help=help_debug)
    parser.add_argument('-o', dest='output_file', type=str, default=None, help=help_output)
    parser.add_argument('-i', dest='instruction_set', type=str, default='instruction_set.json',
                        help=help_is)
    parser.add_argument('source_file', type=str, help=help_source)
    # Parse any arguments passed to the program
    args = parser.parse_args()
    # Begin the program
    sys.exit(main(args))
