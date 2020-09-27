import ujson

class Protocol:
	
	def __init__(self, paddo):
		self.paddo = paddo
		
	def handle(self, msg):
		# print('received %s' % msg.data)
		evt = ujson.loads(str(msg.data))
		# print('parsed %s' % evt)
		
		commands = evt['commands']
		
		for cmd in commands:
			# print('handling %s' % cmd)
			operator = cmd['op']
			if operator == 'clear':
				self.paddo.clear(flush=False)
				print('CLR')
			elif operator == 'set':
				self.paddo.set(cmd['ring'], cmd['pos'], cmd['value'], flush=False)
				print('SET %d AT ring-%d TO %s' % (cmd['pos'], cmd['ring'], cmd['value']))
			elif operator == 'ring':
				self.paddo.ring(cmd['ring'], cmd['value'], flush=False)
				print('SET all AT ring-%d TO %s' % (cmd['ring'], cmd['value']))
			else:
				print('unknown operator: %s' % (operator))
				
		self.paddo.flush()