from abe import *

@bot.on(events.CallbackQuery(data=b'menu_saldo'))
async def sub_menu(event):
  db = get_db()
  sender = await event.get_sender()
  x = db.execute("SELECT * FROM admin").fetchall()
  admin_id = [v[0] for v in x]
  if sender.id not in admin_id:
    await event.edit("ACCESS DENIED", alert=True)
    return
  tombol = [
    [Button.inline("ADD SALDO","add_saldo"),
    Button.inline("MIN SALDO","min_saldo")],
    [Button.inline("MENU","menu")]]
  await event.edit(buttons=tombol)