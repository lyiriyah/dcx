#!/usr/bin/env python3

import readline, time, sys, math
from collections import OrderedDict, deque

def _help():
    print("""dcx: dc but in python and probably a bit worse
    +, -, /, *, and % do what you expect them to.
    ~ is equivalent to divmod(stack.pop(-2), stack.pop(-1))
    p prints the first member of the stack without modifying it
    f prints the whole stack
    F prints all of the registers
    c clears the stack
    C clears the registers
    sN pops the first value from the stack and stores it in register N
    lN copies the value in register N and pushes it to the stack
    h prints this help
    q exits the program""".replace("    ", ""))

try:
    if sys.argv[1] in ["h", "--help", "-h", "cockwomble"]:
        _help()
        exit(0)
except IndexError: pass

readline.parse_and_bind("")

stack = []

registers = OrderedDict()

def get_regs(registers):
    for i, j in registers.items(): print(f"{i}: {j}")

while 1:
    get_stack_member = lambda n, msg: f"{stack[-n]} " if stack != [] else msg
    uinput = input(f"{get_stack_member(1, '')}> ")
    is_number = True

    try: float(uinput)
    except ValueError: is_number = False

    try:
        if uinput == "" or uinput.isspace(): continue
        elif is_number: stack.append(float(uinput))
        elif uinput == "+": stack.append(stack.pop() + stack.pop())
        elif uinput == "-": stack.append(stack.pop(-2) - stack.pop(-1))
        elif uinput == "*": stack.append(stack.pop() * stack.pop())
        elif uinput == "/":
            try: stack.append(stack.pop(-2) / stack.pop(-1))
            except ZeroDivisionError: print("Division by zero!")
        elif uinput == "%": stack.append(stack.pop(-2) % stack.pop(-1))
        elif uinput == "~":
            try: stack.extend(divmod(stack.pop(-2), stack.pop(-1)))
            except ZeroDivisionError: print("Division by zero!")
        elif uinput == "^": stack.append(stack.pop(-2) ** stack.pop(-1))
        elif uinput == "v": stack.append(math.log(stack.pop(-2), stack.pop(-1)))
        elif uinput == "&": stack.append(stack.pop(-2) ** (1/stack.pop(-1)))
        elif uinput == "p": stack.append(math.pi)
        elif uinput == "e": stack.append(math.e)
        elif uinput == "f":
            for i, v in enumerate(stack[::-1]):
                print(f"{i}: {v}") if stack != [] else print("dcx: stack empty")
        elif uinput == "F": get_regs(registers)
        elif uinput == "c": stack.clear()
        elif uinput == "C": registers.clear()
        elif uinput == "h": _help()
        elif uinput[0] == "s":
            if str(uinput[1::]) != None:
                    if stack != []:
                        registers[str(uinput[1::])] = stack.pop()
                    else: print("dcx: stack empty")
        elif uinput[0] == "l": stack.append(registers.get(uinput[1]))
        elif uinput == "r": stack[-1], stack[-2] = stack[-2], stack[-1]
        elif uinput[0] == "R": stack = [stack.pop()].extend(stack)
        elif uinput == "q": exit(0)
        else: print(f"dcx: {uinput} unimplemented")
    except IndexError as e:
        error = str(e).replace("list", "stack")
        print(f"dcx: {error}")
