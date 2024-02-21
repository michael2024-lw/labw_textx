from collections import deque
from textx import metamodel_from_file
from karel_robot.run import *


class KarelInterpreter(object):
    __EMPTY_CONTEXT = {'break':False}
    __stack = deque()
    __procedures_defines = {}

    def __classNameOf(self, obj):
        return obj.__class__.__name__ 

    def __init__(self):
        self.__stack.append(KarelInterpreter.__EMPTY_CONTEXT)

    def __handleCmd(self, cmd):
        if self.__classNameOf(cmd) == 'Turn':
            if cmd.where == 'left':
                turn_left()
            if cmd.where == 'right':
                turn_right()

        if self.__classNameOf(cmd) == 'Beeper':
            if cmd.action == 'pick':
                pick_beeper()
            if cmd.action == 'put':
                put_beeper()

        if self.__classNameOf(cmd) == 'SubCall':
            self.__callProcedure(cmd.name, cmd.param)

        if cmd == 'move':
            move()
        if cmd == 'exit':
            exit()
        if cmd == 'break':
            self.__stack[-1]['break'] = True


    def __callProcedure(self, nameObj, args):
        self.__stack.append(KarelInterpreter.__EMPTY_CONTEXT)
        
        for idx, arg in enumerate(args):
            self.__stack[-1][self.__procedures_defines[nameObj.name][0][idx]] = arg

        self.__traverseStatements(self.__procedures_defines[nameObj.name][1])

        self.__stack.pop()


    def __handleExpression(self, exp):
        if self.__classNameOf(exp) == 'Var':
            return self.__handleExpression(self.__stack[-1][exp.expr])

        if self.__classNameOf(exp) == 'Or':
            return self.__handleExpression(exp.left) or self.__handleExpression(exp.right)
        
        if self.__classNameOf(exp) == 'And':
            return self.__handleExpression(exp.left) and self.__handleExpression(exp.right)
        
        if self.__classNameOf(exp) == 'Not':
            return not self.__handleExpression(exp.expr)
        
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
      
    
    def __handleStatement(self, stmt):
        if self.__stack[-1]['break']:
            return 

        if self.__classNameOf(stmt) == 'Procedure':
            self.__procedures_defines[stmt.name] = (stmt.param, stmt.commands) # [Str], [Any]

        self.__handleCmd(stmt)

        if self.__classNameOf(stmt) == 'StatementFor':
            for _ in range(stmt.times_count):
                self.__traverseStatements(stmt.commands)

                if self.__stack[-1]['break']:
                    self.__stack[-1]['break'] = False
                    break
        
        if self.__classNameOf(stmt) == 'StatementWhile':
            while self.__handleExpression(stmt.cond):
                self.__traverseStatements(stmt.commands)
                
                if self.__stack[-1]['break']:
                    self.__stack[-1]['break'] = False
                    break
        
        if self.__classNameOf(stmt) == 'StatementIf':
            if self.__handleExpression(stmt.cond):
                self.__traverseStatements(stmt.commands)
            else:
                self.__traverseStatements(stmt.else_commands)


    def __traverseStatements(self, stmts):
        for stmt in stmts:
            self.__handleStatement(stmt)

            if self.__stack[-1]['break']:
                break            


    def run(self, ast):
        for stmt in ast.commands:
            self.__handleStatement(stmt)


language_model = metamodel_from_file('karel-structured.tx')
ast = language_model.model_from_file("maze-procedure.karel")

robot = KarelInterpreter()
robot.run(ast)
