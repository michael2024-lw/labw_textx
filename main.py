from textx import metamodel_from_file

def move_command_processor(move_cmd):

  # If steps is not given, set it do default 1 value.
  if move_cmd.steps == 0:
    move_cmd.steps = 1

robot_mm = metamodel_from_file('robot.tx')
robot_mm.register_obj_processors({'MoveCommand': move_command_processor})


robot_model = robot_mm.model_from_file('example.robot')

class Robot(object):

  def __init__(self, initial):
    # Initial position is (0,0)
    self.x = initial.x
    self.y = initial.y

  def __str__(self):
    return "Robot position is {}, {}.".format(self.x, self.y)

  def interpret(self, model):

    # model is an instance of Program
    print("Starting from position: {}, {}".format(self.x, self.y))

    for c in model.moves:
        dir = c.direction
        print("Going {} for {} step(s).".format(dir, c.steps))

        move = {
            "up": (0, 1),
            "down": (0, -1),
            "left": (-1, 0),
            "right": (1, 0)
        }[dir]

        # Calculate new robot position
        self.x += c.steps * move[0]
        self.y += c.steps * move[1]

        print(self)


robot = Robot(robot_model.initial)
robot.interpret(robot_model)