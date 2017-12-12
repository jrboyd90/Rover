import os
import tornado.log
import tornado.ioloop
import tornado.web
import tornado.websocket
import time
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import atexit
from jinja2 import Environment, PackageLoader, select_autoescape

PORT = int(os.environ.get('PORT', '8888'))

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
motorBackRight = mh.getMotor(1)  #M1
motorBackLeft = mh.getMotor(2)  #M2
motorFrontRight = mh.getMotor(3)  #M3
motorFrontLeft = mh.getMotor(4)  #M4
interval = 1 #interval to check for key press/release - change to increase/decrease sensetivity
minSpeed = 100
maxSpeed = 200
speed = 100 #intial speed

def moveForward(speed,runTime):
    motorBackLeft.setSpeed(speed)
    motorBackLeft.run(Adafruit_MotorHAT.FORWARD)
    motorBackRight.setSpeed(speed)
    motorBackRight.run(Adafruit_MotorHAT.FORWARD)
    motorFrontLeft.setSpeed(speed)
    motorFrontLeft.run(Adafruit_MotorHAT.FORWARD)
    motorFrontRight.setSpeed(speed)
    motorFrontRight.run(Adafruit_MotorHAT.FORWARD)
    time.sleep(runTime);#this is not required as motors are release on key release
    #turn off motor
    motorBackLeft.run(Adafruit_MotorHAT.RELEASE) #release when key is release
    motorBackRight.run(Adafruit_MotorHAT.RELEASE)
    motorFrontLeft.run(Adafruit_MotorHAT.RELEASE)
    motorFrontRight.run(Adafruit_MotorHAT.RELEASE)
    return;


def moveForwardWS(speed):
    motorBackLeft.setSpeed(speed)
    motorBackLeft.run(Adafruit_MotorHAT.FORWARD)
    motorBackRight.setSpeed(speed)
    motorBackRight.run(Adafruit_MotorHAT.FORWARD)
    motorFrontLeft.setSpeed(speed)
    motorFrontLeft.run(Adafruit_MotorHAT.FORWARD)
    motorFrontRight.setSpeed(speed)
    motorFrontRight.run(Adafruit_MotorHAT.FORWARD)
    return

#moving backward
def moveBackward(speed,runTime):
    motorBackLeft.setSpeed(speed)
    motorBackRight.setSpeed(speed)
    motorFrontLeft.setSpeed(speed)
    motorFrontRight.setSpeed(speed)
    motorBackLeft.run(Adafruit_MotorHAT.BACKWARD)
    motorBackRight.run(Adafruit_MotorHAT.BACKWARD)
    motorFrontLeft.run(Adafruit_MotorHAT.BACKWARD)
    motorFrontRight.run(Adafruit_MotorHAT.BACKWARD)
    time.sleep(runTime);
    # turn off motor
    motorBackLeft.run(Adafruit_MotorHAT.RELEASE)
    motorBackRight.run(Adafruit_MotorHAT.RELEASE)
    motorFrontLeft.run(Adafruit_MotorHAT.RELEASE)
    motorFrontRight.run(Adafruit_MotorHAT.RELEASE)
    return;


def moveBackwardWS(speed):
    motorBackLeft.setSpeed(speed)
    motorBackRight.setSpeed(speed)
    motorFrontLeft.setSpeed(speed)
    motorFrontRight.setSpeed(speed)
    motorBackLeft.run(Adafruit_MotorHAT.BACKWARD)
    motorBackRight.run(Adafruit_MotorHAT.BACKWARD)
    motorFrontLeft.run(Adafruit_MotorHAT.BACKWARD)
    motorFrontRight.run(Adafruit_MotorHAT.BACKWARD)
    return


#Turn Right
def turnRight(speedBackMotor, speedFrontMotor, runTime):
    motorBackLeft.setSpeed(speedBackMotor)
    motorBackLeft.run(Adafruit_MotorHAT.FORWARD)
    motorFrontLeft.setSpeed(speedFrontMotor)
    motorFrontLeft.run(Adafruit_MotorHAT.FORWARD)
    motorBackRight.setSpeed(speedBackMotor)
    motorBackRight.run(Adafruit_MotorHAT.BACKWARD)
    motorFrontRight.setSpeed(speedFrontMotor)
    motorFrontRight.run(Adafruit_MotorHAT.BACKWARD)
    time.sleep(runTime)
    # turn off motor
    motorBackLeft.run(Adafruit_MotorHAT.RELEASE)
    motorFrontLeft.run(Adafruit_MotorHAT.RELEASE)
    motorBackRight.run(Adafruit_MotorHAT.RELEASE)
    motorFrontRight.run(Adafruit_MotorHAT.RELEASE)
    return


def turnRightWS(speed):
    motorBackLeft.setSpeed(speed)
    motorBackLeft.run(Adafruit_MotorHAT.FORWARD)
    motorFrontLeft.setSpeed(speed)
    motorFrontLeft.run(Adafruit_MotorHAT.FORWARD)
    motorBackRight.setSpeed(speed)
    motorBackRight.run(Adafruit_MotorHAT.BACKWARD)
    motorFrontRight.setSpeed(speed)
    motorFrontRight.run(Adafruit_MotorHAT.BACKWARD)
    return


#Turn left
def turnLeft(speedBackMotor, speedFrontMotor, runTime):
    motorBackLeft.setSpeed(speedBackMotor)
    motorBackLeft.run(Adafruit_MotorHAT.BACKWARD)
    motorFrontLeft.setSpeed(speedFrontMotor)
    motorFrontLeft.run(Adafruit_MotorHAT.BACKWARD)
    motorBackRight.setSpeed(speedBackMotor)
    motorBackRight.run(Adafruit_MotorHAT.FORWARD)
    motorFrontRight.setSpeed(speedFrontMotor)
    motorFrontRight.run(Adafruit_MotorHAT.FORWARD)
    time.sleep(runTime)
    # turn off motor
    motorBackLeft.run(Adafruit_MotorHAT.RELEASE)
    motorFrontLeft.run(Adafruit_MotorHAT.RELEASE)
    motorBackRight.run(Adafruit_MotorHAT.RELEASE)
    motorFrontRight.run(Adafruit_MotorHAT.RELEASE)
    return


def turnLeftWS(speed):
    motorBackLeft.setSpeed(speed)
    motorBackLeft.run(Adafruit_MotorHAT.BACKWARD)
    motorFrontLeft.setSpeed(speed)
    motorFrontLeft.run(Adafruit_MotorHAT.BACKWARD)
    motorBackRight.setSpeed(speed)
    motorBackRight.run(Adafruit_MotorHAT.FORWARD)
    motorFrontRight.setSpeed(speed)
    motorFrontRight.run(Adafruit_MotorHAT.FORWARD)
    return
#Increase speed
def increaseSpeed():
    global speed
    global maxSpeed
    global minSpeed
    if speed <= maxSpeed:
        speed = speed + 10 #increaseing speed by 10
        print ('speed +10')
        print('speed = ' + str(speed))
    else:
        print('speed = maxSpeed')
    return

#Decrease speed
def decreaseSpeed():
    global speed
    global maxSpeed
    global minSpeed
    if speed <= minSpeed:
        speed = minSpeed
        print('speed = minSpeed')
    else:
        speed = speed - 10
        print('speed -10')
        print('speed = ' + str(speed))
    return

# release the motors for the Websocket
def releaseWS():
    motorBackLeft.run(Adafruit_MotorHAT.RELEASE)
    motorBackRight.run(Adafruit_MotorHAT.RELEASE)
    motorFrontLeft.run(Adafruit_MotorHAT.RELEASE)
    motorFrontRight.run(Adafruit_MotorHAT.RELEASE)
    return


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
        elif button == 'Forward':
            moveForward(speed, 2)  #increase or decrese this time for sensitivity
            print("Move Forward")
        elif button == 'Back':
            moveBackward(speed, 2)
            print("Move Back")
        elif button == 'Left':
            turnLeft(speed, 220, .5)
            print("Move Left")
        elif button == 'Right':
            turnRight(speed, 220, .5)
            print("Move Right")
        else:
            print("Do Nothing")
        self.redirect('/')


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print('open')

    def on_message(self, message):
        button = message
        print("The button hit is '" + button + "'")
        if button == 'Fast':
            increaseSpeed()
        elif button == 'Slow':
            decreaseSpeed()
        elif button == 'Forward':
            moveForwardWS(speed)
            print("Move Forward")
        elif button == 'Back':
            moveBackwardWS(speed)
            print("Move Back")
        elif button == 'Left':
            turnLeftWS(speed)
            print("Move Left")
        elif button == 'Right':
            turnRightWS(speed)
            print("Move Right")
        elif button == 'Release':
            releaseWS()

    def on_close(self):
        print('closed')


# Make the Web Applicaton using Tornado
def make_app():
    return tornado.web.Application([
      (r"/", MainHandler),
      (r"/control", ControlHandler),
      (r"/ws", WebSocketHandler),
      ], autoreload=True)

if __name__ == "__main__":
    tornado.log.enable_pretty_logging()
    app = make_app()
    app.listen(PORT, print('Hosting at 8888'))
    tornado.ioloop.IOLoop.current().start()
