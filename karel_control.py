import sys
from textx import metamodel_from_file
from karel_robot.run import *

robot_mm = metamodel_from_file('karel.tx')


robot_model = robot_mm.model_from_file("maze.karel")

def is_(o, name):
    return o.__class__.__name__ == name

class Robot(object):

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

        if is_(s, 'Beeper'):
            if s.action == 'pick':
                pick_beeper()
            if s.action == 'put':
                put_beeper()


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


    def process_statements(self, cs):
        for c in cs:
            self.process_statement(c)
       

    def process_statement(self, s):
        self.process_command(s)

        if is_(s, 'StatementWhile'):
            while self.process_expression(s.cond):
                self.process_statements(s.commands)

        
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