

from openpyxl import load_workbook

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
print(d)
