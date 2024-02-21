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


def handleExpression(exp):
    if classNameOf(exp) == 'Or':
        return handleExpression(exp.left) or handleExpression(exp.right) # lazy execution
    
    if classNameOf(exp) == 'And':
        return handleExpression(exp.left) and handleExpression(exp.right) # lazy execution
    
    if classNameOf(exp) == 'Not':
        return not handleExpression(exp.expr)
    
    if exp == 'front_is_treasure':
        return front_is_treasure()
    if exp == 'front_is_blocked':
        return front_is_blocked()

    if exp == 'north':
        return facing_north()
    if exp == 'south':
        return facing_south()
    if exp == 'west':
        return facing_west()
    if exp == 'east':
        return facing_east()

    if exp == 'is_beeper':
        return beeper_is_present()


def handleStatement(stmt):
    handleCmd(stmt)
    
    if classNameOf(stmt) == 'StatementFor':
        for _ in range(stmt.times_count):
            traverseStatements(stmt.commands)

    if classNameOf(stmt) == 'StatementWhile':
        while handleExpression(stmt.cond):
            traverseStatements(stmt.commands)
    
    if classNameOf(stmt) == 'StatementIf':
        if handleExpression(stmt.cond):
            traverseStatements(stmt.commands)
        else:
            traverseStatements(stmt.else_commands)


def traverseStatements(stmts):
    for stmt in stmts:
        handleStatement(stmt)


def run(ast):
    for cmd in ast.commands:
        handleStatement(cmd)


language_model = metamodel_from_file('karel-control.tx')
ast = language_model.model_from_file("maze.karel")

run(ast)
