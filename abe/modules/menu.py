from abe import *

@bot.on(events.NewMessage(pattern=r"(?:.menu|/menu)$"))
@bot.on(events.CallbackQuery(data=b'menu'))
async def menu(event):
  sender = await event.get_sender()
  db = get_db()
  x = db.execute("SELECT user_id FROM admin").fetchall()
  admin_id = [v[0] for v in x]
  val = valid(sender.id)
  if sender.id in admin_id:
    msg_admin = f"""
**Selamat Datang Admin @{sender.username}!!**
**-----------------------**
**ID :** `{sender.id}`
**Username :** @{sender.username}
**Saldo :** Rp. `Infinity`
**-----------------------**
"""
    a = await event.edit(msg_admin,buttons=[
  [Button.inline("MENU CREATE","sub_menu")],
  [Button.inline("MENU SERVER","menu_server"),
  Button.inline("MENU SALDO","menu_saldo")],
  [Button.inline("MENU ORKUT","menu_orkut"),
  Button.inline("LIST USER","list_user")]])
    if not a:
      await event.edit(msg_admin,buttons=[
          [Button.inline("MENU CREATE","sub_menu")],
          [Button.inline("MENU SERVER","menu_server"),
          Button.inline("MENU SALDO","menu_saldo")],
          [Button.inline("MENU ORKUT","menu_orkut")],
          [Button.inline("LIST USER ","list_user")]])
  else:
    if val == "false":
      try:
        await event.answer("ACCESS DENIED",alert=True)
      except:
        await event.answer("ACCESS DENIED",alert=True)
    else:
      msg_user = f"""
**Selamat Datang @{sender.username}!!**
**-----------------------**
**ID :** `{sender.id}`
**Username :** @{sender.username}
**Saldo :** Rp. `{val["saldo"]}`
**-----------------------**
"""
      u = await event.edit(msg_user,buttons=[
          [Button.inline("MENU SSH","ssh"),
          Button.inline("MENU VMESS","vmess")],
          [Button.inline("MENU VLESS","vless"),
          Button.inline("MENU TROJAN","trojan")],
          [Button.inline("TOPUP BY ORKUT","orkut")]])
      if not u:
          await event.edit(msg_user,buttons=[
            [Button.inline("MENU SSH","ssh"),
            Button.inline("MENU VMESS","vmess")],
            [Button.inline("MENU VLESS","vless"),
            Button.inline("CREATE TROJAN","trojan")],
            [Button.inline("TOPUP BY ORKUT","orkut")]])
        