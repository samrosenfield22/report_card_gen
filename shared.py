

def file_read_ifnot_create(path):
	content = ''
	try:
		with open(path, "r", encoding='utf-8') as file:
			content = file.read()
	except FileNotFoundError:
		open(path, 'w+', encoding='utf-8')
	return content

def file_write(path, text):
	with open(path, "w+", encoding='utf-8') as file:
		file.write(text)
