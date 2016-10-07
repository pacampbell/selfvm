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

class IRInstr(object):
    '''Intermediate representation of an instruction'''
    def __init__(self, bincode, size, needs_patch=False, label=None):
        self.bincode = bincode
        self.size = size
        self._meta = {
            'needs_patch': needs_patch,
            'label': label
        }
        # Do a sanity check to make sure valid arguments were given
        if needs_patch and label == None:
            raise Exception('Cannot have a null label when a patch is needed')

    def needs_patch(self):
        return self._meta['needs_patch']

    def patch(self, table):
        '''Patches jump address or relative offset into instruction.'''
        if not self.needs_patch:
            raise Exception('Attempting to patch an instruction that doesn\'t need a patch')
        # Lets patch up the instruction so its valid
        pass


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
    # args: RD, RS, RT, SHAMT, IMM
    ir_instr = None
    if mapping['size'] == 1:
        ir_instr = create1(mapping, arguments)
    elif mapping['size'] == 2:
        ir_instr = create2(mapping, arguments)
    elif mapping['size'] == 3:
        ir_instr = create3(mapping, arguments)
    elif mapping['size'] == 4:
        ir_instr = create4(mapping, arguments)
    else:
        print('Unsupported instruction mapping: {}'.format(mapping))
    return ir_instr


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
    return IRInstr(bincode=instruction, size=1)

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
    return IRInstr(bincode=instruction, size=2)


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
    return IRInstr(bincode=instruction, size=3)

def create4(mapping, arguments):
    '''
    opcode = `11110xxx`
    +--------+--------+--------+--------+-----------+-----------+
    | 5-bits | 3-bits | 4-bits | 4-bits | 8-bits    | x-bytes   |
    +--------+--------+--------+--------+-----------+-----------+
    | marker | opcode | rd     | rs     | fmt       | immediate |
    +--------+--------+--------+--------+-----------+-----------+

    fmt values:
    +--------+---------------+
    | 4-bits | 4-bits        |
    +--------+---------------+
    | size   | encoding      |
    +--------+---+---+---+---+
    | bbbb   | S | 1 | R | 2 |
    +--------+---+---+---+---+
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
    imm = 0
    # TODO: Default values
    size = 4          # Default to four bytes
    encoding = 0 # Default to two's complement

    for (reg,field) in zip(registers, mapping['args']):
        reg = reg.strip()
        field = field.strip()
        # print('reg: {}, field: {}'.format(reg, field))
        if field == 'RD':
            rd = Types.reg_to_num(reg)
        elif field == 'RS':
            rs = Types.reg_to_num(reg)
        elif field == 'IMM':
            imm = int(reg)
        else:
            print('Invalid field for a 2-byte encoding.')
    # Build the final instruction
    instruction = (opcode << 16) | (0xf & rd) << 12 | (0xf & rs) << 8 | (0xff & encoding)
    # Now make space for the value
    instruction = (instruction << 32) | imm
    # Print the instruction hex value
    print('0x{:08x}'.format(instruction))
    return IRInstr(bincode=instruction, size=7)

def main(args):
    with open(args.source_file, 'r') as source_file, open(args.instruction_set, 'r') as is_set:
        # Get a list of the instructions
        instruction_set = json.load(is_set)
        # pprint(instruction_set)
        # Make a mapping of labels to patch
        lookup_table = {}
        ir_list = []
        # Start parsing the source file
        src_lineno = 1
        rel_offset = 0
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
                    # Get rid of the colon
                    mline = mline[:mline.index(':')]
                    print('Found label: \'{}\''.format(mline))
                    # Add to lookup table for second pass
                    if mline not in lookup_table:
                        lookup_table[mline] = rel_offset
                    else:
                        # This is wrong, multiple labels defined in same pgm
                        print('Line{}: Multiple occurrances of label {}.. exiting'.format(mline))
                        sys.exit(1)
                elif mline.find('.') > -1:
                    # TODO: Handle a .text or .data directive
                    print('Found directive: \'{}\''.format(mline))
                else:
                    # Have a possible instruction
                    parts = mline.split(' ', 1)
                    mnemonic = parts[0].strip()
                    body = None
                    if len(parts) > 1:
                        body = parts[1].strip()
                    if mnemonic not in instruction_set:
                        print('Line {}: mnemonic \'{}\' does not exist.. exiting'.format(src_lineno, mnemonic))
                        sys.exit(1)
                    # We found the instruction lets validate it and build it
                    ir_instr = create(instruction_set[mnemonic], body)
                    if ir_instr == None:
                        # Decoded some invalid instruction
                        print('Exiting..')
                        sys.exit(1)
                    # print('{}: {}'.format(lineno, mline))
                    # Increment the relative offset
                    rel_offset = rel_offset + ir_instr.size
                    # Add the instruction for the second pass
                    ir_list.append(ir_instr)
            # Increment the line number
            src_lineno = src_lineno + 1
        # DEBUG: Print the lookup table
        print(lookup_table)
        # TODO: Begin second pass over intermediate code and patch labels and gen code
        for instr in ir_list:
            if instr.needs_patch:
                instr.patch(lookup_table)
            # Instruction is completed, write instruction to file
            print('0x{:x}'.format(instr.bincode))


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
