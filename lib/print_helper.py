import colorama
from time import time
from colorama import Fore,Style
from traceback import extract_stack
colorama.init()
class PrintHelper():
	class PrintHelperMessage():
		def __init__(self, message, tag):
			self.message 	= message
			self.tag		= tag
			self.stack		= extract_stack()[-3]
		def __str__(self):
			return ("%s,%s,%s" %(self.tag, str(self.message),self.stack))
	class PrintHelperLogger():
		def __init__(self, path):
			self.messages = []
			self.path		= path
		def append(self, msg):
			self.messages.append(msg)
			self.write(msg)
		def write(self, msg):
			with open (self.path, "a") as file:
				file.write(str(msg) + "\n")
	DEFAULT_PAD_HEADER_SIZE	= 56
	HEADER_COLOUR			= Fore.BLUE
	PRINTING_ON 			= True
	TIMERS					= {}
	logFilePath				= False
	messages				= []
	@staticmethod
	def logFile(path):
		__class__.messages = __class__.PrintHelperLogger(path)
		
	@staticmethod
	def startTimer(key):
		__class__.TIMERS[key] = time()
	@staticmethod
	def printTimeDelta(msg, key):
		__class__.messages.append(__class__.PrintHelperMessage(msg, key))
		__class__.print("%s in %s" %(msg, str(__class__.timeDelta(key))), flag=key+"-Timer")
	@staticmethod
	def timeDelta(key):
		return time() - __class__.TIMERS[key]
	@staticmethod
	def print(msg, flag="Notification"):
		__class__.messages.append(__class__.PrintHelperMessage(msg, flag))
		if __class__.PRINTING_ON:
			print(Fore.YELLOW + "--> %s:\t%s%s" %(flag, msg, Style.RESET_ALL))
	@staticmethod
	def printError(msg, flag="Error"):
		__class__.messages.append(__class__.PrintHelperMessage(msg, flag))
		if __class__.PRINTING_ON:
			print(Fore.RED + "--> %s:\t%s%s" %(flag, msg, Style.RESET_ALL))
	@staticmethod
	def printHeader(header):
		__class__.messages.append(__class__.PrintHelperMessage(header, ""))
		if __class__.PRINTING_ON:
			header = __class__.padWithChar(header, "-")
			print(__class__.HEADER_COLOUR + header + Style.RESET_ALL)
	@staticmethod
	def printSubHeader(msg, flag="Sub section"):
		__class__.messages.append(__class__.PrintHelperMessage(msg, flag))
		if __class__.PRINTING_ON:
			print(Fore.WHITE + "==> %s:\t%s%s" %(flag, msg, Style.RESET_ALL))
	@staticmethod
	def padWithChar(str, char, size=DEFAULT_PAD_HEADER_SIZE):
		str = " " + str + " "
		padSize = (size - __class__.DEFAULT_PAD_HEADER_SIZE - len(str)) / 2
		output = ""
		while len(str) < __class__.DEFAULT_PAD_HEADER_SIZE:
			str = char + str + char
		return str
