import json
import os
import re


def _save_items(file_name, data):
    with open(file_name, 'w') as f:
        f.write(json.dumps(data))


def _load_items(file_name):
    with open(file_name, 'r') as f:
        data = json.loads(f.read())
    return data


def _reset_items(file_name):

    os.remove(file_name)


def _get_item_by_name(items, name):
    for group in items:
        for key in items[group]:
            if items[group][key]['name'] == name:
                return group, key, items[group][key]
    return None


def parse_text_from_guild(text):

    lines = text.split('\n')
    if len(lines) == 0 or lines[0] != 'Guild Warehouse:':
        return False

    if os.path.exists('items.json'):
        items = _load_items('items.json')
    else:
        items = _load_items('items_base.json')

    lines.pop(0) # remove header line
    for l in lines:
        m = re.match('([kr0-9]+) ([A-Za-z\' ]+) x (\\d+)', l)
        if m:
            code = m.group(1)
            name = m.group(2)
            amnt = int(m.group(3))

            group = 'recipes' if code[0] == 'r' else 'parts'

            items[group][code]['amnt'] += amnt
            print(items[group][code])

        else:
            print('# GUILD STOCK ERROR #', l)

    print('updating items.json')
    _save_items('items.json', items)

    return True


def parse_text_from_craft(text):

    lines = text.split('\n')

    if os.path.exists('items.json'):
        items = _load_items('items.json')
    else:
        items = _load_items('items_base.json')

    for l in lines:
        # quick fix
        if l[0] == '\xf0':
            l = l[4:]

        m = re.match('\\W*([A-Za-z\' ]+) \\((\\d+)\\)', l)
        if m:
            name = m.group(1)
            amnt = int(m.group(2))
            
            group, code, item = _get_item_by_name(items, name)
            if not item is None:
                items[group][code]['amnt'] += amnt
                print(items[group][code])
            else:
                print('# ERROR ITEM NOT FOUND #', name, amnt)
        else:
            print('# CRAFT ERROR #', l)
            return False

    print('updating items.json')
    _save_items('items.json', items)

    return True


def list_possible_crafts(full=False):

    if os.path.exists('items.json'):
        items = _load_items('items.json')
    else:
        items = _load_items('items_base.json')

    tiers = {'T2': 3, 'T3': 5, 'T4': 6}

    lines = []

    for k_key in items['parts']:
        r_key = k_key.replace('k', 'r')

        name = items['recipes'][r_key]['name'].replace(' recipe', '')
        n_prt = items['parts'][k_key]['amnt']
        n_rec = items['recipes'][r_key]['amnt']

        tier = items['parts'][k_key]['tier']
        prts_needed = tiers[tier]

        can_craft = 0
        if n_rec > 0 and n_prt > 0:
            can_craft = min(n_prt // prts_needed, n_rec)
        can_craft = '' if can_craft == 0 else can_craft

        line = [k_key[1:], n_rec, n_prt, can_craft, name]
        lines.append(line)

    return list(filter(lambda l: l[3] != '', lines)) if not full else lines


if __name__ == '__main__':
   
    text = open('text_from_craft').read()
    parse_text_from_craft(text)

    text = open('text_from_craft2').read()
    parse_text_from_craft(text)