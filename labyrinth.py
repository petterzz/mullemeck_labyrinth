import pyglet, serial
from pyglet.window import key
from game import resources, board, servo, ball, controller, target

# Set up a window
game_window = pyglet.window.Window(1024, 768)

# Batch for graphics objects
main_batch = pyglet.graphics.Batch()

# Initialize board object
board = board.Board(350, 350, batch=main_batch)

# Initialize ball
ball = ball.Ball(board, mass=0.005, batch=main_batch)

# Initialize target
target = target.Target(board, batch=main_batch)

# Initialize servos
servo_x = servo.Servo()
servo_y = servo.Servo()

# Initialize controller
controller = controller.Controller([-50, 50], servo_x, servo_y, ball, target)

# Add stuff to key event stack
game_window.push_handlers(target)
game_window.push_handlers(controller.key_handler)

# Initialize text labels
text_ball_position_x = pyglet.text.Label("Ball position X: ",
                                    x = 20, y = game_window.height - 20,
                                    font_name='consolas', batch=main_batch)
text_ball_position_y = pyglet.text.Label("Ball position Y: ",
                                    x = 300, y = game_window.height - 20,
                                    font_name='consolas', batch=main_batch)
text_ball_velocity_x = pyglet.text.Label("Ball velocity X: ",
                                    x = 20, y = game_window.height - 40,
                                    font_name='consolas', batch=main_batch)
text_ball_velocity_y = pyglet.text.Label("Ball velocity Y: ",
                                    x = 300, y = game_window.height - 40,
                                    font_name='consolas', batch=main_batch)
text_target_position_x = pyglet.text.Label("Target position X: ",
                                    x = 20, y = game_window.height - 60,
                                    font_name='consolas', batch=main_batch)
text_target_position_y = pyglet.text.Label("Target position Y: ",
                                    x = 300, y = game_window.height - 60,
                                    font_name='consolas', batch=main_batch)
text_dist_x = pyglet.text.Label("Distance to target X: ",
                                    x = 20, y = game_window.height - 80,
                                    font_name='consolas', batch=main_batch)
text_dist_y = pyglet.text.Label("Distance to target Y: ",
                                    x = 300, y = game_window.height - 80,
                                    font_name='consolas', batch=main_batch)

# All game objects to be updated together
game_objects = [board] + [ball] + [servo_x] + [servo_y] + [controller] + [target]

serial = serial.Serial('/dev/ttyACM0', 115200)



def update(dt):
    for obj in game_objects:
        obj.update(dt)
    board.x_rotation = servo_x.position_state
    board.y_rotation = servo_y.position_state

def send_serial(dt):
    # send servo control messages
    #print "x" + str(int(board.x_rotation)) + "y" + str(int(board.y_rotation)) + "_"
    serial.write("x" + str(int(board.x_rotation)) + "y" + str(int(board.y_rotation)) + "_")


def on_key_press(symbol, modifiers):
    # send calibration messages
    if symbol == key.A:
        serial.write("cx-1")
    elif symbol == key.D:
        print "D"
        serial.write("cx1")
    elif symbol == key.S:
        serial.write("cy-1")
    elif symbol == key.W:
        serial.write("cy1")
game_window.push_handlers(on_key_press)

@game_window.event
def on_draw():
    # update text labels
    text_ball_position_x.text = "Ball position X: " + str(int(ball.x - board.x))
    text_ball_position_y.text = "Ball position Y: " + str(int(ball.y - board.y))
    text_ball_velocity_x.text = "Ball velocity X: " + str(int(ball.velocity_x))
    text_ball_velocity_y.text = "Ball velocity Y: " + str(int(ball.velocity_y))
    text_target_position_x.text = "Target position X: " + str(int(target.x - board.x))
    text_target_position_y.text = "Target position Y: " + str(int(target.y - board.y))
    text_dist_x.text = "Distance to target X: " + str(int(controller.distToTarget_x))
    text_dist_y.text = "Distance to target Y: " + str(int(controller.distToTarget_y))
    game_window.clear()

    main_batch.draw()
    ball.draw()
    target.draw()



if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/100.0)
    pyglet.clock.schedule_interval(send_serial, 1/100.0)
    pyglet.app.run()
