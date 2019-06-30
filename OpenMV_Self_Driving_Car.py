import sensor, image, time
from pyb import UART


THRESHOLD = (0,100)
BINARY_VISIBLE = False

#Creates a grayscale image by making everything black and white pixels
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE) # grayscale is faster
sensor.set_framesize(sensor.QQQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()


# Initialize UART connection
uart = UART(1, 9600, timeout_char=1000)
uart.init(9600, bits=8, parity=None, stop=1, timeout_char=1000) # init with given parameters


#Runs the necessary code
while(True):
    clock.tick()
    img = sensor.snapshot().binary([THRESHOLD]) if BINARY_VISIBLE else sensor.snapshot()

#It does the regression to create lines
    line = img.get_regression([(255,255) if BINARY_VISIBLE else THRESHOLD], robust = True)
    if (line): img.draw_line(line.line(), color =127)
	
	#If there is a line run this:
    	if (line != None):
		#Subtracts x2 from x1 to find direction 
        	delta_x = line[2] - line[0]
		
		# Converts it to string to use UART
        	delta_x = str(delta_x)
		
		# If there is a line sends it through UART
        	if (delta_x != "n"):
           		uart.write(delta_x)
           		time.sleep(2000)
