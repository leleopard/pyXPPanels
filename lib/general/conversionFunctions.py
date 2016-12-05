import math
import decimal
D = decimal.Decimal

#------------------------------------------------------------------------------------------
#	Conversion functions
#------------------------------------------------------------------------------------------

## Convert input elapsed time in seconds to hh:mm equivalent, and return the mm minutes 
# @param inValue float elapsed time in seconds 
# @param XPlaneDataDispatcher the XPlaneUDPServer instance
#
def returnMinutes(inValue,XPlaneDataDispatcher):
	outValue = inValue//60.0 #total minutes elapsed
	outValue = outValue%60.0
	
	return outValue

## Convert input elapsed time in seconds to hh:mm equivalent, and return the hh minutes 
# @param inValue float elapsed time in seconds 
# @param XPlaneDataDispatcher the XPlaneUDPServer instance
#
def returnHours(inValue,XPlaneDataDispatcher):
	outValue = inValue/60.0 #total minutes elapsed
	outValue = outValue//60.0 #total hours elapsed
	
	return outValue

	
def modulo360(inValue,XPlaneDataDispatcher):
	outValue = inValue%360
	return outValue

def divideby100(inValue,XPlaneDataDispatcher):
	outValue = float(inValue)/100.0
	return outValue

def returnSpeedLabelValue(inValue,XPlaneDataDispatcher):
	outValue = int(float(inValue+0.5)/10.0)
	return outValue

def returnSpeedTapeValue(inValue,XPlaneDataDispatcher):
	outValue = int(inValue)
	outValue = float(outValue)/10
	outValue = outValue%1*10
	outValue = float(outValue)+float(inValue%1)
	return outValue
	
def returnSpeed100sValue(inValue,XPlaneDataDispatcher):
	# 215.27
	outValue = int(inValue)
	#215
	outValue = float(outValue)/100
	#2.15
	outValue = outValue%1*100
	#15
	outValue = float(outValue)+float(inValue%1)
	return outValue

def roundToNearest10(inValue,XPlaneDataDispatcher):
	#8980
	outValue = (D(inValue)//D(10))*10
	return outValue


def returnAlti100sDigit(inValue,XPlaneDataDispatcher):
	#8980
	outValue = (D(inValue)/D(1000))%1
	#8.980%1 = 0.980
	outValue = D(outValue)*10
	#9.80
	return D(outValue)//D(1)

def returnAlti10s(inValue,XPlaneDataDispatcher):
	# 14215.27
	outValue = float(inValue)/100
	#142.1527
	outValue = outValue%1*100
	return outValue
	
def returnAlti1k10kDigits(inValue,XPlaneDataDispatcher):
	# 15215.27
	outValue = int(inValue/1000)
	#15.21527
	return outValue
	
def convertINtomb(inValue,XPlaneDataDispatcher):
	outValue = inValue*33.863753
	#print "inValue: ", inValue, "outValue: ", outValue
	return outValue

def convertSuction(inValue,XPlaneDataDispatcher):
	outValue = inValue*2.8
	#print "inValue: ", inValue, "outValue: ", outValue
	return outValue

def convertLbsToGallons(XPindicatedValue,XPlaneDataDispatcher):
	XPindicatedValue = XPindicatedValue/6
	return XPindicatedValue
	
def return100s(XPindicatedValue,XPlaneDataDispatcher):
	XPindicatedValue = XPindicatedValue/1000
	XPindicatedValue = XPindicatedValue%1
	return XPindicatedValue

def return1000s(XPindicatedValue,XPlaneDataDispatcher):
	XPindicatedValue = XPindicatedValue/10000
	XPindicatedValue = XPindicatedValue%1
	return XPindicatedValue

def return10000s(XPindicatedValue,XPlaneDataDispatcher):
	XPindicatedValue = XPindicatedValue/100000
	XPindicatedValue = XPindicatedValue%1
	return XPindicatedValue

def addCompassHeadingToValue(XPindicatedValue,XPlaneDataDispatcher):
	bugHeading = XPindicatedValue - XPlaneDataDispatcher.dataList[308][0]
	if bugHeading < 0:
		bugHeading = bugHeading+360
	return bugHeading
	
def addNondriftCompassHeadingToValue(XPindicatedValue,XPlaneDataDispatcher):
	bugHeading = XPindicatedValue - XPlaneDataDispatcher.dataList[17][3]
	if bugHeading < 0:
		bugHeading = bugHeading+360
	return bugHeading

def calculateTurnRate(XPindicatedValue,XPlaneDataDispatcher):
	roll = math.radians(XPlaneDataDispatcher.dataList[17][1])
	pitch = math.radians(XPlaneDataDispatcher.dataList[17][0])
	Q = XPlaneDataDispatcher.dataList[16][0]
	P = XPlaneDataDispatcher.dataList[16][1]
	R = XPlaneDataDispatcher.dataList[16][2]
	
	turnRate = Q * math.sin(roll)/math.cos(pitch) + R * math.cos(roll)/math.cos(pitch)
	turnRate = turnRate * 180/math.pi
	#print "Turn rate: ", turnRate
	return turnRate

def NAV_TO_Toggle(XPindicatedValue,XPlaneDataDispatcher):
	val = int(XPindicatedValue)
	if val == 1:
		return True
	else:
		return False

def NAV_FR_Toggle(XPindicatedValue,XPlaneDataDispatcher):
	val = int(XPindicatedValue)
	if val == 2:
		return True
	else:
		return False
		
def NAV_FLG_Toggle (XPindicatedValue,XPlaneDataDispatcher):
	val = int(XPindicatedValue)
	if val == 0:
		return True
	else:
		return False

def NAV_GSFLG_Toggle (XPindicatedValue,XPlaneDataDispatcher):
	val = int(XPindicatedValue)
	if val != 10:
		return True
	else:
		return False
		
def returnTrueIfOverZero(XPindicatedValue,XPlaneDataDispatcher):
	if XPindicatedValue > 0.0:
		return True
	else:
		return False