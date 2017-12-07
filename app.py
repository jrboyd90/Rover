import os
import tornado.log
import tornado.ioloop
import tornado.web
import time
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import atexit
import jinja2 import Environment, PackageLoader, select_autoescape

PORT = int(os.environ.get('PORT', '8080'))

# Retrieve path where HTML lives
ENV = Environment(
    loader=PackageLoader('rover', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

mh = Adafruit_MotorHAT(addr=0x60) #CJA -Modified from 0X61

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

#motor pin setup on the Adafruit DC motor Pi Hat
motorFrontLeft = mh.getMotor(1)
motorFrontRight = mh.getMotor(2)
motorBackLeft = mh.getMotor(3)
motorBackRight = mh.getMotor(4)
interval = 1 #interval to check for key press/release - change to increase/decrease sensetivity
minSpeed = 100
maxSpeed = 200
speed = 100 #intial speed

def moveFoward(speed,runTime):
    motorBackLeft.setSpeed(speed)
    motorBackLeft.run(Adafruit_MotorHAT.FORWARD);
    motorBackRight.setSpeed(speed)
    motorBackRight.run(Adafruit_MotorHAT.FORWARD);
    motorFrontLeft.setSpeed(speed)
    motorFrontLeft.run(Adafruit_MotorHAT.FORWARD);
    motorFrontRight.setSpeed(speed)
    motorFrontRight.run(Adafruit_MotorHAT.FORWARD);
    time.sleep(runTime);#this is not required as motors are release on key release
    #turn on motor
    motorBackLeft.run(Adafruit_MotorHAT.RELEASE); #release when key is release
    motorBackRight.run(Adafruit_MotorHAT.RELEASE);
    motorFrontLeft.run(Adafruit_MotorHAT.RELEASE); 
    motorFrontRight.run(Adafruit_MotorHAT.RELEASE); 
    return;
#moving backward
def moveBackward(speed,runTime):
    motorBack.setSpeed(speed)
    motorBack.run(Adafruit_MotorHAT.BACKWARD);
    time.sleep(runTime);
    # turn on motor
    motorBack.run(Adafruit_MotorHAT.RELEASE);
    return;
#Turn Right - note this was created for a monster truck toy - which uses a dc motor to move the axel to about 30 degress
def turnFowardRight(speedBackMotor,speedFrontMotor,runTime):
    motorBack.setSpeed(speedBackMotor)
    motorBack.run(Adafruit_MotorHAT.FORWARD);
    motorFront.setSpeed(speedFrontMotor)
    motorFront.run(Adafruit_MotorHAT.FORWARD);
    time.sleep(runTime);
    # turn on motor
    motorBack.run(Adafruit_MotorHAT.RELEASE);
    motorFront.run(Adafruit_MotorHAT.RELEASE);
    return;

#Turn left - note this was created for a monster truck toy - which uses a dc motor to move the axel to about 30 degress
def turnFowardLeft(speedBackMotor,speedFrontMotor,runTime):
    motorBack.setSpeed(speedBackMotor)
    motorBack.run(Adafruit_MotorHAT.FORWARD);
    motorFront.setSpeed(speedFrontMotor)
    motorFront.run(Adafruit_MotorHAT.BACKWARD);
    time.sleep(runTime);
    # turn on motor
    motorBack.run(Adafruit_MotorHAT.RELEASE);
    motorFront.run(Adafruit_MotorHAT.RELEASE);
    return;

#Increase speed
def increaseSpeed():
    global speed
    global maxSpeed
    global minSpeed
    if speed <= maxSpeed:
        speed = speed + 10 #increaseing speed by 10
        print ('speed +10')
    else:
        speed = maxSpeed

#Decrease speed
def decreaseSpeed():
    global speed
    global maxSpeed
    global minSpeed
    if speed <= minSpeed:
        speed = minSpeed
        print ('speed = minSpeed')
    else:
        speed = speed - 10
        print ('speed -10')

class TemplateHandler(tornado.web.RequestHandler):
    def render_template (self, tpl, context):
        template = ENV.get_template(tpl)
        self.write(template.render(**context))

class MainHandler(TemplateHandler):
    def get(self):
        self.set_header('Cache-Control',
         'no-store, no-cache, must-revalidate, max-age=0')
        self.render_template("index.html", {})

class ControlHandler(TemplateHandler):
    def post(self):
        button = self.get_body_argument('buttonPress')
        print("The button hit is '" + button + "'")
        if button == 'Fast':
            increaseSpeed()
        elif button == 'Slow':
            decreaseSpeed()
        elif button == 'Foward':
            moveFoward(speed,2) #increase or decrese this time for sensitivity
            print("Move Foward")
        elif button == 'Back':
            moveBackward(speed,2)
            print("Move Back")
        elif button == 'Left':
            turnFowardLeft(speed,220,2)
            print("Move Left")
        elif button == 'Right':
            turnFowardRight(speed,220,2)
            print("Move Right")
        else :
            print("Do Nothing")


# Make the Web Applicaton using Tornado
def make_app():
  return tornado.web.Application([
    (r"/", MainHandler),
    (r"/control", ControlHandler)
    ], autoreload=True)

if __name__ == "__main__":
    tornado.log.enable_pretty_logging()
    app = make_app()
    app.listen(PORT, print('Hosting at 8080'))
    tornado.ioloop.IOLoop.current().start()
