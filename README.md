# BOT para WhatsApp Web

## Configuração

Este bot não precisa de APIs terceiras para funcinar, mas precisa de alguns requisitos para funcionar:

- Baixar o [ChromeDriver](https://chromedriver.chromium.org/) e coloca-lo na pasta do projeto.
- Instalar as seguintes bibliotecas Python utilizando o `pip3 install`:

	- PySimpleGUI         4.19.0 [Documentação](https://pysimplegui.readthedocs.io/en/latest/) -> `# pip3 install pysimplegui`
	- selenium            3.141.0 [Documentação](https://www.selenium.dev/documentation/en/webdriver/keyboard/) -> `# pip3 install selenium`

- Você ainda pode precisar instalar a biblioteca `python3-tk` para o funcionamento da interface. Por exemplo:

	- `# sudo apt install python3-tk`
	- `# sudo pacman -S python3-tk`

- No arquivo `main.py` altere a importação do `chromedriver` para o diretótio onde está o executável caso esteja em um diretório diferente ou nome diferente, mas recomendamos manter o padrão, o arquivo deve estar exatamente nomeado como `chromedriver` e deve também estar no diretório raiz do projeto.

## Utilizando

Para iniciar, basta utilizar o comando no terminal, dentro do diretório do projeto:

> `# python3 main.py`

A seguinte janela será exibida:

![Tela do Aplicativo](.github/screen.png)

Informe a mensagem que quiser e no campo contatos, informe uma lista de nomes, um nome em cada linha, que deve estar exatamente como o nome do contato que aparece no chat do WhatsApp.

Clicando em iniciar uma nova janela do chrome será aberta, e você terá 30 segundos para scanear o QR code. Então o BOT manda a mensagem para todos os contatos listados em intervalos diferentes.

Você pode usar o computador para outras atividades e também utilizar o WhatsApp no celular enquanto o BOT está funcionando.

A configuração padrão de intervalos enviará uma média de 60 mensagens por hora, abaixar os intervalos enviará mais mensagens, porém exige que você tenha um bom computador e que não esteja executando tarefas intensivas durante a sua utilização.

