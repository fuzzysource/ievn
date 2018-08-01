def tba_power(power_string):
    if power_string in ("0", ""):
        return 0
    else:
        power_string = power_string.replace('x','*')
        return eval(power_string)

def split_row(row):
    return row.split(",")

def row_type(row):
    if (split_row(row)[0] == "tba"):
        return "tba"
    else:
        return "xa"

def tba_from_row(tba_row):
    tba_properties = ['type', 'name', 'owner',
                      'v0', 'v1', 'v2',
                      'p0', 'p1', 'p2']
    return {val: split_row(tba_row)[i]
            for i, val in enumerate(tba_properties)}

def xa_from_row(row):
    xa_properties = ['type', 'name']
    return {val: split_row(row)[i]
            for i, val in enumerate(xa_properties)}

def new_xa(row):
    xa = xa_from_row(row)
    return {
        "name": xa["name"],
        "tbas": []
    }

def update_xa(xa_list, tba):
    xa_list["tbas"].append(tba)
    return xa_list

def xa_data(data):
    current_xa = {}
    xas = []
    for row in data:
        if row_type(row) == "xa":
            current_xa = new_xa(row)
            xas.append(current_xa)
        else:
            current_xa = update_xa(current_xa,
                                   (tba_from_row(row)))
    return xas

def count_group_mba(power_string):
    g = power_string
    if (g in ("0", "")):
        return 0
    elif "x" in g:
        return eval(g.split("x")[0])
    else:
        return 1

def count_mba(power_string):
    n = 0
    for i in power_string.split("+"):
        n = n + count_group_mba(i)
    return n

def get_change_type_tba(v1, v2, p1, p2):
    c1, c2 = count_mba(p1), count_mba(p2)
    pv1, pv2 = tba_power(p1), tba_power(p2)
    if (c2 > c1):
        return {"type" : "new_tba",
                "num": c2 - c1,
                "power": pv2 - pv1,
                "voltage": v2
        }
    elif (v1 != v2 or pv2 > pv1):
        return {
            "type": "upgrade_tba",
            "num": c2,
            "power": pv2,
            "voltage": v2
        }
    else:
        return {
            "type": "nothing",
            "num": 0,
            "power": 0,
            "voltage": v2
        }

def init_xa_result(name):
    return  {
        "name": name,
        "GD1": {
            "DL":{
                "New": {"22/0.4": {"num": 0,
                                   "power": 0},
                        "Other": {"num": 0,
                                  "power": 0}},
                "Upgrade": {"22/0.4": {"num": 0,
                                       "power": 0},
                            "Other": {"num": 0,
                                      "power": 0}}
            },
            "KH":{
                "New": {"22/0.4": {"num": 0,
                                   "power": 0},
                        "Other": {"num": 0,
                                  "power": 0}},
                "Upgrade": {"22/0.4": {"num": 0,
                                       "power": 0},
                            "Other": {"num": 0,
                                      "power": 0}}
            }
        },
        "GD2": {
            "DL":{
                "New": {"22/0.4": {"num": 0,
                                   "power": 0},
                        "Other": {"num": 0,
                                  "power": 0}},
                "Upgrade": {"22/0.4": {"num": 0,
                                       "power": 0},
                            "Other": {"num": 0,
                                      "power": 0}}
            },
            "KH":{
                "New": {"22/0.4": {"num": 0,
                                   "power": 0},
                        "Other": {"num": 0,
                                  "power": 0}},
                "Upgrade": {"22/0.4": {"num": 0,
                                       "power": 0},
                            "Other": {"num": 0,
                                      "power": 0}}
            }
        },                                    
    }

def aggregate_xa(xa):
    tbas = xa["tbas"]
    result = init_xa_result(xa["name"])
    for tba in tbas:
        owner = tba["owner"]
        name = tba["name"]
        v0, v1, v2 = tba["v0"], tba["v1"], tba["v2"]
        p0, p1, p2 = tba["p0"], tba["p1"], tba["p2"]
        change_gd1 = get_change_type_tba(v0,v1, p0, p1)
        change_gd2 = get_change_type_tba(v1,v2, p1, p2)
        v1 = "Other" if v1 != "22/0.4" else v1
        v2 = "Other" if v2 != "22/0.4" else v2
        if (change_gd1["type"] == "new_tba"):
            result["GD1"][owner]["New"][v1]["num"] += change_gd1["num"]
            result["GD1"][owner]["New"][v1]["power"] += change_gd1["power"]
        elif (change_gd1["type"] == "upgrade_tba"):
            result["GD1"][owner]["Upgrade"][v1]["num"] += change_gd1["num"]
            result["GD1"][owner]["Upgrade"][v1]["power"] += change_gd1["power"]
        if (change_gd2["type"] == "new_tba"):
            result["GD2"][owner]["New"][v2]["num"] += change_gd2["num"]
            result["GD2"][owner]["New"][v2]["power"] += change_gd2["power"]
        elif (change_gd2["type"] == "upgrade_tba"):
            result["GD2"][owner]["Upgrade"][v2]["num"] += change_gd2["num"]
            result["GD2"][owner]["Upgrade"][v2]["power"] += change_gd2["power"]
    return result

def aggregate_all_xas(xas):
    result = []
    for xa in xas:
        result.append(aggregate_xa(xa))
    return result
        
def read_file(file_name):
    with open(file_name,'r') as f:
        data = f.read().replace("/0,4", "/0.4").replace("ĐL", "DL")
        f.close()
        return data

def main():
    file_name = input("File Name: ")
    data = read_file(file_name)
    xas = xa_data(data.splitlines())
    result = aggregate_all_xas(xas)
    print(result)

if __name__ == "__main__":
    main()
