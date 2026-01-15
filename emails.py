

from openpyxl import load_workbook

def send_bulk_emails(email_dict, sample_email):
	#print(email_dict)
	for email,children in email_dict.items():
		print(f'to {email}:')
		
		cstr = children_list_to_str(children)
		this_email = sample_email.replace('{children}', cstr)
		print(this_email)
		#for child in children:
		#	print(f'{child}, ')

def children_list_to_str(names):
	cstr = ''
	for child in names:
		if child == names[-1]:
			cstr += child
		elif child == names[len(names)-2]:
			cstr += f'{child} and '
		else:
			cstr += f'{child}, '
	return cstr

#converts the list of lists into a dictionary, with shared
#email users as a list
def email_list_to_dict(path):

	students_and_emails = read_email_list(path)

	mydict = {}
	for v,k in students_and_emails:
		mydict.setdefault(k, [])
		mydict[k].append(v)
	return mydict

def read_email_list(path):
	workbook = load_workbook(filename=path)

	# Select the desired sheet
	sheet = workbook.active

	# Use list comprehension with iter_rows to get all values
	# values_only=True extracts the cell's value directly, not the cell object
	data_as_list = [row for row in sheet.iter_rows(values_only=True)]

	return data_as_list


d = email_list_to_dict('dummy_emails.xlsx')
sample_email = 'To whom it may concern:\nReport card(s) for {children} are attached below!\n'
send_bulk_emails(d, sample_email)
