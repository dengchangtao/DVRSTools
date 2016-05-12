class Line(object):
	"""Python object for a dvref mooring line - test"""
	def __init__(self,name):
		self.name = name

	@property
	def Unstretch_length(self):
		try:
			return self._Unstretch_length
		except AttributeError:
			self._Unstretch_length = None
		return self._Unstretch_length
	
	@Unstretch_length.setter
	def Unstretch_length(self,value):
		self._Unstretch_length = value
	
	@property
	def Restoring_coeff(self):
		try:
			return self._Restoring_coeff
		except AttributeError:
			self._Restoring_coeff = []
		return self._Restoring_coeff

	@Restoring_coeff.setter
	def Restoring_coeff(self,value):
		self._Restoring_coeff = value
	
	@property
	def Damping_coeff(self):
		try:
			return self._Damping_coeff
		except AttributeError:
			self._Damping_coeff = []
		return self._Damping_coeff

	@Damping_coeff.setter
	def Damping_coeff(self,value):
		self._Damping_coeff = value
	
	@property
	def Attachment_ship(self):
		try:
			return self._Attachment_ship
		except AttributeError:
			self._Attachment_ship = []
		return self._Attachment_ship
	@Attachment_ship.setter
	def Attachment_ship(self,value):
		self._Attachment_ship = value
	
	@property
	def Attachment_quay(self):
		try:
			return self._Attachment_quay
		except AttributeError:
			self._Attachment_quay = []
		return self._Attachment_quay
	@Attachment_quay.setter
	def Attachment_quay(self,value):
		self._Attachment_quay = value
	
	@property
	def Attached_to_body(self):
		try:
			return self._Attached_to_body
		except AttributeError:
			self._Attached_to_body = None
		return self._Attached_to_body
	@Attached_to_body.setter
	def Attached_to_body(self,value):
		self._Attached_to_body = value

class Lines(list):
	"""Inherits from line object"""
	def __init__(self,Number_lines):
		self.Number_lines = Number_lines

class Fender(object):
	"""Generates a dvref fender"""
	def __init__(self,name):
		self.name = name

	@property
	def Restoring_coeff(self):
		try:
			return self._Restoring_coeff
		except AttributeError:
			self._Restoring_coeff = []
		return self._Restoring_coeff
	@Restoring_coeff.setter
	def Restoring_coeff(self,value):
		self._Restoring_coeff = value
	@property
	def Damping_coeff(self):
		try:
			return self._Damping_coeff
		except AttributeError:
			self._Damping_coeff = []
		return self._Damping_coeff
	@Damping_coeff.setter
	def Damping_coeff(self,value):
		self._Damping_coeff = value
	@property
	def Friction_coeff(self):
		try:
			return self._Friction_coeff
		except AttributeError:
			self._Friction_coeff = []
		return self._Friction_coeff
	@Friction_coeff.setter
	def Friction_coeff(self,value):
		self._Friction_coeff = value
	@property
	def Attachment_ship(self):
		try:
			return self._Attachment_ship
		except AttributeError:
			self._Attachment_ship = []
		return self._Attachment_ship
	@Attachment_ship.setter
	def Attachment_ship(self,value):
		self._Attachment_ship = value
	@property
	def Attachment_quay(self):
		try:
			return self._Attachment_quay
		except AttributeError:
			self._Attachment_quay = []
		return self._Attachment_quay
	@Attachment_quay.setter
	def Attachment_quay(self,value):
		self._Attachment_quay = value
	@property
	def Fender_dir(self):
		try:
			return self._Fender_dir
		except AttributeError:
			self._Fender_dir = []
		return self._Fender_dir
	@Fender_dir.setter
	def Fender_dir(self,value):
		self._Fender_dir = value
	@property
	def Attached_to_body(self):
		try:
			return self._Attached_to_body
		except AttributeError:
			self._Attached_to_body = []
		return self._Attached_to_body
	@Attached_to_body.setter
	def Attached_to_body(self,value):
		self._Attached_to_body = value

class Fenders(list):
	"""docstring for Fenders"""
	def __init__(self,Number_fenders):
		self.Number_fenders = Number_fenders

class DVREF_file(object):
	"""docstring for DVREF_file"""
	def __init__(self, filename):
		super(DVREF_file, self).__init__()
		self.filename = filename
	@property
	def readDvref(self):
		f = open(self.filename)
		self._readDvref = f.read()
		f.close()
		return self._readDvref
	

		
		
		
#class Option_Parameters:
	

#if __name__ == '__main__':
#	test = Line("line_no_1")
#	test.Unstretch_length = 123.9
#	print test.Unstretch_length
#	test.Restoring_coeff = [2.,3.,5]
#	print test.Restoring_coeff[0]
#
#	lines = Lines(24)
#	print lines.Number_lines
#
#	line_no_1 = Line("line_no1")
#	line_no_1.Unstretch_length = 56.391392
#	line_no_1.Restoring_coeff = [135740.55413, 116559.17813, -9215.311887]
#	line_no_1.Damping_coeff = [0.0,0.0]
#	line_no_1.Attachment_ship = [146.551, -0.576, 7.52]
#	line_no_1.Attachment_quay = [165.752, 53.646, 7.0]
#	line_no_1.Attached_to_body = [1,0]
#
#	lines.append(line_no_1)
#	print lines[0].Damping_coeff
#
#	fenders = Fenders(4)
#
#	fender_no_1 = Fender("fender_no_1")
#	fender_no_1.Restoring_coeff = [1748122.64928, -3380753.827608, 6717319.817372, -4629984.640707, 1263226.780136]
#	fender_no_1.Damping_coeff = [0.0,0.0]
#	fender_no_1.Friction_coeff  = 0.1
#	fender_no_1.Attachment_ship = [-48.023, 23.05, -3.18]
#	fender_no_1.Attachment_quay = [-49.273, 23.0, 2.8]
#	fender_no_1.Fender_dir = [0.0, -1.0, 0.0]
#	fender_no_1.Attached_to_body = [1,0]
#
#	fenders.append(fender_no_1)
#	print fenders[0].Fender_dir
#
#	test = DVREF_file(filename = "That")
#	test.filename
#	print (test.filename)
#	print (test.readDvref)