import os
import shutil
from vc_basic import *

"""基本参数设置"""
#分割线开始的Slot的ID
cutLineStartID = 18
cutLineEndID = 26
#出售价格 = 购买价格 / sell_price_deduct
sell_price_deduct = 4

ColorsIdList = [2, 3, 4, 5, 6, 7,  9, 'a', 'b', 'c', 'd', 'e', 'f']

#重建menu文件夹
path = "menu"
if os.path.exists(path): shutil.rmtree(path)
os.makedirs(path)

#整理yaml
yamlOrganize()

#读取config里的配置文件
allShopData = {}
#读取文件
for filePath in glob("config/*.yaml"):
    with open(filePath, "r", encoding='utf-8') as f:
        DATA = yaml.load(f.read(),Loader=yaml.FullLoader)
        allShopData[DATA["id"]] = DATA
        allShopData[DATA["id"]]["file_name"] = filePath.replace(".yaml","").replace("config\\","")

#写入超市主菜单
dictToSave = {
    "virtualchest": {
        "TextTitle": "&6在线超市-请选择商品种类",
        "Rows": 6,
        "UpdateIntervalTick": 20,
        "AcceptableActionIntervalTick": 20,
        "Slot53": createSlot(
            1,
            "&f返回",
            ["&7点击此处返回上一个菜单"],
            "minecraft:redstone",
            Command = "vc o main",
        )
    }
}
for key,value in allShopData.items():
    dictToSave["virtualchest"]["Slot"+str(value["id"]*2)] = createSlot(
        1,
        "&{0}{1}".format(ColorsIdList[value["id"]],value["MenuName"]),
        ["&7点击此处进入对应菜单"],
        value["ItemIcon"],
        Command = "vc o {}".format(value["file_name"])
    )
#写入数据
dump("menu/shop_choose.conf",dictToSave)


for key,DATA in allShopData.items():
    sellMode = DATA["sellMode"]
    slotNum = 0
    #数据模版
    dictToSave = {"virtualchest": {
        "TextTitle": "&a请选择你想要购买的物品",
        "Rows": 6,
        "UpdateIntervalTick": 20,
        "AcceptableActionIntervalTick": 20,
        "Slot49": createSlot(
            1,
            "&6你的当前余额:&f%economy_balance%",
            ["&d点击此处返回到选择菜单"],
            "minecraft:name_tag",
            Command = "vc o shop_choose"
        )
    }}
    #上一页的按钮
    if DATA["id"]-1 in allShopData:
        dictToSave["virtualchest"]["Slot45"] = createSlot(
            1,
            "&{0}上一页:{1}".format(ColorsIdList[DATA["id"]-1],allShopData[DATA["id"]-1]["MenuName"]),
            ["&7点击此处进入对应菜单"],
            allShopData[DATA["id"]-1]["ItemIcon"],
            Command = "vc o {}".format(allShopData[DATA["id"]-1]["file_name"]),
        )
    else:
        dictToSave["virtualchest"]["Slot45"] = createSlot(
            1,
            "&c上一页:没有了",
            ["&d点击此处返回到选择菜单"],
            "minecraft:barrier",
            Command = "vc o shop_choose"
        )
    #下一页的按钮
    if DATA["id"]+1 in allShopData: dictToSave["virtualchest"]["Slot53"] = createSlot(
        1,
        "&{0}下一页:{1}".format(ColorsIdList[DATA["id"]+1],allShopData[DATA["id"]+1]["MenuName"]),
        ["&7点击此处进入对应菜单"],
        allShopData[DATA["id"]+1]["ItemIcon"],
        Command = "vc o {}".format(allShopData[DATA["id"]+1]["file_name"])
    )
    #分割线
    if sellMode:
        for i in range(cutLineStartID,cutLineEndID+1):
            dictToSave["virtualchest"]["Slot{}".format(i)] = createSlot(
                1,
                "&e这里是萌萌哒的分割线哦",
                ["&7上方为购买区,下方为出售区"],
                "minecraft:stained_glass_pane",
                5,
                KeepInventoryOpen=True
            )
    #写入物品
    for eachItemData in DATA['Items']:
        #初始化名称
        if eachItemData["amount"] == 64:
            eachItemData["name"] = "一组" + eachItemData["name"]
        elif eachItemData["amount"] == 32:
            eachItemData["name"] = "半组" + eachItemData["name"]
        elif eachItemData["amount"] == 12:
            eachItemData["name"] = "一打" + eachItemData["name"]
        elif eachItemData["amount"] == 1:
            eachItemData["name"] = "一块" + eachItemData["name"] if "块" in eachItemData["name"] else "一个" + eachItemData["name"]
        else:
            eachItemData["name"] = "{0}块{1}".format(eachItemData["amount"],eachItemData["name"])\
                if "块" in eachItemData["name"] else "{0}个{1}".format(eachItemData["amount"],eachItemData["name"])
        if "type" not in eachItemData or eachItemData["type"] == "normal":
            if "specialId" not in eachItemData:
                eachItemData["specialId"] = 0
            dictToSave["virtualchest"]["Slot{}".format(slotNum)] = writeBuySlot(
                eachItemData["name"],
                eachItemData["itemID"],
                eachItemData["amount"],
                eachItemData["price"],
                eachItemData["specialId"])
            #出售的slot
            if sellMode: dictToSave["virtualchest"]["Slot{}".format(slotNum+27)] = writeSellSlot(
                eachItemData["name"],
                eachItemData["itemID"],
                eachItemData["amount"],
                eachItemData["price"]/sell_price_deduct,eachItemData["specialId"])
            slotNum+=1
        elif "type" in eachItemData and eachItemData["type"] == "duplicate":
            for i in range(eachItemData["endSpecialId"]+1):
                dictToSave["virtualchest"]["Slot{}".format(slotNum)] = writeBuySlot(
                    eachItemData["name"],
                    eachItemData["itemID"],
                    eachItemData["amount"],
                    eachItemData["price"],
                    i)
                if sellMode: dictToSave["virtualchest"]["Slot{}".format(slotNum+27)] = writeSellSlot(
                    eachItemData["name"],
                    eachItemData["itemID"],
                    eachItemData["amount"],
                    eachItemData["price"]/sell_price_deduct,
                    i)
                slotNum+=1
    dump("menu/{}.conf".format(DATA["file_name"]),dictToSave)