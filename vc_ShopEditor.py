import yaml
import os
from glob import glob
from fileProcessor import *
#检测是否有menu文件夹
if not os.path.exists("menu"):
    os.makedirs("menu") 

#分割线开始的Slot的ID
cutLineStartID = 18
cutLineEndID = 26

#读取config里的配置文件
allShopFiles = glob("config/*.yaml")
allShopData = {}
#读取文件
for filePath in allShopFiles:
    with open(filePath, "r", encoding='utf-8') as f:
        DATA = yaml.load(f.read(),Loader=yaml.FullLoader)
        allShopData[DATA["id"]] = DATA
        allShopData[DATA["id"]]["file_name"] = filePath.replace(".yaml","").replace("config\\","")

with open("menu/shop_choose.conf","w+",encoding='utf-8') as f:
    f.write('virtualchest {\n  TextTitle = "&6在线超市-请选择商品种类"\n  Rows = 6\n  UpdateIntervalTick = 20\n  AcceptableActionIntervalTick = 20\n')
    
    for key,value in allShopData.items():
        f.write('  Slot'+str(value["id"]*2)+' = {\n    Item {\n	  Count = 1\n	  ItemType = "'+value["ItemIcon"]+'"\n	  UnsafeDamage = 0\n      DisplayName = "&'+value["Color"]+value["MenuName"]+'"\n	}\n	PrimaryAction {Command = "vc o '+value["file_name"]+'"}\n  }\n')
    f.write('  Slot53 =  {\n    Item {\n	  Count = 1\n	  ItemType = "minecraft:redstone"\n	  UnsafeDamage = 0\n      DisplayName = "&f返回"\n      ItemLore = ["&7点击此处返回上一个菜单"]\n    }\n	PrimaryAction {Command = "vc o main"}\n	KeepInventoryOpen = true\n  }\n}')

for key,DATA in allShopData.items():
    file_name = DATA["file_name"]
    Items = DATA['Items']
    sellMode = DATA["sellMode"]
    slotNum = 0
    with open("menu/"+file_name+".conf","w+",encoding='utf-8') as f:
        f.write('virtualchest {\n')
        f.write('  TextTitle = "&a请选择你想要购买的物品"\n')
        f.write('  Rows = 6\n  UpdateIntervalTick = 20\n  AcceptableActionIntervalTick = 20\n')
        
        for eachItemData in Items:
            if "type" not in eachItemData or eachItemData["type"] == "normal":
                #初始化名称
                if eachItemData["amount"] == 64:
                    eachItemData["name"] = "一组"+eachItemData["name"]
                elif eachItemData["amount"] == 32:
                    eachItemData["name"] = "半组"+eachItemData["name"]
                elif eachItemData["amount"] == 12:
                    eachItemData["name"] = "一打"+eachItemData["name"]
                elif eachItemData["amount"] == 1:
                    eachItemData["name"] = "一块"+eachItemData["name"]
                else:
                    eachItemData["name"] = str(eachItemData["amount"])+"块"+eachItemData["name"]
                if "specialId" not in eachItemData:
                    eachItemData["specialId"] = 0
                writeBuySlot(f,slotNum,eachItemData["name"],eachItemData["itemID"],eachItemData["amount"],eachItemData["price"],eachItemData["specialId"])
                #出售的slot
                if sellMode == True:
                    writeSellSlot(f,slotNum+27,eachItemData["name"],eachItemData["itemID"],eachItemData["amount"],eachItemData["price"]/2,eachItemData["specialId"])
                slotNum+=1
            if "type" in eachItemData and eachItemData["type"] == "duplicate":
                #初始化名称
                if eachItemData["amount"] == 64:
                    eachItemData["name"] = "一组"+eachItemData["name"]
                elif eachItemData["amount"] == 32:
                    eachItemData["name"] = "半组"+eachItemData["name"]
                elif eachItemData["amount"] == 12:
                    eachItemData["name"] = "一打"+eachItemData["name"]
                elif eachItemData["amount"] == 1:
                    eachItemData["name"] = "一个"+eachItemData["name"]
                else:
                    eachItemData["name"] = str(eachItemData["amount"])+"个"+eachItemData["name"]
                for i in range(eachItemData["endSpecialId"]+1):
                    writeBuySlot(f,slotNum,eachItemData["name"],eachItemData["itemID"],eachItemData["amount"],eachItemData["price"],i)
                    if sellMode == True:
                        writeSellSlot(f,slotNum+27,eachItemData["name"],eachItemData["itemID"],eachItemData["amount"],eachItemData["price"]/2,i)
                    slotNum+=1

        if sellMode == True:
            for i in range(cutLineStartID,cutLineEndID+1):
                f.write('  Slot{0} ='.format(i))
                f.write('{\n    Item {\n      Count = 1\n      ItemType = "minecraft:stained_glass_pane"\n')
                f.write('      UnsafeDamage = 5\n      DisplayName = "&e这里是萌萌哒的分割线哦"\n      ItemLore = ["&7上方为购买区,下方为出售区"]\n')
                f.write('    }\n  KeepInventoryOpen = true\n  }\n')
        #上一页的按钮
        if DATA["id"]-1 in allShopData:
            f.write('  Slot45 = {\n    Item {\n      Count = 1\n      ')
            f.write('ItemType = "{2}"\n      UnsafeDamage = 0\n      DisplayName = "&{0}上一页:{1}"\n    '.format(allShopData[DATA["id"]-1]["Color"],allShopData[DATA["id"]-1]["MenuName"],allShopData[DATA["id"]-1]["ItemIcon"]))
            f.write('}\n    PrimaryAction {Command = "vc o '+allShopData[DATA["id"]-1]["file_name"]+'"}\n    KeepInventoryOpen = true\n  }\n')
        else:
            f.write('  Slot45 = {\n    Item {\n      Count = 1\n      ItemType = "minecraft:barrier"\n      UnsafeDamage = 0\n      DisplayName = "&c上一页:没有了"\n    }\n    PrimaryAction {Command = "vc o shop_choose"}\n    KeepInventoryOpen = true\n  }\n')
        #显示余额的按钮
        f.write('  Slot49 = {\n    Item {\n      Count = 1\n      ItemType = "minecraft:name_tag"\n      UnsafeDamage = 0\n      DisplayName = "&6你的当前余额:&f%economy_balance%"\n      ItemLore = ["&d点击此处返回到选择菜单"]\n    }\n    PrimaryAction {Command = "vc o shop_choose"}\n    KeepInventoryOpen = true\n  }\n')
        #下一页的按钮
        if DATA["id"]+1 in allShopData:
            f.write('  Slot53 = {\n    Item {\n      Count = 1\n      ')
            f.write('ItemType = "{2}"\n      UnsafeDamage = 0\n      DisplayName = "&{0}下一页:{1}"\n    '.format(allShopData[DATA["id"]+1]["Color"],allShopData[DATA["id"]+1]["MenuName"],allShopData[DATA["id"]+1]["ItemIcon"]))
            f.write('}\n    PrimaryAction {Command = "vc o '+allShopData[DATA["id"]+1]["file_name"]+'"}\n    KeepInventoryOpen = true\n  }\n')
        f.write('}')
