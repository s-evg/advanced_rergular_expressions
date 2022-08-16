import csv, re


def read(file):
    with open(file, "r", encoding="utf-8") as filecsv:
        rows = csv.reader(filecsv)
        return list(rows)


def clear(contacts_list):
    contacts_dict = {}
    key_contact = contacts_list.pop(0)
    for contact in contacts_list:
        fio = [x.strip() for x in ' '.join(contact[:3]).split(' ', 2)]
        new_contact = fio + contact[3:]
        key = ' '.join(fio[:2])
        contacts_dict.setdefault(key, {i: None for i in key_contact})

        for index, value in enumerate(new_contact):
            if value and not contacts_dict[key][key_contact[index]]:
                contacts_dict[key][key_contact[index]] = value
            elif value and contacts_dict[key][key_contact[index]] != value:
                contacts_dict[key][key_contact[index]] += f';{value}'
        pattern = r'(\+7|8)?\s*\(?(\d+)\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})((\s*)\(?(доб\.)\s*(\d+)\)?)?'
        subst = r'+7(\2)\3-\4-\5\7\8\9'
        contacts_dict[key]['phone'] = re.sub(pattern, subst, contacts_dict[key]['phone'])

    clear_contacts_list = [key_contact]
    for value in contacts_dict.values():
        clear_contacts_list += [[value[i] for i in key_contact]]

    return clear_contacts_list


def write(clear_contacts_list):
    with open("phonebook.csv", "w", encoding="utf-8") as filecsv:
        filewriter = csv.writer(filecsv, delimiter=",")
        filewriter.writerows(clear_contacts_list)


def main(file):
    contacts_list = read(file)
    clear_contact_list = clear(contacts_list)
    write(clear_contact_list)


if __name__ == '__main__':
    main("phonebook_raw.csv")
