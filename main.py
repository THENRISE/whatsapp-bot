import PySimpleGUI as sg
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import random
import time

class MainScreen:
	def __init__(self):
		# Layout
		sg.theme('Reddit')
		layout = [
			[sg.Text('Mensagem: ', size=(15, 0)), sg.Multiline(size=(30, 5), key='message')],
			[sg.Text('Contatos: ', size=(15, 0)), sg.Multiline(size=(30, 5), key='contactList')],
			[sg.Button('Iniciar')]
		]

		# Janela
		self.window = sg.Window("WhatsApp BOT 0.3").layout(layout)

	def Start(self):
		while True:
			# Obter os dados da tela
			self.button, self.values = self.window.Read()
			
			# A mensagem a ser enviada, obtida pelo campo "Mensagem"
			self.messages = self.values['message'].split('\n')

			# Nome dos grupos ou pessoas a quem você deseja enviar a mensagem
			# Deve estar exatamente igual que aparece no WhatsApp
			# Esses nomes são colocado no campo mensagem, um em cada linha
			self.contact_list = self.values['contactList'].split('\n')

			print("Enviando para: ")
			print(self.contact_list)
			print("\nMensagem: ")
			print(self.messages)

			# Configuração do WebDriver
			options = webdriver.ChromeOptions()
			options.add_argument('lang=pt-br')
			self.driver = webdriver.Chrome(
				executable_path=r'/usr/bin/chromedriver',
				options=options
			)

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
			time.sleep(3)
			contact_panel.click()

			# Selecionar o campo de texto
			chat_box = self.driver.find_element_by_class_name('_1Plpp')
			time.sleep(3)
			chat_box.click()

			# Para cada pedaço da mensagem envie a mensagem e aperte Shift+Enter
			for message in self.messages:
				# Escrever cada caractere da mensagem individualmente
				for char in list(message):
					print(char)
					chat_box.click()
					chat_box.send_keys(char)
					time.sleep(random.uniform(0.1, 0.5))
				

				# Após escrever o trecho de mensagem, aperte Shift+Enter
				ActionChains(self.driver) \
						.key_down(Keys.SHIFT) \
						.send_keys_to_element(chat_box, Keys.ENTER) \
						.key_up(Keys.SHIFT) \
						.perform()
				print('[Shift+Enter]')

			# Selecionar o botão de enviar
			send_button = self.driver.find_element_by_xpath('//span[@data-icon="send"]')
			time.sleep(3)
			send_button.click()

			# Aguardar para o próximo contato
			time.sleep(5)

screen = MainScreen()
screen.Start()




# Mensagem testada:


# Olá, eu sou o BOT, seu amiguinho, vamos brincar?
#
# Esta mensagem tem "Enters".