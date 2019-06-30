from pyb import Pin, Timer
import utime 
from pyb import UART

# Initialize UART connection
uart = UART(3, 9600, timeout_char=1000)
uart.init(9600, bits=8, parity=None, stop=1, timeout_char=1000) # init with given parameters

#W16 has Timer2, Channel1
Apwm=Pin('W16')
timerA=Timer(2, freq=1000)
chA=timerA.channel(1, Timer.PWM, pin=Apwm)

Ain1=Pin('W22', Pin.OUT_PP)
Ain2=Pin('W24', Pin.OUT_PP)

standBy=Pin('W29', Pin.OUT_PP)

#W29 has Timer1, Channel3
Bpwm=Pin('Y12')
timerB=Timer(1, freq=1000)
chB=timerB.channel(3, Timer.PWM, pin=Bpwm)

Bin1=Pin('W30', Pin.OUT_PP)
Bin2=Pin('W32', Pin.OUT_PP)

#Moves the back motor continuosly
def backmotor(speed):
     Ain1.low()
     Ain2.high()
     chA.pulse_width_percent(speed)
     print("Backmotor")

# Turns the wheel according to the delta X from OpenMV
def direction(delta):
     print("Front1")
     if(delta>10):
          Bin1.low()
          Bin2.high()
          chB.pulse_width_percent(delta)
          print("Front2")
     if(delta <-10):
          Bin1.high()
          Bin2.low()
          chB.pulse_width_percent(abs(delta))
          print("Front3")
      if(delta>-10 and delta <10):
          Bin1.high()
          Bin2.high()
          chB.pulse_width_percent(abs(delta))
          print("Front")

# Gets the delta X from OpenMV
def getdelta():
     delta = uart.readline()
     delta = str(delta)
     # Gets rid of from 'b' characters
     delta = delta[2: len(delta)-1]
     utime.sleep(3)
     delta = int(delta)
     if (delta <100):
          direction(delta)
     # If it reads multiple values and puts them together, only gets the last 2 digits
     elif (delta>100):
          delta = str(delta)
          delta = delta[len(delta) -2: len(delta)]
          delta = int(delta)
          direction(delta)

def main():
     standBy.high()
     backmotor(20)
     while (True):
        getdelta()
while (True):
     main()
