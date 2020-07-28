import pickle
import os

class Storage():
	def saveData(
		self,
		message,
		contact_list,
		min_step_wait,
		max_step_wait,
		min_next_wait, 
		max_next_wait,
		min_char_wait,
		max_char_wait,
		init_timer
	):
		# Salvar em arquivos as configurações
		pickle.dump(message, open('messages.dat', 'wb'))
		pickle.dump(contact_list, open('contacts.dat', 'wb'))
		pickle.dump({
			'minStepWait': min_step_wait,
			'maxStepWait': max_step_wait,
			'minNextWait': min_next_wait,
			'maxNextWait': max_next_wait,
			'minCharWait': min_char_wait,
			'maxCharWait': max_char_wait,
			'initTimer': init_timer
		}, open('timing.dat', 'wb'))