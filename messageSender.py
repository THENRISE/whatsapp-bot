from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from removeEmojis import removeAllEmojis
import random
import time
import os
import re

class MessageSender():
	search_box_name = '_3FRCZ'
	chat_box_name = '_3uMse'
	multicolor_emoji_selector = 'li._1N-3y.eP_pD._12VoD'

	def __init__(self, timing_settings):
		self.timing = timing_settings

	def openWhatsApp(self):
		options = webdriver.ChromeOptions()
		options.add_argument('lang=pt-br')

		self.driver = webdriver.Chrome(
			executable_path=r'./chromedriver',
			options=options
		) # Chrome

		# options = webdriver.FirefoxOptions()
		# options.add_argument('lang=pt-br')

		# self.driver = webdriver.Firefox(
		# 	executable_path=r'./geckodriver',
		# 	options=options
		# ) # Firefox

		print('Iniciando o WhatsApp...')
		time.sleep(5)

		# Iniciar o WhatsApp aguardar 30 segundos
		self.driver.get('https://web.whatsapp.com')

		# Atrasar o início do envio
		if (int(self.timing['initTimer']) > 0.99):
			for minutes in range(int(self.timing['initTimer']) -1, -1, -1): 
				print('Enviando mensagens em ' + str(minutes + 1) + ' min...')
				time.sleep(1 * 60)

		for seconds in range(15, -1, -1):
			print('Enviando mensagens em ' + str(seconds) + ' seg...')
			time.sleep(1)

	def sendMessage(self, contact, messages):
		# Se o contato estiver vazio, pule para o próximo
		if (contact.replace(' ', '') == ''):
			return False

		# Pesquisar o contato no painel de contatos
		search_box = self.driver.find_element_by_class_name(self.search_box_name)
		search_slice = ''
		self.await_by('step')
		search_box.click()

		search_box_value = self.driver.find_elements_by_class_name(self.search_box_name)[0]

		# Apagar o texto que estiver escrito no campo de pesquisa
		while (self.driver.find_elements_by_class_name(self.search_box_name)[0].get_attribute('innerText') != ''):
			self.await_by('char')
			search_box_value.send_keys(Keys.BACKSPACE)

		last_search_char = ''

		# Digitar cada caractere do contato individualmente na caixa de pesquisa
		for char in list(contact):
			# Valor interno do campo de texto para checar
			search_box_value = self.driver.find_elements_by_class_name(self.search_box_name)[0]
			search_text = search_box_value.get_attribute('innerText')

			# Se o caractere não for digitado, tentar novamente
			# while (search_slice + char == search_text + char):
			while ((search_text == '') or (char != search_text[-1]) or (char == last_search_char)):
				search_box.send_keys(char)
				self.await_by('char')

				search_text = search_box_value.get_attribute('innerText')

				# Se o caractere foi digitado, registrar o sucesso
				# Se o caractere foi digitado
				if (char == search_text[-1]):
					search_slice += char
					last_search_char = ''
					continue

				print('Tentando inserir o caractere [' + char + '] novamente.')
				
			last_search_char = char
		
		# Selecionar o contato no painel de contatos
		try:
			contact_panel = WebDriverWait(self.driver, 10) \
				.until(
					expected_conditions \
						.presence_of_element_located((
							By.XPATH,
							f"//span[@title='{contact}']"
						)) # presence_of_element_located
				) # until
			self.await_by('step')
			contact_panel.click()
		except Exception as error:
			print(f"Contato {contact} não encontrado. Pulando...")
			print(f"Exceção: {error}")
			return False

		# Selecionar o campo de texto
		chat_box = self.driver.find_element_by_class_name(self.chat_box_name)
		self.await_by('step')
		chat_box.click()

		message_slice = ''
		last_char = ''
		emoji = False
		press_tab = False

		# Para cada pedaço da mensagem envie a mensagem e aperte Shift+Enter
		# A mensagem é dividida por '\n', desse jeito é possível pressionar
		# Shift + Enter para quebrar a linha quando o pedaço de mensagem chega
		# ao final
		for index, message in enumerate(messages):
			# Escrever cada caractere da mensagem individualmente no chat
			for char in list(message):
				if (char == ':'):
					print('Emoji encontrado.')
					emoji = True

				# Valor interno do campo de texto para checar
				chat_box_value = self.driver \
					.find_elements_by_class_name(self.search_box_name)[1]
				inner_text_with_emojis = chat_box_value \
					.get_attribute('innerText') \
					.replace('\n', '')
				inner_text = removeAllEmojis(inner_text_with_emojis)

				# Se o caractere for &, prepare para pressionar TAB
				if (emoji and (char == '&')):
					message_slice += char
					# Se este é o segundo caractere &, pressiona o TAB
					if (press_tab and (char == '&')):
						print('Inserindo emoji...')
						# Se o caractere não for inserido, tente novamente
						while (inner_text != message_slice):
							try:
								self.await_by('char')
								emoji_selected = WebDriverWait(self.driver, 10) \
									.until(
										expected_conditions \
											.presence_of_element_located((
												By.XPATH,
												'//span[@data-emoji-index=\'0\']'
											)) # presence_of_element_located
									) # until

								self.await_by('char')
								chat_box.click()

								self.await_by('char')
								self.gotoEnd()

								self.await_by('step')
								chat_box.send_keys(Keys.TAB)
							except:
								print('Emoji não encontrado, pulando...')

							try:
								# Selecionar o popup de cores do emoji
								multicolor_emoji_selected = WebDriverWait(self.driver, 2) \
									.until(
										expected_conditions \
											.presence_of_element_located((
												By.CSS_SELECTOR,
												self.multicolor_emoji_selector
											)) # presence_of_element_located
									) # until

								self.await_by('step')
								multicolor_emoji_selected.click()

								self.await_by('step')
								chat_box.click()

								self.await_by('char')
								self.gotoEnd()
							except:
								print('Emoji não é multicolorido...')
							
							inner_text_with_emojis = chat_box_value \
								.get_attribute('innerText') \
								.replace('\n', '')
							inner_text = removeAllEmojis(inner_text_with_emojis)

							# Remover o código de inserção do emoji da string
							emoji_pattern = re.compile(r'[^\s]*&&')
							message = emoji_pattern.sub(r'', message)
							message_slice = emoji_pattern.sub(r'', message_slice)


						# Voltar para a caixa de texto
						self.await_by('char')
						chat_box.click()

						self.await_by('char')
						self.gotoEnd()

						press_tab = False

						print('Emoji inserido com sucesso.')

						continue

					# Não pressionou tab, desativar
					if (press_tab):
						press_tab = False

					press_tab = True
					continue

				# Se o caractere não for digitado, tentar novamente
				while ((len(inner_text) < 1) or (char != inner_text[-1]) or (char == last_char)):
					chat_box.send_keys(char)

					self.await_by('char')
					inner_text_with_emojis = chat_box_value \
						.get_attribute('innerText') \
						.replace('\n', '')
					inner_text = removeAllEmojis(inner_text_with_emojis)

					# Se o último caractere digitado for igual ao caractere atual
					if (char == last_char):
						# Se o caractere foi digitado
						if (
							(len(inner_text) > 0)
							and (char == inner_text[-1])
							and (char == inner_text[-2])
						):
							message_slice += char
							last_char = ''
							continue
					# Se não for igual
					else:
						# Se o caractere foi digitado
						if (
							(len(inner_text) > 0)
							and (char == inner_text[-1])
						):
							message_slice += char
							last_char = ''
							continue

					print(f"Tentando inserir o caractere [{char}] novamente.")
				
				last_char = char

			# Após escrever o trecho de mensagem, aperte Shift+Enter
			self.await_by('char')
			self.breakLine()

		# Selecionar o botão de enviar
		send_button = self.driver \
			.find_element_by_xpath('//span[@data-icon="send"]')
		self.await_by('step')
		send_button.click()

		# Aguardar para o próximo contato
		self.await_by('next')

		return True

	def breakLine(self):
		ActionChains(self.driver) \
			.key_down(Keys.SHIFT) \
			.key_down(Keys.ENTER) \
			.key_up(Keys.ENTER) \
			.key_up(Keys.SHIFT) \
			.perform()

	def gotoEnd(self):
		ActionChains(self.driver) \
			.key_down(Keys.CONTROL) \
			.key_down(Keys.END) \
			.key_up(Keys.END) \
			.key_up(Keys.CONTROL) \
			.perform()

	def await_by(self, type):
		if (type == 'char'):
			return time.sleep(
				random.uniform(
					float(self.timing['minCharWait']),
					float(self.timing['maxCharWait'])
				) # uniform
			) # sleep

		if (type == 'step'):
			return time.sleep(
				random.uniform(
					float(self.timing['minStepWait']),
					float(self.timing['maxStepWait'])
				) # uniform
			) # sleep

		if (type == 'next'):
			return time.sleep(
				random.uniform(
					float(self.timing['minNextWait']),
					float(self.timing['maxNextWait'])
				) # uniform
			) # sleep

		return 1
