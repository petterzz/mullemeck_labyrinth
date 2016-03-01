import pyglet
pyglet.resource.path = ['resources']
pyglet.resource.reindex()



board_topview_image = pyglet.resource.image("boardtopview.png")
board_sideview_image = pyglet.resource.image("boardsideview.png")
ball_image = pyglet.resource.image("ball.png")
asteroid_image = pyglet.resource.image("asteroid.png")
target_image = pyglet.resource.image("target.png")

def center_image(image):
	"""Sets an image's anchor point to its center"""
	image.anchor_x = image.width/2
	image.anchor_y = image.height/2

center_image(board_topview_image)
center_image(ball_image)
center_image(asteroid_image)
center_image(target_image)
board_sideview_image.anchor_x = board_sideview_image.width / 2
board_sideview_image.anchor_y = board_sideview_image.height / 2
