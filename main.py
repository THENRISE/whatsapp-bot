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
		# Se existirem dados da menagem salvos, carregue-os
		if (os.path.exists('./messages.dat')):
			initial_mesasge = pickle.load(open('./messages.dat', 'rb'))
		else:
			initial_mesasge = ''

		# Se existirem dados dos contatos salvos, carregue-os
		if (os.path.exists('./contacts.dat')):
			initial_contacts = pickle.load(open('./contacts.dat', 'rb'))
		else:
			initial_contacts = ''

		# Se existirem configurações de intervalo salvos, carregue-os
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
		self.window = sg.Window("WhatsApp BOT 0.5").layout(layout)

	def Start(self):
		while True:
			# Obter os dados da tela
			self.event, self.values = self.window.Read()

			# Clicar no botão fechar
			if self.event in (None, 'Fechar'):
				quit()
				break

			self.message = self.values['message']
			self.contact_list = self.values['contactList']
			self.min_step_wait = self.values['minStepWait']
			self.max_step_wait = self.values['maxStepWait']
			self.min_next_wait = self.values['minNextWait']
			self.max_next_wait = self.values['maxNextWait']
			self.min_char_wait = self.values['minCharWait']
			self.max_char_wait = self.values['maxCharWait']

			# Clicar no botão salvar
			if self.event in (None, 'Salvar'):
				# Salvar em arquivos as configurações
				pickle.dump(self.message, open('messages.dat', 'wb'))
				pickle.dump(self.contact_list, open('contacts.dat', 'wb'))
				pickle.dump({
					'minStepWait': self.min_step_wait,
					'maxStepWait': self.max_step_wait,
					'minNextWait': self.min_next_wait,
					'maxNextWait': self.max_next_wait,
					'minCharWait': self.min_char_wait,
					'maxCharWait': self.max_char_wait
				}, open('timing.dat', 'wb'))

				continue

			if self.event in (None, 'Iniciar'):
				# A mensagem a ser enviada, obtida pelo campo "Mensagem"
				self.messages = self.message.split('\n')

				# Nome dos grupos ou pessoas a quem você deseja enviar a mensagem
				# Deve estar exatamente igual que aparece no WhatsApp
				# Esses nomes são colocado no campo mensagem, um em cada linha
				self.contact_list = self.values['contactList'].split('\n')

				# Obter as configurações de timing
				self.timing = pickle.load(open('timing.dat', 'rb'))

				# Configuração do WebDriver
				options = webdriver.ChromeOptions()
				options.add_argument('lang=pt-br')
				self.driver = webdriver.Chrome(
					executable_path=r'./chromedriver',
					options=options
				)

				# Abrir o navegador e aguardar 30 segundos
				time.sleep(5)
				self.driver.get('https://web.whatsapp.com')
				time.sleep(30)

				self.SendMessage()

	def SendMessage(self):
		# Para cada contato, enviar a mensagem
		for contact in self.contact_list:
			# Se o contato estiver vazio, pule para o próximo
			if (contact.replace(' ', '') == ''):
				continue

			# Pesquisar o contato no painel de contatos
			search_box = self.driver.find_element_by_class_name('_3FRCZ')
			search_slice = ''

			time.sleep(random.uniform(float(self.timing['minStepWait']), float(self.timing['maxStepWait'])))
			search_box.click()

			# Apagar o texto que estiver escrito
			while (self.driver.find_elements_by_class_name('_3FRCZ')[0].get_attribute('innerText') != ''):
				time.sleep(random.uniform(float(self.timing['minCharWait']), float(self.timing['maxCharWait'])))
				search_box_value.send_keys(Keys.BACKSPACE)

			for char in list(contact):
				# Valor interno do campo de texto para checagem
				search_box_value = self.driver.find_elements_by_class_name('_3FRCZ')[0]
				search_text = search_box_value.get_attribute('innerText')

				while (search_slice + char == search_text + char):
					search_box.send_keys(char)
					time.sleep(random.uniform(float(self.timing['minCharWait']), float(self.timing['maxCharWait'])))

					tmp_search_text = search_box_value.get_attribute('innerText')

					if (search_slice + char == tmp_search_text):
						search_slice += char
			
			# Selecionar o contato no painel de contatos
			contact_panel = self.driver.find_element_by_xpath(f"//span[@title='{contact}']")
			time.sleep(random.uniform(float(self.timing['minStepWait']), float(self.timing['maxStepWait'])))
			contact_panel.click()

			# Selecionar o campo de texto
			chat_box = self.driver.find_element_by_class_name('_3uMse')
			time.sleep(random.uniform(float(self.timing['minStepWait']), float(self.timing['maxStepWait'])))
			chat_box.click()

			message_slice = ''

			# Para cada pedaço da mensagem envie a mensagem e aperte Shift+Enter
			for message in self.messages:

				# Escrever cada caractere da mensagem individualmente
				for char in list(message):
					# Valor interno do campo de texto para checagem
					chat_box_value = self.driver.find_elements_by_class_name('_3FRCZ')[1]
					inner_text = chat_box_value.get_attribute('innerText').replace('\n', '')

					while (message_slice + char == inner_text + char):
						chat_box.send_keys(char)
						time.sleep(random.uniform(float(self.timing['minCharWait']), float(self.timing['maxCharWait'])))

						tmp_inner_text = chat_box_value.get_attribute('innerText').replace('\n', '')

						if (message_slice + char == tmp_inner_text):
							message_slice += char
				
				time.sleep(random.uniform(float(self.timing['minStepWait']), float(self.timing['maxStepWait'])))

				# Após escrever o trecho de mensagem, aperte Shift+Enter
				ActionChains(self.driver) \
					.key_down(Keys.SHIFT) \
					.key_down(Keys.ENTER) \
					.key_up(Keys.ENTER) \
					.key_up(Keys.SHIFT) \
					.perform()

			# Selecionar o botão de enviar
			send_button = self.driver.find_element_by_xpath('//span[@data-icon="send"]')
			time.sleep(random.uniform(int(self.timing['minStepWait']), int(self.timing['maxStepWait'])))
			send_button.click()

			# Aguardar para o próximo contato
			time.sleep(random.uniform(int(self.timing['minNextWait']), int(self.timing['maxNextWait'])))

os.system('clear')
screen = Main()
screen.Start()
