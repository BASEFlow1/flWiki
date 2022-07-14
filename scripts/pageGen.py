import json
from pyperclip import copy
from os import getcwd

def loadData(filename):
    with open(f"{getcwd()}\\{filename}", "r") as file:
        data = json.load(file)
    return data

classToWikiType = {
    "Light Fighter" : "L_FIGHTER",
    "Heavy Fighter" : "H_FIGHTER",
    "Very Heavy Fighter" : "VH_FIGHTER",
    "Super Heavy Fighter" : "SH_FIGHTER",
    "Bomber" : "BOMBER",
    "Gunship" : "GUNBOAT",
    "Gunboat" : "GUNBOAT",
    "Cruiser" : "CRUISER",
    "Battlecruiser" : "BATTLECRUISER",
    "Battleship" : "BATTLESHIP",
    "Dreadnought" : "DREADNOUGHT",
    "Carrier" : "CARRIER",
    "Freighter" : "FREIGHTER",
    "Liner" : "LINER",
    "Transport" : "TRANSPORT",
    "Destroyer" : "CRUISER",
    "Repair Ship" : "FREIGHTER",
    "Train" : "TRANSPORT",
    "Super Train" : "TRANSPORT",
    "Heavy Transport" : "TRANSPORT"
}


def resetTemplates(template):
    match template:
        case "Ship":
            infobox = "{{Ship Infobox\n| name = {name}\n| image = {image}\n| nickname = {nickname}\n| shipclass = {class}\n| shipowner = {{House Link | {built_by}}}\n| shiptechcategory = {techcompat}\n| techmix = {techcompat}\n| guns = {gunCount}\n| turrets = {turretCount}\n| torpedoes = {torpedoCount}\n| mines = {mineCount}\n| CM = {cmCount}\n| hull = {hull}\n| cargo = {cargo}\n| maxregens = {regens}\n| optwepclass = {optwep}\n| maxwepclass = {maxwep}\n| maxshieldclass = {maxShield}\n| maxspeed = {impulse_speed}| maxturn = {turnRate}\n| maxthrust = {maxthrust}\n| maxpower = {power_output}\n| maxcruise = {maxCruise}\n| recharge = {power_recharge}\n| hullcost = {hull_price}\n| fullcost = {package_price}\n}}\n\n"
            infocard = "{infocard}\n\n"
            handling = "==Handling==\n{handling}\n"
            hardpoints = "==Hardpoints==\n{hardpoints}\n"
            includes = "==Purchase Includes==\n{{Spoiler|\n{includes}\n}}\n\n"
            availability = "==Availability==\n{| class=\"wikitable collapsible collapsed\"\n!Spoiler: Buying Locations\n|-\n|\n{| class=\"wikitable sortable\"\n|-\n!Base!!Owner!!System!!Location\n{sold_at}\n|}\n|}"
            category = "\n[[Category: {built_by}]]"
            return infobox, infocard, handling, hardpoints, includes, availability, category
        case _:
            return 1

while True:
    data = loadData("flData.json")
    infobox, infocard, handling, hardpoints, includes, availability, category = resetTemplates("Ship")
    while True:
        name = str(input("Enter ship name (as displayed in FLStat): "))
        try:
            if data["Ships"][name]:
                break
        except:
            print("Ship name could not be found in database, retrying...")
    image = str(input("Enter image name (copy-paste from page source): "))
    if image == "":
        image = "li_fighter.png"
        print(f"No Image has been specified, defaulting to {image}")
    elif image.lower() == "nickname":
        image = f'{data["Ships"][name]["nickname"]}.png'
        print("Using Ship's nickname as image name.")

    infobox = infobox.replace("{name}", data["Ships"][name]["longName"])
    infobox = infobox.replace("{image}", image)
    infobox = infobox.replace("{nickname}", data["Ships"][name]["nickname"])
    infobox = infobox.replace("{class}", classToWikiType[data["Ships"][name]["type"]])
    if data["Ships"][name]["built_by"] != "":
        infobox = infobox.replace("{built_by}", data["Ships"][name]["built_by"])
    else:
        built = str(input("Enter ship owner faction: "))
        infobox = infobox.replace("{{House Link | {built_by}}}", f"[[{built}]]")
    infobox = infobox.replace("{techcompat}", data["Ships"][name]["techcompat"])
    infobox = infobox.replace("{gunCount}", str(data["Ships"][name]["gunCount"]))
    infobox = infobox.replace("{turretCount}", str(data["Ships"][name]["turretCount"]))
    infobox = infobox.replace("{torpedoCount}", str(data["Ships"][name]["torpedoCount"])) if data["Ships"][name]["torpedoCount"] != 0 else infobox.replace("{torpedoCount}", "")
    infobox = infobox.replace("{mineCount}", str(data["Ships"][name]["mineCount"])) if data["Ships"][name]["mineCount"] != 0 else infobox.replace("{mineCount}", "")
    infobox = infobox.replace("{cmCount}", str(data["Ships"][name]["cmCount"])) if data["Ships"][name]["cmCount"] != 0 else infobox.replace("{cmCount}", "")
    infobox = infobox.replace("{maxthrust}", str(data["Ships"][name]["maxThrust"]))
    infobox = infobox.replace("{hull}", str(data["Ships"][name]["hit_pts"]))
    infobox = infobox.replace("{cargo}", str(data["Ships"][name]["hold_size"]))
    infobox = infobox.replace("{regens}", str(data["Ships"][name]["bat_limit"]))
    infobox = infobox.replace("{optwep}", str(data["Ships"][name]["maxClass"]))
    infobox = infobox.replace("{maxwep}", str(data["Ships"][name]["maxClass"]))
    infobox = infobox.replace("{maxShield}", str(data["Ships"][name]["maxShield"]))
    infobox = infobox.replace("{impulse_speed}", str(data["Ships"][name]["impulse_speed"]))
    infobox = infobox.replace("{turnRate}", str(data["Ships"][name]["turnRate"]))
    infobox = infobox.replace("{power_output}", str(data["Ships"][name]["power_output"]))
    infobox = infobox.replace("{maxCruise}", str(data["Ships"][name]["maxCruise"]))
    infobox = infobox.replace("{power_recharge}", str(data["Ships"][name]["power_recharge"]))
    infobox = infobox.replace("{hull_price}", str(data["Ships"][name]["hull_price"]))
    infobox = infobox.replace("{package_price}", str(data["Ships"][name]["package_price"]))


    info = data["Ships"][name]["infocard"].split("\n", 1)[1]
    while True:
        if info[0].isspace():
            info = info[1:len(info)]
        else:
            break
    infocard = infocard.replace("{infocard}", info)

    handle = data["Ships"][name]["maneuverability"].replace("\n", "\n* ")
    if data["Ships"][name]["mustUseMoors"] == True:
        handle.replace('*', '**')
        handle = f"* This ship is too large to use docking bays, it must use mooring points.{handle}"
        handling = handling.replace("{handling}", handle)
    else:
        handling = handling.replace("{handling}", handle)


    hardpoint = ""
    for x in data["Ships"][name]["hardpoints"]:
        if "Cruiser Shield Upgrade" in x:
            x = x.replace("Cruiser Shield Upgrade", "Shield Harmonic Reinforcement")
        try:
            if "Gun" in x:
                temp = x.split("(")[1]
                temp = temp.split(")")[0]
                temp = temp.replace(" ", "_")
                temp2 = x.split("[[")[1]
                temp2 = temp2.split("]]")[0]
                #print(f"* [[{temp}_Guns|{temp2}]]")
                x = x.replace(temp2, f"{temp}_Guns|{temp2}")
        except IndexError:
            pass
        hardpoint = hardpoint + x + "\n"
    hardpoints = hardpoints.replace("{hardpoints}", hardpoint)

    include = ""
    temp = ""
    for x in data["Ships"][name]["equipment"]:
        number = "{:,}".format(x[1])
        if "Shield" in x[0]:
            temp = x[0].split("[[")[1]
            temp = temp.split("]]")[0]
            x[0] = x[0].replace(temp, f"Shields|{temp}")
        elif "Armor" in x[0]:
            temp = x[0].split("[[")[1]
            temp = temp.split("]]")[0]
            x[0] = x[0].replace(temp, f"Armor_Upgrades|{temp}")
        include = f"{include}{x[0]} (${number})\n"
    includes = includes.replace("{includes}", include)

    available = ""
    for x in data["Ships"][name]["sold_at"]:
        if x[3] == "Independent":
            x[3] = "Independent Worlds"
        available = f"{available}|-\n|[[{x[0]}]]||[[{x[1]}]]||[[{x[2]}]]||[[{x[3]}]]\n"
    availability = availability.replace("{sold_at}", available)

    if data["Ships"][name]["built_by"] != "":
        category = category.replace("{built_by}", data["Ships"][name]["built_by"])
    else:
        category = ""
    if handle != "":
        copy(f"{infobox}{infocard}{handling}{hardpoints}{includes}{availability}{category}")
    else:
        copy(f"{infobox}{infocard}{hardpoints}{includes}{availability}{category}")
    print("Page source copied to clipboard.")

    repeat = input("Generate another page? (yes/No): ")
    if repeat == "":
        break
    elif 'y' in repeat.lower():
        pass
    elif 'n' in repeat.lower():
        break