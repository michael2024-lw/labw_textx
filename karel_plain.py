from textx import metamodel_from_file
from karel_robot.run import *

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


    def process_statements(self, cs):
        for c in cs:
            self.process_statement(c)


    def process_statement(self, s):
        self.process_command(s)


    def interpret(self, model):

        for s in model.commands:
            self.process_statement(s)

robot_mm = metamodel_from_file('karel-plain.tx')
robot_model = robot_mm.model_from_file("maze-plain.karel")

robot = Robot()
robot.interpret(robot_model)

