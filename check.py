
import json


def netscape_to_json(filename, path, file_name_without_extension):
    x = f"Cookies//{file_name_without_extension}//" + filename
    # x = filename
    myfile = open(x, "r")
    cookie = []
    myline = myfile.readlines()
    for line in myline:
        key = {}
        x = line.split()
        try:
            key['domain'] = x[0]
            key['httpOnly'] = x[1] == "TRUE"
            key['path'] = x[2]
            key['secure'] = x[3] == "TRUE"

            key['expirationDate'] = int(x[4])
            key['name'] = x[5]
            key['value'] = x[6]
            cookie.append(key)
        except:
            continue
    myfile.close()
    filepath = path + filename
    file1 = open(filepath, 'w')
    file1.writelines(str(json.dumps(cookie, indent=2)))
    file1.close()

