import sys
from textx import metamodel_from_file
from karel_robot.run import *

robot_mm = metamodel_from_file('karel.tx')


robot_model = robot_mm.model_from_file("maze.karel")

def is_(o, name):
    return o.__class__.__name__ == name

class Robot(object):

    DEFAULT_CTX = {'break':False}

    def __init__(self):
        self.ctx = [dict(Robot.DEFAULT_CTX)]

    def process_command(self, s):
        if is_(s, 'Turn'):
            if s.where == 'left':
                turn_left()
            if s.where == 'right':
                turn_right()

        if s == 'move':
            move()
        if s == 'exit':
            exit()
        if s == 'break':
            self.ctx[-1]['break'] = True

        if is_(s, 'Beeper'):
            if s.action == 'pick':
                pick_beeper()
            if s.action == 'put':
                put_beeper()

        if is_(s, 'SubCall'):
            self.call_sub(s.name, s.param)


    def call_sub(self, s, ps):
        self.ctx += [dict(Robot.DEFAULT_CTX)]
        
        for i, p in enumerate(ps):
            self.ctx[-1][vars(self)[s.name][0][i]] = p

        self.process_statements(vars(self)[s.name][1])

        self.ctx = self.ctx[:-1]

    def process_definition(self, d):
        if is_(d, 'Procedure'):
            vars(self)[d.name] = (d.param, d.commands)

    def process_expression(self, e):
        # Check
        if e == 'front_is_treasure':
            return front_is_treasure()
        if e == 'front_is_blocked':
            return front_is_blocked()
        
        # Dir
        if e == 'north':
            return facing_north()
        if e == 'south':
            return facing_south()
        if e == 'west':
            return facing_west()
        if e == 'east':
            return facing_east()

        # Beeper
        if e == 'is_beeper':
            return beeper_is_present()

        
        if is_(e, 'Or'):
            return self.process_expression(e.left) \
                    or self.process_expression(e.right)
        
        if is_(e, 'And'):
            return self.process_expression(e.left) \
                    and self.process_expression(e.right)
        
        if is_(e, 'Not'):
            return not self.process_expression(e.expr)

        # Var
        if is_(e, 'Var'):
            return self.process_expression(self.ctx[-1][e.expr])

    def process_statements(self, cs):
        for c in cs:
            self.process_statement(c)

            if self.ctx[-1]['break']:
                break            

    def process_statement(self, s):
        if self.ctx[-1]['break']:
            return 

        self.process_definition(s)
        self.process_command(s)

        if is_(s, 'StatementWhile'):
            while self.process_expression(s.cond):
                self.process_statements(s.commands)
                
                if self.ctx[-1]['break']:
                    self.ctx[-1]['break'] = False
                    break
        
        if is_(s, 'StatementIf'):
            if self.process_expression(s.cond):
                self.process_statements(s.commands)
            else:
                self.process_statements(s.else_commands)



    def interpret(self, model):

        for s in model.commands:
            self.process_statement(s)


robot = Robot()
robot.interpret(robot_model)