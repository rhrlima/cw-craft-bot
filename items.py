import json


source_file = 'items.json'


ITEMS = None


def _load_items(filename=source_file):
	global ITEMS
	try:
		ITEMS = json.loads(open(filename, 'r').read())
	except:
		print(f'Error while trying to load {filename}')
		ITEMS = {}


def get_item_by_name(item_name):

	for group in ITEMS:
		for code in ITEMS[group]:
			name = ITEMS[group][code]['name']
			if name.lower() == item_name.lower():
				return ITEMS[group][code]
	return {}


def get_item_by_code(item_code):
	
	for group in ITEMS:
		for code in ITEMS[group]:
			if ITEMS[group][code]['code'] == item_code:
				return ITEMS[group][code]
	return {}



if __name__ == '__main__':
	
	ITEMS = load_items(source_file)
	print(ITEMS.keys())

	print(get_item_by_name('Thread'))
	print(get_item_by_name('HARDENER'))
	print(get_item_by_name('Bone powder'))
	print(get_item_by_name('Rubi'))
	
	print(get_item_by_code('02'))
	print(get_item_by_code('32'))
	print(get_item_by_code('999'))