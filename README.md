# VirtualChestShop-editor
使用python,求大佬帮忙用java重置一个带gui的太感谢了...
我知道基本的菜单应该都会做，但超市做起来有点烦，就根据原来bossshop插件的编辑器改了一下做成了这个
代码仅供参考，请根据实际情况修改

输出实例：
Slot0 = [{
    Item {
      Count = 64
      ItemType = "minecraft:dirt"
      UnsafeDamage = 0
      DisplayName = "&a购买：一组泥土"
      ItemLore = ["&a价格：$30"]
    }
    PrimaryAction {
      Command = "cost: 30; console: give %player_name% minecraft:dirt 64"
      KeepInventoryOpen = true
    }
    Requirements = "%economy_balance% >= 30"
    }, {
    Item {
      Count = 64
      ItemType = "minecraft:dirt"
      UnsafeDamage = 0
      DisplayName = "&a购买：一组泥土"
      ItemLore = [
          "&a价格：$30"
          "&c你没有足够的金币！"
          ]
    }
  }]
  Slot27 = {
    Item {
      Count = 64
      ItemType = "minecraft:dirt"
      UnsafeDamage = 0
      DisplayName = "&c出售：一组泥土"
      ItemLore = ["&c价格：$30"]
    }
    PrimaryAction {
      Command = "cost-item: 64; cost: -30"
      HandheldItem {
        SearchInventory = true
        ItemType = "minecraft:dirt"
        UnsafeDamage = 0
                 Count = 64
      }
      KeepInventoryOpen = true
    }
  }


插件原帖：https://github.com/ustc-zzzz/VirtualChest/releases

mcbbs插件发布原帖：http://www.mcbbs.net/forum.php?mod=viewthread&tid=679260&extra=page%3D1%26filter%3Dsortid%26sortid%3D7%26searchoption%5B70%5D%5Bvalue%5D%5B4%5D%3D4%26searchoption%5B70%5D%5Btype%5D%3Dcheckbox
