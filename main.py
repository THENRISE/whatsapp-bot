import PySimpleGUI as sg
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pickle
import random
import time
import os

class Main:
	def __init__(self):
		if (os.path.exists('./messages.dat')):
			initial_mesasge = pickle.load(open('./messages.dat', 'rb'))
		else:
			initial_mesasge = ''

		if (os.path.exists('./contacts.dat')):
			initial_contacts = pickle.load(open('./contacts.dat', 'rb'))
		else:
			initial_contacts = ''

		if (os.path.exists('./timing.dat')):
			initial_timing = pickle.load(open('./timing.dat', 'rb'))
		else:
			initial_timing = {
				'minStepWait': 2,
				'maxStepWait': 4,
				'minNextWait': 5,
				'maxNextWait': 7,
				'minCharWait': 0.4,
				'maxCharWait': 0.8
			}

		# Layout
		sg.theme('Reddit')
		layout = [
			[sg.Text('Mensagem: ', size=(15, 0))],
			[
				sg.Multiline(
					size=(50, 10),
					key='message',
					default_text=initial_mesasge
				)
			],
			[sg.Text('Contatos: ', size=(15, 0))],
			[sg.Text('Os nomes dos contatos ou grupos devem ser idênticos aos que estão na sua lista de contatos do WhatsApp.', size=(50, 0))],
			[
				sg.Multiline(
					size=(50, 5),
					key='contactList',
					default_text=initial_contacts
				)
			],
			[sg.Text('Atenção: definir intervalos baixos além de exigir um computador mais potente, corre o risco de ser bloqueado no WhatsApp.', size=(50, 0))],
			[
				sg.Text('Intervalo entre os passos em seg.:', size=(34, 0)),
				sg.InputText(
					size=(7, 0),
					key='minStepWait',
					default_text=initial_timing['minStepWait']
				),
				sg.Text('a', size=(2, 0), justification='center'),
				sg.InputText(
					size=(7, 0),
					key='maxStepWait',
					default_text=initial_timing['maxStepWait']
				)
			],
			[
				sg.Text('Intervalo entre os contatos em seg.:', size=(34, 0)),
				sg.InputText(
					size=(7, 0),
					key='minNextWait',
					default_text=initial_timing['minNextWait']
				),
				sg.Text('a', size=(2, 0), justification='center'),
				sg.InputText(
					size=(7, 0),
					key='maxNextWait',
					default_text=initial_timing['maxNextWait']
				)
			],
			[
				sg.Text('Intervalo entre os caracteres em seg.:', size=(34, 0)),
				sg.InputText(
					size=(7, 0),
					key='minCharWait',
					default_text=initial_timing['minCharWait']
				),
				sg.Text('a', size=(2, 0), justification='center'),
				sg.InputText(
					size=(7, 0),
					key='maxCharWait',
					default_text=initial_timing['maxCharWait']
				)
			],
			[sg.Button('Iniciar'), sg.Button('Salvar'), sg.Button('Fechar')]
		]

		# Janela
		self.window = sg.Window("WhatsApp BOT 0.3").layout(layout)

	def Start(self):
		while True:
			# Obter os dados da tela
			self.event, self.values = self.window.Read()

			# Clicar no botão fechar
			if self.event in (None, 'Fechar'):
				quit()
				break

			# Clicar no botão salvar
			if self.event in (None, 'Salvar'):
				# Salvar em um arquivo as configurações
				pickle.dump(self.values['message'], open('messages.dat', 'wb'))
				pickle.dump(self.values['contactList'], open('contacts.dat', 'wb'))
				pickle.dump({
					'minStepWait': self.values['minStepWait'],
					'maxStepWait': self.values['maxStepWait'],
					'minNextWait': self.values['minNextWait'],
					'maxNextWait': self.values['maxNextWait'],
					'minCharWait': self.values['minCharWait'],
					'maxCharWait': self.values['maxCharWait']
				}, open('timing.dat', 'wb'))
				continue

			if self.event in (None, 'Iniciar'):
				# A mensagem a ser enviada, obtida pelo campo "Mensagem"
				self.messages = self.values['message'].split('\n')

				# Nome dos grupos ou pessoas a quem você deseja enviar a mensagem
				# Deve estar exatamente igual que aparece no WhatsApp
				# Esses nomes são colocado no campo mensagem, um em cada linha
				self.contact_list = self.values['contactList'].split('\n')

				# Obter as configurações de timing
				self.timing = pickle.load(open('timing.dat', 'rb'))

				# Configuração do WebDriver
				options = webdriver.ChromeOptions()
				# options = webdriver.FirefoxOptions()
				options.add_argument('lang=pt-br')
				self.driver = webdriver.Chrome(
					executable_path=r'/usr/bin/chromedriver',
					options=options
				)
				# self.driver = webdriver.Firefox(
				# 	executable_path=r'/usr/bin/geckodriver',
				# 	options=options
				# )

				print(self.timing)
				self.SendMessage()

	def SendMessage(self):
		# Abrir o navegador e aguardar 30 segundos
		time.sleep(5)
		self.driver.get('https://web.whatsapp.com')
		time.sleep(30)

		# Para cada contato, enviar a mensagem
		for contact in self.contact_list:
			# Se o contato estiver vazio, pule para o próximo
			if (contact.replace(' ', '') == ''):
				continue

			# Selecionar o um contato no painel de contatos
			contact_panel = self.driver.find_element_by_xpath(f"//span[@title='{contact}']")
			time.sleep(random.uniform(float(self.timing['minStepWait']), float(self.timing['maxStepWait'])))
			contact_panel.click()

			# Selecionar o campo de texto
			chat_box = self.driver.find_element_by_class_name('_1Plpp')
			time.sleep(random.uniform(float(self.timing['minStepWait']), float(self.timing['maxStepWait'])))
			chat_box.click()

			# Para cada pedaço da mensagem envie a mensagem e aperte Shift+Enter
			for message in self.messages:
				# Escrever cada caractere da mensagem individualmente
				for char in list(message):
					print(char)
					chat_box.send_keys(char)
					time.sleep(random.uniform(float(self.timing['minCharWait']), float(self.timing['maxCharWait'])))
				
				time.sleep(random.uniform(float(self.timing['minStepWait']), float(self.timing['maxStepWait'])))

				# Após escrever o trecho de mensagem, aperte Shift+Enter
				ActionChains(self.driver) \
					.key_down(Keys.SHIFT) \
					.key_down(Keys.ENTER) \
					.key_up(Keys.ENTER) \
					.key_up(Keys.SHIFT) \
					.perform()
				print('[Shift+Enter]')

			# Selecionar o botão de enviar
			send_button = self.driver.find_element_by_xpath('//span[@data-icon="send"]')
			time.sleep(random.uniform(int(self.timing['minStepWait']), int(self.timing['maxStepWait'])))
			send_button.click()

			# Aguardar para o próximo contato
			time.sleep(random.uniform(int(self.timing['minNextWait']), int(self.timing['maxNextWait'])))

os.system('clear')
screen = Main()
screen.Start()
