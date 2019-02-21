list = ["night_vision","long_night_vision","invisibility","long_invisibility","leaping","strong_leaping","long_leaping","fire_resistance","long_fire_resistance","swiftness","strong_swiftness","long_swiftness","water_breathing","healing","strong_healing","regeneration","strong_regeneration","long_regeneration","strength","strong_strength","long_strength","luck"]
list2 = ["night_vision","long_night_vision","invisibility","long_invisibility","leaping","strong_leaping","long_leaping","fire_resistance","long_fire_resistance","swiftness","strong_swiftness","long_swiftness","slowness","long_slowness","water_breathing","healing","strong_healing","harming","strong_harming","poison","strong_poison","long_poison","regeneration","strong_regeneration","long_regeneration","strength","strong_strength","long_strength","weakness","long_weakness","luck"]
position = 0
for i in range(0,len(list)):
  position_input = str(position)
  item_ask = "药水"
  amount_ask = "1"
  price_ask = "5000"
  id_ask = "minecraft:potion" 
  print("  Slot"+position_input+" = [{") #购买
  print("    Item {")
  print("      Count = 1")
  print('      ItemType = "minecraft:potion"')
  print("      UnsafeDamage = 0")
  print('      UnsafeData = {Potion = "'+list[i]+'"}')
  print('      DisplayName = "&e该药水具有以下效果:"')
  print('      ItemLore = ["&a价格：$'+price_ask+'"]')
  print("    }")
  print("    PrimaryAction {")
  print('      Command = "cost: '+price_ask+'; console: give %player_name% '+id_ask+' '+amount_ask+' 0 {Potion:"'+list[i]+'"}"')
  print("      KeepInventoryOpen = true")
  print("    }")
  print('    Requirements = "%economy_balance% >= '+price_ask+'"')
  print("    }, {")
  print("    Item {")
  print("      Count = 1")
  print('      ItemType = "minecraft:potion"')
  print("      UnsafeDamage = 0")
  print('      UnsafeData = {Potion = "'+list[i]+'"}')
  print('      DisplayName = "&e该药水具有以下效果:"')
  print("      ItemLore = [")
  print('	  "&a价格：$'+price_ask+'"')
  print('	  "&c你没有足够的金币！"')
  print("	  ]")
  print("    }")
  print("  }]")
  position += 1
for i in range(0,len(list2)):
  position_input = str(position)
  item_ask = "药水"
  amount_ask = "1"
  price_ask = "10000"
  id_ask = "minecraft:splash_potion" 
  print("  Slot"+position_input+" = [{") #购买
  print("    Item {")
  print("      Count = 1")
  print('      ItemType = "minecraft:splash_potion"')
  print("      UnsafeDamage = 0")
  print('      UnsafeData = {Potion = "'+list2[i]+'"}')
  print('      DisplayName = "&c该喷溅型药水具有以下效果:"')
  print('      ItemLore = ["&a价格：$'+price_ask+'"]')
  print("    }")
  print("    PrimaryAction {")
  print('      Command = "cost: '+price_ask+'; console: give %player_name% '+id_ask+' '+amount_ask+' 0 {Potion:"'+list2[i]+'"}"')
  print("      KeepInventoryOpen = true")
  print("    }")
  print('    Requirements = "%economy_balance% >= '+price_ask+'"')
  print("    }, {")
  print("    Item {")
  print("      Count = 1")
  print('      ItemType = "minecraft:splash_potion"')
  print("      UnsafeDamage = 0")
  print('      UnsafeData = {Potion = "'+list2[i]+'"}')
  print('      DisplayName = "&c该喷溅型药水具有以下效果:"')
  print("      ItemLore = [")
  print('	  "&a价格：$'+price_ask+'"')
  print('	  "&c你没有足够的金币！"')
  print("	  ]")
  print("    }")
  print("  }]")
  position += 1