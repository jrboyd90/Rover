import os
import tornado.log
import tornado.ioloop
import tornado.web
import time
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import atexit

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
