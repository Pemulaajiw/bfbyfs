from abe import *

@bot.on(events.CallbackQuery(data=b'add_ssh'))
async def addserv(event):
  sender = await event.get_sender()
  db = get_db()
  val = valid(sender.id)
  admin_id = [v[0] for v in db.execute("SELECT * FROM admin").fetchall()]
  if sender.id not in admin_id:
    await event.edit("ANDA TIDAK MEMILIKI AKSES KE FITUR INI")
    return
  async with bot.conversation(event.chat_id) as nama:
    await event.edit("Silahkan masukan nama server")
    nama = nama.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
    nama = await nama
    nama = nama.message.message

  async with bot.conversation(event.chat_id) as domain:
    await event.respond("Silahkan masukan domain server")
    domain = domain.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
    domain = await domain
    domain = domain.message.message

  async with bot.conversation(event.chat_id) as limitip:
    await event.respond("Silahkan masukan limit ip")
    limitip = limitip.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
    limitip = await limitip
    limitip = limitip.message.message

  async with bot.conversation(event.chat_id) as harga:
    await event.respond("Silahkan masukan harga/day server")
    harga = harga.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
    harga = await harga
    harga = harga.message.message
    
  db.execute("INSERT INTO ssh (buttonname, domain, limitip, harga) VALUES (?,?,?,?)",(nama, domain, limitip, harga,))
  db.commit()
  
  msg = f"""
ADD SERVER ssh 
---------------------
Nama : {nama}
Domain : {domain}
Limit IP : {limitip}
Harga/day : {harga}
---------------------
"""
  await event.respond(msg,buttons=[[Button.inline(" MENU ","menu")]])

@bot.on(events.CallbackQuery(data=b'add_vmess'))
async def addserv(event):
  sender = await event.get_sender()
  db = get_db()
  val = valid(sender.id)
  admin_id = [v[0] for v in db.execute("SELECT * FROM admin").fetchall()]
  if sender.id not in admin_id:
    await event.edit("ANDA TIDAK MEMILIKI AKSES KE FITUR INI")
    return
  async with bot.conversation(event.chat_id) as nama:
    await event.edit("Silahkan masukan nama server")
    nama = nama.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
    nama = await nama
    nama = nama.message.message

  async with bot.conversation(event.chat_id) as domain:
    await event.respond("Silahkan masukan domain server")
    domain = domain.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
    domain = await domain
    domain = domain.message.message

  async with bot.conversation(event.chat_id) as limitip:
    await event.respond("Silahkan masukan limit ip")
    limitip = limitip.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
    limitip = await limitip
    limitip = limitip.message.message

  async with bot.conversation(event.chat_id) as quota:
    await event.respond("Silahkan masukan limit quota")
    quota = quota.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
    quota = await quota
    quota = quota.message.message

  async with bot.conversation(event.chat_id) as harga:
    await event.respond("Silahkan masukan harga/day server")
    harga = harga.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
    harga = await harga
    harga = harga.message.message
    
  db.execute("INSERT INTO vmess (buttonname, domain, limitip, quota, harga) VALUES (?,?,?,?,?)",(nama, domain, limitip, quota, harga,))
  db.commit()
  
  msg = f"""
ADD SERVER VMESS 
---------------------
Nama : {nama}
Domain : {domain}
Limit IP : {limitip}
Quota : {quota}
Harga/day : {harga}
---------------------
"""
  await event.respond(msg,buttons=[[Button.inline(" MENU ","menu")]])
 
@bot.on(events.CallbackQuery(data=b'add_vless'))
async def addserv(event):
  sender = await event.get_sender()
  db = get_db()
  val = valid(sender.id)
  admin_id = [v[0] for v in db.execute("SELECT * FROM admin").fetchall()]
  if sender.id not in admin_id:
    await event.edit("ANDA TIDAK MEMILIKI AKSES KE FITUR INI")
    return
  async with bot.conversation(event.chat_id) as nama:
    await event.edit("Silahkan masukan nama server")
    nama = nama.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
    nama = await nama
    nama = nama.message.message

  async with bot.conversation(event.chat_id) as domain:
    await event.respond("Silahkan masukan domain server")
    domain = domain.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
    domain = await domain
    domain = domain.message.message

  async with bot.conversation(event.chat_id) as limitip:
    await event.respond("Silahkan masukan limit ip")
    limitip = limitip.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
    limitip = await limitip
    limitip = limitip.message.message

  async with bot.conversation(event.chat_id) as quota:
    await event.respond("Silahkan masukan limit quota")
    quota = quota.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
    quota = await quota
    quota = quota.message.message

  async with bot.conversation(event.chat_id) as harga:
    await event.respond("Silahkan masukan harga/day server")
    harga = harga.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
    harga = await harga
    harga = harga.message.message
    
  db.execute("INSERT INTO vless (buttonname, domain, limitip, quota, harga) VALUES (?,?,?,?,?)",(nama, domain, limitip, quota, harga,))
  db.commit()
  
  msg = f"""
ADD SERVER vless 
---------------------
Nama : {nama}
Domain : {domain}
Limit IP : {limitip}
Quota : {quota}
Harga/day : {harga}
---------------------
"""
  await event.respond(msg,buttons=[[Button.inline(" MENU ","menu")]])

@bot.on(events.CallbackQuery(data=b'add_trojan'))
async def addserv(event):
  sender = await event.get_sender()
  db = get_db()
  val = valid(sender.id)
  admin_id = [v[0] for v in db.execute("SELECT * FROM admin").fetchall()]
  if sender.id not in admin_id:
    await event.edit("ANDA TIDAK MEMILIKI AKSES KE FITUR INI")
    return
  async with bot.conversation(event.chat_id) as nama:
    await event.edit("Silahkan masukan nama server")
    nama = nama.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
    nama = await nama
    nama = nama.message.message

  async with bot.conversation(event.chat_id) as domain:
    await event.respond("Silahkan masukan domain server")
    domain = domain.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
    domain = await domain
    domain = domain.message.message

  async with bot.conversation(event.chat_id) as limitip:
    await event.respond("Silahkan masukan limit ip")
    limitip = limitip.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
    limitip = await limitip
    limitip = limitip.message.message

  async with bot.conversation(event.chat_id) as quota:
    await event.respond("Silahkan masukan limit quota")
    quota = quota.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
    quota = await quota
    quota = quota.message.message

  async with bot.conversation(event.chat_id) as harga:
    await event.respond("Silahkan masukan harga/day server")
    harga = harga.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
    harga = await harga
    harga = harga.message.message
    
  db.execute("INSERT INTO trojan (buttonname, domain, limitip, quota, harga) VALUES (?,?,?,?,?)",(nama, domain, limitip, quota, harga,))
  db.commit()
  
  msg = f"""
ADD SERVER trojan 
---------------------
Nama : {nama}
Domain : {domain}
Limit IP : {limitip}
Quota : {quota}
Harga/day : {harga}
---------------------
"""
  await event.respond(msg,buttons=[[Button.inline(" MENU ","menu")]])

@bot.on(events.CallbackQuery(data=b'add_server'))
async def sub_menu(event):
  db = get_db()
  sender = await event.get_sender()
  x = db.execute("SELECT * FROM admin").fetchall()
  admin_id = [v[0] for v in x]
  if sender.id not in admin_id:
    await event.edit("ACCESS DENIED", alert=True)
    return
  tombol = [
    [Button.inline("ADD SSH","add_ssh"),
    Button.inline("ADD VMESS","add_vmess")],
    [Button.inline("ADD VLESS","add_vless"),
    Button.inline("ADD TROJAN","add_trojan")],
    [Button.inline("MENU SERVER","menu_server"),
    Button.inline("MENU UTAMA","menu")]]
  await event.edit(buttons=tombol)