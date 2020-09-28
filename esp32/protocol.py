import ujson


class Protocol:
	
	def __init__(self, paddo):
		self.paddo = paddo
		
	def handle(self, msg):
		print('received %s' % msg.data)
		evt = ujson.loads(str(msg.data))
		print('parsed %s' % evt)
		
		commands = evt['commands']
		
		for cmd in commands:
			print('handling %s' % cmd)
			operator = cmd['op']
			if operator == 'clear':
				self.paddo.clear(flush=False)
				print('CLR')
			elif operator == 'set':
				print('DBG %s' % cmd)

				if "ring" in cmd:
					if "strand" in cmd:
						self.paddo.strand(cmd['ring'], cmd['strand'], cmd['value'], flush=False)
						print('SET %d AT ring-%d TO %s' % (cmd['strand'], cmd['ring'], cmd['value']))
					else:
						self.paddo.ring(cmd['ring'], cmd['value'], flush=False)
						print('SET all AT ring-%d TO %s' % (cmd['ring'], cmd['value']))
				else:
					self.paddo.all(cmd['value'], flush=False)

			else:
				print('unknown operator: %s' % (operator))
				
		self.paddo.flush()