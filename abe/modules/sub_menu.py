from abe import *

@bot.on(events.CallbackQuery(data=b'sub_menu'))
async def sub_menu(event):
  db = get_db()
  sender = await event.get_sender()
  x = db.execute("SELECT * FROM admin").fetchall()
  admin_id = [v[0] for v in x]
  if sender.id not in admin_id:
    await event.edit("ACCESS DENIED", alert=True)
    return
  tombol = [
    [Button.inline("MENU SSH","ssh"),
    Button.inline("MENU VMESS","vmess")],
    [Button.inline("MENU VLESS","vless"),
    Button.inline("MENU TROJAN","trojan")],
    [Button.inline("MENU","menu")]]
  await event.edit(buttons=tombol)