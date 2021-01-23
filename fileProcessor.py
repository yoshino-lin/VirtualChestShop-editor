from glob import glob
import yaml

#购买的slot
def writeBuySlot(dictToSave,slotId,name,itemID,amount,price,specialId):
    dictToSave["virtualchest"]["Slot{}".format(slotId)] = [{
        "Item":{
            "Count": amount,
            "ItemType": itemID,
            "UnsafeDamage":specialId,
            "DisplayName": "&a购买：{}".format(name),
            "ItemLore": ["&a价格：${}".format(price)],
        },
        "PrimaryAction": {
            "Command": "cost: {0}; console: give %player_name% {1} {2}".format(price,itemID,amount) if specialId == 0 else "cost: {0}; console: give %player_name% {1} {2} {3}".format(price,itemID,amount,specialId)
        },
        "KeepInventoryOpen": True,
        "Requirements": "%economy_balance% >= {}".format(price)
        },{
        "Item": {
            "Count":amount,
            "ItemType": itemID,
            "UnsafeDamage": specialId,
            "DisplayName": "&a购买：{}".format(name),
            "ItemLore": [
                "&a价格：${}".format(price),
                "&c你没有足够的金币！"
            ]
        }
    }]

#出售的slot
def writeSellSlot(dictToSave,slotId,name,itemID,amount,price,specialId):
    dictToSave["virtualchest"]["Slot{}".format(slotId)] = {
        "Item": {
            "Count":amount,
            "ItemType":itemID,
            "UnsafeDamage": specialId,
            "DisplayName":  "&c出售：{}".format(name),
            "ItemLore": ["&c价格：${}".format(price)]
        },
        "PrimaryAction": {
            "Command": "cost-item: {0}; cost: -{1}".format(amount,price),
            "HandheldItem": {
                "SearchInventory": True,
                "ItemType": itemID,
                "UnsafeDamage": specialId,
                "Count": amount
            },
            "KeepInventoryOpen": True
        }
    }

#整理yaml
def yamlOrganize(saveAsUnicode=True):
    for path in glob("config/*.yaml"):
        with open(path, "r", encoding='utf-8') as f:
            data = yaml.load(f.read(),Loader=yaml.FullLoader)
        with open(path, "w", encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=saveAsUnicode)