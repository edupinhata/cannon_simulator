                                                        #Author: Eduardo Pinhata
                                                        #Seat: 06
#Program that implements a cannon shooting
from tkinter import *
import math


#variables
wheel_radius = 10
cannon_length = 50
cannon_width = 15
width = 800
height = 600
FLOOR = 500
sleepTime = 10
DETAIL_RATE = 100
GRAVITY_ACELERATION = 10


class Cannon:


	#constructor that initialize the cannon in a position x and y
	#angle is the position where the cannon will be aiming
	def __init__(self, x_init, y_init, angle, canvas):
		if angle <=90 and angle >=0:
			self.angle = angle
		else:
			self.angle = 45
		self.x = x_init
		self.y = y_init
		self.cannon_hor = [self.x + 0, self.y -wheel_radius, self.x + 0, self.y -(wheel_radius + cannon_width), self.x + cannon_length, self.y -(cannon_width+ wheel_radius), self.x + cannon_length, self.y -wheel_radius] 
		self.sheft = self.cannon_hor  #cannon in the horizontal position
		self.canvas = canvas
		print("Cannon created")

	def setAngle(self, newAngle):
		if newAngle <= 90 and angle >= 0:
			self.angle = newAngle

	def getAngle(self):
		return self.angle

	def draw(self):
		self.canvas.delete("cannon")
		self.canvas.create_oval(self.x-10, self.y, self.x+10, self.y - 20, width=2, fill='black', tag="cannon") #draw the wheel
		self.canvas.create_polygon(self.sheft, outline='black', fill='grey', width=2, tag="cannon")  #draw sheft
		
	#function with debugging objectives
	def printPoints(self):
		print('angle =', self.angle)
		for i in range(0, len(self.sheft),2):
			print('x=',self.sheft[i],'| y =', self.sheft[i+1])

	def rotateSheft(self, angleRot):
		if self.angle + angleRot >=0 and self.angle + angleRot <=90:

			alpha = math.radians(angleRot) #angle to calculate third and 4th point
			self.angle += angleRot
			
			#define rotation matrix
			rotation_matrix = []
			
			#store the initial points
			x_init = self.sheft[0]
			y_init = self.sheft[1]

			for i in range(0, len(self.sheft), 2):
				self.sheft[i] -= x_init
				self.sheft[i+1] = -(y_init - self.sheft[i+1]) 

			#use the image rotation to rotate the polygon
			#x* = x.cos(alpha) + y.sin(alpha)
			#y* = -x.sin(alpha) + y.cos(alpha)
			for i in range(0,len(self.sheft),2):
				self.sheft[i] = (self.sheft[i])*math.cos(alpha) + (self.sheft[i+1])*math.sin(alpha)
				self.sheft[i+1] = -(self.sheft[i])*math.sin(alpha) + (self.sheft[i+1])*math.cos(alpha)
				

			#sum again the x + wheel to put picture on the right place
			for i in range(0, len(self.sheft), 2):
				self.sheft[i] += x_init
				self.sheft[i+1] = self.sheft[i+1] + y_init 

			self.printPoints()
		
		
class Bullet:
	def __init__(self, x_init, y_init, angle, canvas, speed):
		self.x = x_init  #x position that the bullet will start
		self.y = y_init  #y position that the bullet will start
		self.angle = angle  #angle that the bullet will start move
		self.canvas = canvas  #canvas to draw the bullet
		self.speed = speed  #speed that the bullet has
		self.speed_init = speed  #initial speed

	def draw(self):
		self.canvas.delete("bullet")
		self.canvas.create_oval(self.x-5,self.y+5,self.x+5,self.y-5, fill='black', tag="bullet")

	def moveX(self, speed, angle, time):
		return speed*math.cos(math.radians(angle))*time  #uniform moviment

	def moveY(self, speed, angle, time):
		return -speed*math.sin(math.radians(angle))*time + (GRAVITY_ACELERATION*time**2)/2  #uniform moviment

	#return initial y_speed
	def speedYInit(self):
		return self.speed_init*math.sin(math.radians(self.angle))

	#return y speed in a give moment
	def speedY(self, y_speed_ini, angle, space):
		return math.sqrt((-y_speed_ini)**2 + 2*GRAVITY_ACELERATION*space)

		#return x speed
	def speedX(self, speed, angle):
		return speed*math.cos(math.radians(angle))

	def getSpeedAngle(self, x_speed, y_speed):
		return math.degrees(math.acos(x_speed/math.sqrt(x_speed**2 + y_speed**2)))

	def getSpeedComposed(self, x_speed, y_speed):
		return math.sqrt(x_speed**2 + y_speed**2)

	def shoot(self):
		#initialize variables
		time = 1
		y_ini  = self.y #track the last y that will begin with the initial position
		y_speed = self.speedYInit()  #get the initial speed and start to track it
		x_speed = self.speedX(self.speed, self.angle)

		#draw the bullet on its initial position
		self.draw()

		#loop that simulate the bullet flighing
		while True:
			#calculate new x and y
			self.x += self.moveX(self.speed, self.angle, time)/DETAIL_RATE
			self.y += self.moveY(self.speed, self.angle, time)/DETAIL_RATE
			y_speed = self.speedY(y_speed, self.getSpeedAngle(x_speed, y_speed), self.y - y_ini)
			print('yspeed =', y_speed, '| speed=', self.speed, '| y=', format(self.y,'.2f'), '| y_ini=', format(y_ini,'.2f'), '| dif=', format(self.y-y_ini,'.2f'))
			y_ini = self.y			
			self.draw()
			self.canvas.focus_set()
			self.canvas.after(sleepTime)
			self.canvas.update()
			time += 1 	#update time
			
			if (self.y + self.moveY(self.speed, self.angle, time)/DETAIL_RATE > FLOOR and y_speed < 10) or self.x > width:
				break
			#condition to invert movement
			elif self.y + self.moveY(self.speed, self.angle, time)/DETAIL_RATE > FLOOR:
				print('entrou')
				x_speed *= 0.75
				y_speed *= 0.40
				self.speed = self.getSpeedComposed(x_speed, y_speed)
				self.angle = self.getSpeedAngle(x_speed, y_speed)
				time = 1





class Game:
	
	def __init__(self):
		window = Tk()  #create window
		window.title("Cannon simulator")


		#set variables
		self.sleepTime = 100
		

		#setup canvas
		self.canvas = Canvas(window, bg='white', width = width, height = height)
		self.canvas.pack()

		#draw floor
		self.canvas.create_line(0, FLOOR, width, FLOOR, width=2)

		#create an instance of cannon
		self.cannon = Cannon(100, FLOOR, 0, self.canvas)
		self.cannon.draw()

		#Bind the arrow keys to a procedure
		window.bind("<Up>", self.rotateSheftUp)
		window.bind("<Down>", self.rotateSheftDown)
		window.bind("<Right>", self.shoot)


		window.mainloop()

	def rotateSheftUp(self, event):
		self.cannon.rotateSheft(5)
		self.cannon.draw()
		self.canvas.focus_set()
		self.canvas.update()

	def rotateSheftDown(self, event):
		self.cannon.rotateSheft(-5)
		self.cannon.draw()
		self.canvas.focus_set()
		self.canvas.update()


	def printSomething(self, event):
		print('Testing')

	def shoot(self, event):
		print('Shoot')
		bullet = Bullet(self.cannon.sheft[6]-5, self.cannon.sheft[7]-5, self.cannon.getAngle(), self.canvas, 10*DETAIL_RATE/7)
		print('bullet x=', bullet.x, '| bullet y=', bullet.y)
		bullet.shoot()

Game()
