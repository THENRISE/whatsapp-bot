from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
	QApplication,
	QMainWindow,
	QWidget,
	QPushButton,
	QLabel,
	QLineEdit,
	QGridLayout,
	QMessageBox,
	QPlainTextEdit
)
from storage import Storage
from messageSender import MessageSender
from datetime import datetime
import random
import pickle
import sys
import os

class HomeWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.setWindowTitle('WhatsApp BOT 0.9')
		self.resize(360, 640)

		layout = QGridLayout()

		# Se existirem dados da menagem salvos, carregue-os
		if (os.path.exists('./messages.dat')):
			initial_message = pickle.load(open('./messages.dat', 'rb'))
		else:
			initial_message = ''

		# Mensagem
		label_message = QLabel('<font size="4">Mensagem:</font>')
		self.text_area_message = QPlainTextEdit(initial_message)
		self.text_area_message.setPlaceholderText("Digite a mensagem...")
		layout.addWidget(label_message, 0, 0)
		layout.addWidget(self.text_area_message, 1, 0, 1, 4)

		# Se existirem dados dos contatos salvos, carregue-os
		if (os.path.exists('./contacts.dat')):
			initial_contacts = pickle.load(open('./contacts.dat', 'rb'))
		else:
			initial_contacts = ''

		# Lista de Contatos
		label_contacts = QLabel('<font size="4">Lista de Contatos:</font>')
		self.text_area_contacts = QPlainTextEdit(initial_contacts)
		self.text_area_contacts.setPlaceholderText("Contatos, um em cada linha")
		layout.addWidget(label_contacts, 3, 0)
		layout.addWidget(self.text_area_contacts, 4, 0, 1, 4)

		# Se existirem configurações de intervalo salvos, carregue-os
		if (os.path.exists('./timing.dat')):
			self.initial_timing = pickle.load(open('./timing.dat', 'rb'))
		else:
			self.initial_timing = {
				'minStepWait': '2',
				'maxStepWait': '4',
				'minNextWait': '5',
				'maxNextWait': '7',
				'minCharWait': '0.3',
				'maxCharWait': '0.7',
				'initTimer': '0',
			} # self.initial_timing

		# Intervalo entre os passos
		label_step_interval = QLabel('<font size="3">Intervalo entre <b>passos</b> em seg.:</font>')
		self.line_edit_step_min = QLineEdit(self.initial_timing['minStepWait'])
		label_step_divider = QLabel('<font size="3">a</font>')
		self.line_edit_step_max = QLineEdit(self.initial_timing['maxStepWait'])
		layout.addWidget(label_step_interval, 5, 0)
		layout.addWidget(self.line_edit_step_min, 5, 1)
		layout.addWidget(label_step_divider, 5, 2)
		layout.addWidget(self.line_edit_step_max, 5, 3)

		# Intervalo entre os contatos
		label_contact_interval = QLabel('<font size="3">Intervalo entre <b>contatos</b> em seg.:</font>')
		self.line_edit_contact_min = QLineEdit(self.initial_timing['minNextWait'])
		label_contact_divider = QLabel('<font size="3">a</font>')
		self.line_edit_contact_max = QLineEdit(self.initial_timing['maxNextWait'])
		layout.addWidget(label_contact_interval, 6, 0)
		layout.addWidget(self.line_edit_contact_min, 6, 1)
		layout.addWidget(label_contact_divider, 6, 2)
		layout.addWidget(self.line_edit_contact_max, 6, 3)

		# Intervalo entre os caracteres
		label_chars_interval = QLabel('<font size="3">Intervalo entre <b>caracteres</b> em seg.:</font>')
		self.line_edit_chars_min = QLineEdit(self.initial_timing['minCharWait'])
		label_chars_divider = QLabel('<font size="3">a</font>')
		self.line_edit_chars_max = QLineEdit(self.initial_timing['maxCharWait'])
		layout.addWidget(label_chars_interval, 7, 0)
		layout.addWidget(self.line_edit_chars_min, 7, 1)
		layout.addWidget(label_chars_divider, 7, 2)
		layout.addWidget(self.line_edit_chars_max, 7, 3)

		# Tempo de espera para iniciar o envio
		label_init_timer = QLabel('<font size="3">Espera para iniciar o envio em min.:</font>')
		self.line_edit_init_timer = QLineEdit(self.initial_timing['initTimer'])
		layout.addWidget(label_init_timer, 8, 0)
		layout.addWidget(self.line_edit_init_timer, 8, 1)

		button_start = QPushButton('Iniciar')
		button_start.clicked.connect(self.handleStartClick)
		button_save = QPushButton('Salvar')
		button_save.clicked.connect(self.handleSaveClick)
		button_exit = QPushButton('Sair')
		button_exit.clicked.connect(self.handleExitClick)
		layout.addWidget(button_start, 9, 0)
		layout.addWidget(button_save, 9, 1)
		layout.addWidget(button_exit, 9, 3)
		self.setLayout(layout)

	def handleStartClick(self):
		# Verificar e extrair os dados do formulário
		if (not self.getFormData()):
			return

		print('[~]================[ WhatsApp BOT 0.9 ]=================[~]')
		print('')
		print('Criado por: gustavo.c.franca@anhanguera.com')
		print('            T.I. Anhanguera Taubaté')
		print('')
		print('[~]=====================================================[~]')
		print('')

		# A mensagem a ser enviada, obtida pelo campo "Mensagem"
		self.messages = self.message.split('===')

		# Nome dos grupos ou pessoas a quem você deseja enviar a mensagem
		# Deve estar exatamente igual que aparece no WhatsApp
		# Esses nomes são colocado no campo mensagem, um em cada linha
		self.contact_list = self.contact_list.split('\n')

		# Obter as configurações de timing
		try:
			self.timing = pickle.load(open('timing.dat', 'rb'))
		except:
			print('Nenhum dado salvo encontrado.')
			print('Gerando arquivos de configurações (salvamento automático).')
			self.timing = self.initial_timing
			self.handleSaveClick()

		message_sender = MessageSender({
			'minStepWait': self.min_step_wait,
			'maxStepWait': self.max_step_wait,
			'minNextWait': self.min_next_wait,
			'maxNextWait': self.max_next_wait,
			'minCharWait': self.min_char_wait,
			'maxCharWait': self.max_char_wait,
			'initTimer': self.init_timer,
		}) # MessageSender

		message_sender.openWhatsApp()

		print('Enviando mensagens para ' + str(len(self.contact_list)) + ' contatos.')
		
		success_sent = 0
		failed_sent = 0

		self.log('[~]=====================================================[~]')
		self.log(f"Enviando mensagens para {str(len(self.contact_list))} contatos.")
		self.log(f"Início em: {self.getTimestamp()}.\n")

		for contact in self.contact_list: 
			print('[~]=====================================================[~]')
			print('Enviando mensagem para ' + contact)
			if (message_sender.sendMessage(contact, (random.choice(self.messages)).split('\n'))):
				print('Mensagem enviada para ' + contact)
				self.log(f"+ {contact}, {self.getTimestamp()}")
				success_sent += 1
			else:
				print('Falha ao enviar a mensagem para ' + contact)
				self.log(f"# {contact}, {self.getTimestamp()}")
				failed_sent += 1
		
		print('[~]=====================================================[~]')
		print('\n\n')
		print('[~]=====================================================[~]')
		print(f"Mensagens enviadas com sucesso para {success_sent} contatos.")
		print(f"{failed_sent} mensagens falharam.")
		print(f"Total: {str(len(self.contact_list))}")
		print('Finalizado.')
		print('[~]=====================================================[~]')

		self.log(f"\nFinalizado em {self.getTimestamp()}")
		self.log(f"{success_sent} mensagens enviadas com sucesso.")
		self.log(f"{failed_sent} falharam.")
		self.log(f"Total: {str(len(self.contact_list))}")
		self.log('[~]=====================================================[~]\n')

	def handleSaveClick(self):
		self.getFormData()
		data_storage = Storage()
		data_storage.saveData(
			self.message,
			self.contact_list,
			self.min_step_wait,
			self.max_step_wait,
			self.min_next_wait,
			self.max_next_wait,
			self.min_char_wait,
			self.max_char_wait,
			self.init_timer
		) # saveData

	def handleExitClick(self):
		quit()

	def checkFormData(self):
		message_box = QMessageBox(QMessageBox.NoIcon, 'Alerta', 'Alerta')
		error = False

		if (self.message.replace(' ', '') == ''):
			message_box.setText('Informe uma <b>mensagem</b>!')
			error = True

		if (self.contact_list.replace(' ', '') == ''):
			message_box.setText('Informe pelo menos um <b>contato</b>!')
			error = True

		if (self.min_step_wait.replace(' ', '') == ''):
			message_box.setText('Informe o <b>intervalo mínimo</b> entre os <b>passos</b>!')
			error = True

		if (self.max_step_wait.replace(' ', '') == ''):
			message_box.setText('Informe o <b>intervalo máximo</b> entre os <b>passos</b>!')
			error = True

		if (self.min_next_wait.replace(' ', '') == ''):
			message_box.setText('Informe o <b>intervalo mínimo</b> entre os <b>contatos</b>!')
			error = True

		if (self.max_next_wait.replace(' ', '') == ''):
			message_box.setText('Informe o <b>intervalo máximo</b> entre os <b>contatos</b>!')
			error = True

		if (self.min_char_wait.replace(' ', '') == ''):
			message_box.setText('Informe o <b>intervalo mínimo</b> entre os <b>caracteres</b>!')
			error = True

		if (self.max_char_wait.replace(' ', '') == ''):
			message_box.setText('Informe o <b>intervalo máximo</b> entre os <b>caracteres</b>!')
			error = True

		if (self.init_timer.replace(' ', '') == ''):
			message_box.setText('Informe a <b>espera para o início do envio</b>!')
			error = True

		if (not error):
			if (float(self.min_step_wait) > float(self.max_step_wait)):
				message_box.setText('O <b>intervalo mínimo de passos</b> deve ser menor que o <b>intervalo máximo</b>!')
				error = True

			if (float(self.min_next_wait) > float(self.max_next_wait)):
				message_box.setText('O <b>intervalo mínimo entre contatos</b> deve ser menor que o <b>intervalo máximo</b>!')
				error = True

			if (float(self.min_char_wait) > float(self.max_char_wait)):
				message_box.setText('O <b>intervalo mínimo entre caractere</b> deve ser menor que o <b>intervalo máximo</b>!')
				error = True

			if (float(self.init_timer) < 0):
				message_box.setText('A <b>espera para o início do envio</b> deve ser <b>maior ou igual</b> a zero!')
				error = True

		if (error):
			message_box.exec_()
			return False

		return True

	def getFormData(self):
		self.message = self.text_area_message.toPlainText()
		self.contact_list = self.text_area_contacts.toPlainText()
		self.min_step_wait = self.line_edit_step_min.text()
		self.max_step_wait = self.line_edit_step_max.text()
		self.min_next_wait = self.line_edit_contact_min.text()
		self.max_next_wait = self.line_edit_contact_max.text()
		self.min_char_wait = self.line_edit_chars_min.text()
		self.max_char_wait = self.line_edit_chars_max.text()
		self.init_timer = self.line_edit_init_timer.text()

		return self.checkFormData()

	def log(self, message):
		os.system(f"echo \"{message}\" >> ./sent-log.txt")

	def getTimestamp(self):
		datetime_obj = datetime.now()
		return datetime_obj.strftime("%d-%m-%Y %H:%M:%S")

if __name__ == '__main__':
	app = QApplication(sys.argv)

	home = HomeWindow()
	home.show()

	sys.exit(app.exec_())