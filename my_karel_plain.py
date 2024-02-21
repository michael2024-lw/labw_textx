from textx import metamodel_from_file
from karel_robot.run import *

def classNameOf(obj):
    return obj.__class__.__name__ 

def handleCmd(cmd):
    if classNameOf(cmd) == 'Turn':
        if cmd.where == 'left':
            turn_left()
        if cmd.where == 'right':
            turn_right()

    if classNameOf(cmd) == 'Beeper':
        if cmd.action == 'pick':
            pick_beeper()
        if cmd.action == 'put':
            put_beeper()

    if cmd == 'move':
        move()
    if cmd == 'exit':
        exit()

def run(ast):
    for node in ast.commands:
        handleCmd(node)

language_model = metamodel_from_file('karel-plain.tx')
ast = language_model.model_from_file("maze-plain.karel")

run(ast)

