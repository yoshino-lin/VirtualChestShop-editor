from glob import glob
import yaml

#创建一个slot
def createSlot(Count:int, DisplayName:str, ItemLore:list, ItemType:str,
    UnsafeDamage:int = 0, Command:str = None, KeepInventoryOpen:bool = False, Requirements:str = None) -> dict:
    dictReturn = {
        "Item":{
            "Count": Count,
            "DisplayName": DisplayName,
            "ItemLore": ItemLore,
            "ItemType": ItemType,
            "UnsafeDamage":UnsafeDamage,
        },
        "PrimaryAction": {}
    }
    if Command != None: dictReturn["PrimaryAction"]["Command"] = Command
    if Command != None and "vc o" in Command: KeepInventoryOpen = True
    if KeepInventoryOpen: dictReturn["PrimaryAction"]["KeepInventoryOpen"] = True
    #如果PrimaryAction为空，则删除
    if len(dictReturn["PrimaryAction"]) == 0:del dictReturn["PrimaryAction"]
    if Requirements != None: dictReturn["Requirements"] = Requirements
    return dictReturn

#购买的slot
def writeBuySlot(name:str,itemID:str,amount:int,price:int,specialId:int) -> list:
    return [
        createSlot(
            amount,
            "&a购买：{}".format(name),
            ["&a价格：${}".format(price)],
            itemID,
            specialId,
            "cost: {0}; console: give %player_name% {1} {2}".format(price,itemID,amount) if specialId == 0 else "cost: {0}; console: give %player_name% {1} {2} {3}".format(price,itemID,amount,specialId),
            True,
            "%economy_balance% >= {}".format(price)
        ),
        createSlot(
            amount,
            "&a购买：{}".format(name),
            ["&a价格：${}".format(price),"&c你没有足够的金币！"],
            itemID,
            specialId
        )
    ]

#出售的slot
def writeSellSlot(name:str,itemID:str,amount:int,price:int,specialId:int) -> dict:
    slotDict = createSlot(
        amount,
        "&c出售：{}".format(name),
        ["&c价格：${}".format(price)],
        itemID,
        specialId,
        "cost-item: {0}; cost: -{1}".format(amount,price),
        True
        )
    slotDict["PrimaryAction"]["HandheldItem"] = {
        "SearchInventory": True,
        "ItemType": itemID,
        "UnsafeDamage": specialId,
        "Count": amount
    }
    return slotDict

#整理yaml
def yamlOrganize(saveAsUnicode=True):
    for path in glob("config/*.yaml"):
        with open(path, "r", encoding='utf-8') as f:
            data = yaml.load(f.read(),Loader=yaml.FullLoader)
        with open(path, "w", encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=saveAsUnicode)

#按照times给string加缩进（空格）
def _addIndent(str_input:str,times:int,tab_space:int=2):
    for i in range(times*tab_space):
        str_input += " "
    return str_input

#处理string的模块
def _dictConverter(stringToWrite:str,dictToSave:dict,layer:int=0) -> str:
    for key in sorted(dictToSave):
        value = dictToSave[key]
        #如果值是列表
        if isinstance(value,dict):
            stringToWrite = _addIndent(
                _dictConverter(_addIndent(stringToWrite,layer)+key+" = {\n",value,layer+1)
                ,layer) + "}\n"
        #如果值是列表
        elif isinstance(value,list):
            stringToWrite = _addIndent(
                _listConverter(_addIndent(stringToWrite,layer)+key+" = [\n",value,layer+1),
                layer) + "]\n"
        #如果值是bool
        elif isinstance(value,bool):
            if value:
                stringToWrite = _addIndent(stringToWrite,layer) + '{0} = {1}\n'.format(key,"true")
            else:
                stringToWrite = _addIndent(stringToWrite,layer) + '{0} = {1}\n'.format(key,"false")
        #如果值是int
        elif isinstance(value,int):
            stringToWrite = _addIndent(stringToWrite,layer) + "{0} = {1}\n".format(key,value)
        #如果值是str
        elif isinstance(value,str):
            stringToWrite = _addIndent(stringToWrite,layer) + '{0} = "{1}"\n'.format(key,value)
        else:
            raise  Exception("Warning: Cannot recognize value {}'s data type!".format(value))
    return stringToWrite

def _listConverter(stringToWrite:str,listToSave:dict,layer:int) -> str:
    for value in listToSave:
        #如果值是字典
        if isinstance(value,dict):
            stringToWrite = _addIndent(
                _dictConverter(_addIndent(stringToWrite,layer) + "{\n",value,layer+1),
                layer) + "}\n"
        #如果值是列表
        elif isinstance(value,list):
            stringToWrite = _addIndent(
                _listConverter(_addIndent(stringToWrite,layer)+"[\n",value,layer+1),
                layer) + "]\n"
        #如果值是bool
        elif isinstance(value,bool):
            if value:
                stringToWrite = _addIndent(stringToWrite,layer)+'{}\n'.format("true")
            else:
                stringToWrite = _addIndent(stringToWrite,layer)+'{}\n'.format("false")
        #如果值是int
        elif isinstance(value,(int,str)):
            stringToWrite = _addIndent(stringToWrite,layer) + '"{}"\n'.format(value)
        else:
            raise  Exception("Warning: Cannot recognize value {}'s data type!".format(value))
    return stringToWrite

#保存文件
def dump(path:str,dictToSave:dict) -> None:
    with open(path,"w+",encoding='utf-8') as f: f.write(_dictConverter("",dictToSave))