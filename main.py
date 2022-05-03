import pygame, sys, random, math

width = height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Elastic collisions")
clock = pygame.time.Clock()

def distanceTo(a, b):
	distance = math.sqrt(((a.x - b.x) * (a.x - b.x)) + ((a.y - b.y) * (a.y - b.y)))
	if (distance < 0): distance = distance * -1
	return distance

def drawCollision(firstBall, secondBall):
	x1 = firstBall.x
	x2 = secondBall.x
	y1 = firstBall.y
	y2 = secondBall.y
	r1 = firstBall.radius
	r2 = secondBall.radius

	collisionPoint = pygame.math.Vector2((x1 * r2 + x2 * r1) / (r1 + r2), (y1 * r2 + y2 * r1) / (r1 + r2))

	pygame.draw.circle(win, (0, 0, 255), (collisionPoint.x, collisionPoint.y), 5)

def calculateNewVelocities(firstBall, secondBall):
	mass1 = firstBall.radius
	mass2 = secondBall.radius
	velX1 = firstBall.motion.x
	velX2 = secondBall.motion.x
	velY1 = firstBall.motion.y
	velY2 = secondBall.motion.y

	newVelX1 = (velX1 * (mass1 - mass2) + (2 * mass2 * velX2)) / (mass1 + mass2)
	newVelX2 = (velX2 * (mass2 - mass1) + (2 * mass1 * velX1)) / (mass1 + mass2)
	newVelY1 = (velY1 * (mass1 - mass2) + (2 * mass2 * velY2)) / (mass1 + mass2)
	newVelY2 = (velY2 * (mass2 - mass1) + (2 * mass1 * velY1)) / (mass1 + mass2)
	# trace (velX1 * (mass1 - mass2) )
	# trace (2 * mass2 * velX2)
	# trace(newVelX1)
	# s = 0 / 20
	# trace(s)

	firstBall.motion.x = newVelX1
	secondBall.motion.x = newVelX2
	firstBall.motion.y = newVelY1
	secondBall.motion.y = newVelY2

	firstBall.x = firstBall.x + newVelX1
	firstBall.y = firstBall.y + newVelY1
	secondBall.x = secondBall.x + newVelX2
	secondBall.y = secondBall.y + newVelY2;

class Ball:
	def __init__(self, rad):
		self.x = random.randint(rad, width - rad)
		self.y = random.randint(rad, height - rad)
		self.radius = rad
		self.motion = pygame.math.Vector2(random.randint(-5, 5), random.randint(-5, 5))
		self.mass = self.radius

	def update(self, win):
		self.x += self.motion.x
		self.y += self.motion.y
		if self.x - self.radius <= 0 or self.x + self.radius >= width:
			self.motion.x = -self.motion.x
		if self.y - self.radius <= 0 or self.y + self.radius >= height:
			self.motion.y = -self.motion.y

		pygame.draw.circle(win, (0, 0, 0), (self.x, self.y), self.radius)

firstBall = Ball(random.randint(20, 40))
secondBall = Ball(random.randint(20, 40))

while True:
	clock.tick(60)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()

	win.fill('white')
	firstBall.update(win)
	secondBall.update(win)
	if (firstBall.x + firstBall.radius + secondBall.radius > secondBall.x
	and firstBall.x < secondBall.x + firstBall.radius + secondBall.radius
	and firstBall.y + firstBall.radius + secondBall.radius > secondBall.y
	and firstBall.y < secondBall.y + firstBall.radius + secondBall.radius):
		if (distanceTo(firstBall, secondBall) < firstBall.radius + secondBall.radius):
			drawCollision(firstBall, secondBall)
			calculateNewVelocities(firstBall, secondBall)
	pygame.display.update()
