while True:
  position_input = input("请输入物品在菜单位置:")
  if position_input == "" or position_input == " ": #如果未输入或者空格时，视为上一个输入数字+1
    position_input = last_position_input + 1
  last_position_input = int(position_input)
  position_input = int(position_input)
  position_input_sell = str(position_input + 27)
  position_input = str(position_input)
  item_ask = input("请输入你所要出售物品的中文名字:") #例子：一组火药；一块金锭 （务必带量词）
  amount_64 = "一组"
  amount_12 = "一打"
  amount_1 = ["一个","一颗","一棵","一打","一块"]  #敏感词辨识
  if amount_64 in item_ask:
    amount_ask = "64"
  elif amount_12 in item_ask:
    amount_ask = "12"
  elif amount_1[0] in item_ask or amount_1[1] in item_ask or amount_1[2] in  item_ask or amount_1[3] in item_ask or amount_1[4] in item_ask:
    amount_ask = "1"
  else:
    amount_ask = str(input('物品的数量:'))
  price_ask = input('物品的价格:')
  mc_item = input("请问是原版物品吗(y/n):")
  if mc_item == "y":
    id_ask = input('物品的英文id--minecraft:')
    id_ask = "minecraft:" + id_ask
  if mc_item == "n":
    id_ask = input('请输入物品的完整英文id:')
    id_ask = id_ask.replace("：",":")
  unsafe_num = input("请输入物品的UnsafeDamage特殊值:")  
  print("Slot"+position_input+" = [{") #购买
  print("    Item {")
  print("      Count = "+amount_ask)
  print('      ItemType = "'+id_ask+'"')
  print("      UnsafeDamage = "+unsafe_num)
  print('      DisplayName = "&a购买：'+item_ask+'"')
  print('      ItemLore = ["&a价格：$'+price_ask+'"]')
  print("    }")
  print("    PrimaryAction {")
  print('      Command = "cost: '+price_ask+'; console: give %player_name% '+id_ask+' '+amount_ask+'"')
  print("      KeepInventoryOpen = true")
  print("    }")
  print('    Requirements = "%economy_balance% >= '+price_ask+'"')
  print("    }, {")
  print("    Item {")
  print("      Count = "+amount_ask)
  print('      ItemType = "'+id_ask+'"')
  print("      UnsafeDamage = "+unsafe_num)
  print('      DisplayName = "&a购买：'+item_ask+'"')
  print("      ItemLore = [")
  print('	  "&a价格：$'+price_ask+'"')
  print('	  "&c你没有足够的金币！"')
  print("	  ]")
  print("    }")
  print("  }]")
  print("  Slot"+position_input_sell+" = {") #出售：默认为购买格+27
  print("    Item {")
  print("      Count = "+amount_ask)
  print('      ItemType = "'+id_ask+'"')
  print("      UnsafeDamage = "+unsafe_num)
  print('      DisplayName = "&c出售：'+item_ask+'"')
  print('      ItemLore = ["&c价格：$'+price_ask+'"]')
  print("    }")
  print("    PrimaryAction {")
  print('      Command = "cost-item: '+amount_ask+'; cost: -'+price_ask+'"')
  print("      HandheldItem {")
  print("        SearchInventory = true")
  print('        ItemType = "'+id_ask+'"')
  print("        UnsafeDamage = "+unsafe_num)
  print("        Count = "+amount_ask)
  print("      }")
  print("        KeepInventoryOpen = true")
  print("    }")
  print("  }")