import L1_LinearActuation as act


while 1:
	u_in = int(input('Enter 1 for extension, anything else for retraction.'))
	act.actuate(u_in)
