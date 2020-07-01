import yaml
#读取文件
with open("config.yaml", "r", encoding='utf-8') as f:
    DATA = yaml.load(f.read(),Loader=yaml.FullLoader)
    file_name = DATA["file_name"]
    itemName = DATA["itemName"]
    lastPageItemName = DATA["lastPageItemName"]
    lastPageItemColor = DATA["lastPageItemColor"]
    lastPageItemType = DATA['lastPageItemType']
    lastPageMenuName = DATA['lastPageMenuName']
    nextPageItemName = DATA['nextPageItemName']
    nextPageItemColor = DATA['nextPageItemColor']
    nextPageItemType = DATA['nextPageItemType']
    nextPageMenuName = DATA['nextPageMenuName']
    Items = DATA['Items']

#分割线开始的Slot的ID
cutLineStartID = 18
cutLineEndID = 26
slotNum = 0

with open(file_name,"w+",encoding='utf-8') as f:
    f.write('virtualchest {\n')
    f.write('  TextTitle = "&a请选择你想要购买的{}"\n'.format(itemName))
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
                eachItemData["name"] = "一个"+eachItemData["name"]
            else:
                eachItemData["name"] = str(eachItemData["amount"])+"个"+eachItemData["name"]
            #购买的slot
            f.write('  Slot'+str(slotNum)+' = [{\n')
            f.write('    Item {\n')
            f.write('      Count = {}\n'.format(eachItemData["amount"]))
            f.write('      ItemType = "{}"\n'.format(eachItemData["itemID"]))
            if "specialId" not in eachItemData:
                f.write('      UnsafeDamage = 0\n')
            else:
                f.write('      UnsafeDamage = {}\n'.format(eachItemData["specialId"]))
            f.write('      DisplayName = "&a购买：{}"\n'.format(eachItemData["name"]))
            f.write('      ItemLore = ["&a价格：${}"]\n'.format(eachItemData["price"]))
            f.write('    }\n')
            f.write('    PrimaryAction {\n')
            if "specialId" not in eachItemData:
                f.write('      Command = "cost: {0}; console: give %player_name% {1} {2}"\n'.format(eachItemData["price"],eachItemData["itemID"],eachItemData["amount"]))
            else:
                f.write('      Command = "cost: {0}; console: give %player_name% {1} {2} {30}"\n'.format(eachItemData["price"],eachItemData["itemID"],eachItemData["amount"],eachItemData["specialId"]))
            f.write('      KeepInventoryOpen = true\n')
            f.write('    }\n')
            f.write('    Requirements = "%economy_balance% >= {}"\n'.format(eachItemData["price"]))
            f.write('    }, {\n')
            f.write('    Item {\n')
            f.write('      Count = {}\n'.format(eachItemData["amount"]))
            f.write('      ItemType = "{}"\n'.format(eachItemData["itemID"]))
            if "specialId" not in eachItemData:
                f.write('      UnsafeDamage = 0\n')
            else:
                f.write('      UnsafeDamage = {}\n'.format(eachItemData["specialId"]))
            f.write('      DisplayName = "&a购买：{}"\n'.format(eachItemData["name"]))
            f.write('      ItemLore = [\n')
            f.write('        "&a价格：${}"\n'.format(eachItemData["price"]))
            f.write('        "&c你没有足够的金币！"\n')
            f.write('      ]\n')
            f.write('    }\n')
            f.write('  }]\n')
            #出售的slot
            eachItemData["price"] = int(eachItemData["price"]/2)
            f.write('  Slot'+str(slotNum+27)+' = {\n')
            f.write('    Item {\n')
            f.write('      Count = {}\n'.format(eachItemData["amount"]))
            f.write('      ItemType = "{}"\n'.format(eachItemData["itemID"]))
            if "specialId" not in eachItemData:
                f.write('      UnsafeDamage = 0\n')
            else:
                f.write('      UnsafeDamage = {}\n'.format(eachItemData["specialId"]))
            f.write('      DisplayName = "&c出售：{}"\n'.format(eachItemData["name"]))
            f.write('      ItemLore = ["&c价格：${}"]\n'.format(eachItemData["price"]))
            f.write('    }\n')
            f.write('    PrimaryAction {\n')
            f.write('      Command = "cost-item: {0}; cost: -{1}"\n'.format(eachItemData["amount"],eachItemData["price"]))
            f.write('      HandheldItem {\n')
            f.write('        SearchInventory = true\n')
            f.write('        ItemType = "{}"\n'.format(eachItemData["itemID"]))
            if "specialId" not in eachItemData:
                f.write('        UnsafeDamage = 0\n')
            else:
                f.write('        UnsafeDamage = {}\n'.format(eachItemData["specialId"]))
            f.write('        Count = {}\n'.format(eachItemData["amount"]))
            f.write('      }\n')
            f.write('      KeepInventoryOpen = true\n')
            f.write('    }\n')
            f.write('  }\n')
            slotNum+=1

    for i in range(cutLineStartID,cutLineEndID+1):
        f.write('  Slot{0} ='.format(i))
        f.write('{\n    Item {\n      Count = 1\n      ItemType = "minecraft:stained_glass_pane"\n')
        f.write('      UnsafeDamage = 5\n      DisplayName = "&e这里是萌萌哒的分割线哦"\n      ItemLore = ["&7上方为购买区,下方为出售区"]\n')
        f.write('    }\n  KeepInventoryOpen = true\n  }\n')
    #上一页的按钮
    if lastPageItemName != None and lastPageItemName != "":
        f.write('  Slot45 = {\n    Item {\n      Count = 1\n      ')
        f.write('ItemType = "{2}"\n      UnsafeDamage = 0\n      DisplayName = "&{0}上一页:{1}"\n    '.format(lastPageItemColor,lastPageItemName,lastPageItemType))
        f.write('}\n    PrimaryAction {Command = "vc o '+lastPageMenuName+'"}\n    KeepInventoryOpen = true\n  }\n')
    #显示余额的按钮
    f.write('  Slot49 = {\n    Item {\n      Count = 1\n      ItemType = "minecraft:name_tag"\n      UnsafeDamage = 0\n      DisplayName = "&6你的当前余额:&f%economy_balance%"\n      ItemLore = ["&d点击此处返回到选择菜单"]\n    }\n    PrimaryAction {Command = "vc o shop_choose"}\n    KeepInventoryOpen = true\n  }\n')
    #下一页的按钮
    if nextPageItemName != None and nextPageItemName != "":
        f.write('  Slot53 = {\n    Item {\n      Count = 1\n      ')
        f.write('ItemType = "{2}"\n      UnsafeDamage = 0\n      DisplayName = "&{0}下一页:{1}"\n    '.format(nextPageItemColor,nextPageItemName,nextPageItemType))
        f.write('}\n    PrimaryAction {Command = "vc o '+nextPageMenuName+'"}\n    KeepInventoryOpen = true\n  }\n')
    f.write('}')
