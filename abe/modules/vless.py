from abe import *

@bot.on(events.CallbackQuery(data=b'cvless'))
async def vless(event):
	async def vless_(event):
		s = db.execute("SELECT buttonname, harga FROM vless").fetchall()
		if not s:
		  await event.answer("TIDAK ADA SERVER DI PROTOCOL VLESS", alert=True)
		  return
        
		server_buttons = [
		  Button.inline(buttonname, buttonname.encode())
		  for buttonname, _ in s
		]
		  
		button_rows = [
		  server_buttons[i:i + 2]
		  for i in range(0, len(server_buttons), 2)
		]
		button_rows.append([Button.inline("MENU", b"menu")])
		await event.edit(buttons=button_rows)
		async with bot.conversation(event.chat_id) as conv:
			conv = conv.wait_event(events.CallbackQuery)
			buttonname = await conv
			buttonname = buttonname.data.decode("utf-8")
		harga = db.execute("SELECT harga FROM vless WHERE buttonname = (?)",(buttonname,)).fetchone()[0]
		domain = db.execute("SELECT domain FROM vless WHERE buttonname = (?)",(buttonname,)).fetchone()[0]
		quota = db.execute("SELECT quota FROM vless WHERE buttonname = (?)",(buttonname,)).fetchone()[0]
		limitip = db.execute("SELECT limitip FROM vless WHERE buttonname = (?)",(buttonname,)).fetchone()[0]
		z = requests.get(f"http://ip-api.com/json/{domain}?fields=country,region,city,timezone,isp").json()
		print(domain); print(harga); print(limitip)
		msg = f"""
**-----------------------------------------------**
**  DETAIL SERVER VLESS  **
**-----------------------------------------------**
** Server Name:** `{buttonname}`
** ISP:** `{z["isp"]}`
** Country:** `{z["country"]}`
** Domain:** `{domain}`
** Limit Quota:** `{quota}` GB
** Max IP:** {limitip}
** Harga/Day:** `{harga:,}`
**-----------------------------------------------**
** Klik Ya jika ingin membuat akun**
"""
		await event.edit(msg,buttons=[
[Button.inline(" Ya ","y"),Button.inline(" Tidak ","n")],
[Button.inline(" 🔙 Back To Menu ","menu")]])
		async with bot.conversation(event.chat_id) as con:
			con = con.wait_event(events.CallbackQuery)
			con = await con
		if con.data.decode("ascii") != "y" and con.data.decode("ascii") != "menu":
			await event.edit("**Dibatalkan.**",buttons=[[Button.inline("Back To Menu","menu")]])
		elif con.data.decode("ascii") == "y":
			async with bot.conversation(event.chat_id) as user:
					await event.edit(f"""
**Vless Account**
**Server :** `{buttonname}`
**Country :** `{z["country"]}`
**Region :** `{z["region"]}`
**Host :** `{domain}`

**Masukan Username**

Kombinasi
- Huruf Besar [A-Z]
- Huruf Kecil [a-z]
- Angka [0-9]

gunakan /cancel untuk membatalkan

""")
					user = user.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
					user = await user
					user = user.message.message
					
					if user == "/cancel":
					    await event.respond("Proses Dibatalkan",buttons=[[Button.inline("Back To Menu","menu")]])
					    return
					    
			async with bot.conversation(event.chat_id) as exp:
				msg = await event.respond(f"""
**Vless Account**
**Server :** `{buttonname}`
**Country :** `{z["country"]}`
**Region :** `{z["region"]}`
**Host :** `{domain}`
**Username :** `{user}`

**Enter Expiry**

""")
				exp = exp.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
				exp = await exp
				exp = exp.message.message
				
				if exp == "cancel":
				   await msg.edit("Proses Dibatalkan",buttons=[[Button.inline("Back To Menu","menu")]])
				   return

				harga_total = (harga * int(exp))

			async with bot.conversation(event.chat_id) as confirm:
				konfirmasi = await event.respond(f"""
**Konfirmasi Pesanan VLess**

**Server :** `{buttonname}`
**Country :** `{z["country"]}`
**Region :** `{z["region"]}`
**Host :** `{domain}`
**Username :** `{user}`
**Expired :** `{exp}` day
**Total Harga :** `Rp. {harga_total:,}`

Lanjutkan? Pilih Ya untuk melanjutkan atau Tidak untuk membatalkan.
			""", buttons=[
				[Button.inline("Ya", "confirm"), Button.inline("Tidak", b"cancel")]
			])
				confirm_event = confirm.wait_event(events.CallbackQuery)
				confirmation = await confirm_event
				confirmation_data = confirmation.data.decode("ascii")

				if confirmation_data == "cancel":
				   await konfirmasi.edit("**Proses dibatalkan.**", buttons=[[Button.inline("Back To Menu", "menu")]])
				   return

			if int(val["saldo"]) < harga_total:
				await konfirmasi.edit(f"""
**Saldo Anda tidak cukup.**
Total biaya: Rp.{harga_total:,}
Saldo Anda: Rp.{val["saldo"]}
""")
			else:
				min = harga_total
				param = f":1000/create-vless?user={user}&limitip={limitip}&quota={quota}&exp={exp}"
				r = requests.get("http://"+domain+param)
				if r.text != "error":
					today = datetime.date.today()
					later = today + datetime.timedelta(days=int(exp))
					try:
						db.execute("UPDATE user SET saldo = ? WHERE member = ?",(int(val["saldo"])-int(min),sender.id,))
						db.commit()
						val["saldo"] = int(val["saldo"]) - int(min)
					except:
						pass
					x = r.text.replace('[','').replace(']','').replace('"',
'').split(',')
					print(x)
					if len(list(x)) == 2:
						remarks = re.search("#(.*)",x[0]).group(1)
						domain = re.search("@(.*?):",x[0]).group(1)
						uuid = re.search("vless://(.*?)@",x[0]).group(1)
						path = re.search("path=(.*?)&",x[0]).group(1)
						msg = f"""
**◇━━━━━━━━━━━━━◇**
**⟨ Xray/Vless Account ⟩**
**◇━━━━━━━━━━━━━◇**
**» Remarks   :** `{remarks}`
**» Domain    :** `{domain}`
**» Jumlah IP :** `{limitip}`
**» Port DNS  :** `443, 53`
**» port TLS  :** `443`
**» Port NTLS :** `80, 8080, 8081-9999`
**» NetWork   :** `(WS) or (gRPC)`
**» User ID   :** `{uuid}`
**» Path      :** `{path}`
**» Path Support :** `http://bug.com/vless`
**» Path :** `Multipath`
**◇━━━━━━━━━━━━━◇**
**» Link TLS   : **
```{x[0]}```
**◇━━━━━━━━━━━━━◇**
**» Link NTLS  :**
```{x[1].replace(" ","")}```
**◇━━━━━━━━━━━━━◇**
**» Link GRPC  :**
```{x[2].replace(" ","")}```**◇━━━━━━━━━━━━━◇**
**» Format OpenClash :** `https://{domain}:89/vless-{remarks}.txt`
**◇━━━━━━━━━━━━━◇**
**🗓️ Expired Until:** `{later}`

"""

					elif len(list(x)) == 3:
						remarks = re.search("#(.*)",x[0]).group(1)
						domain = re.search("@(.*?):",x[0]).group(1)
						uuid = re.search("vless://(.*?)@",x[0]).group(1)
						path = re.search("path=(.*?)&",x[0]).group(1)
						msg = f"""
**◇━━━━━━━━━━━━━◇**
**⟨ Xray/Vless Account ⟩**
**◇━━━━━━━━━━━━━◇**
**» Remarks   :** `{remarks}`
**» Domain    :** `{domain}`
**» Jumlah IP :** `{limitip}`
**» Port DNS  :** `443, 53`
**» port TLS  :** `443`
**» Port NTLS :** `80, 8080, 8081-9999`
**» NetWork   :** `(WS) or (gRPC)`
**» User ID   :** `{uuid}`
**» Path      :** `{path}`
**» Path Support :** `http://bug.com/vless`
**» Path :** `Multipath`
**◇━━━━━━━━━━━━━◇**
**» Link TLS   : **
```{x[0]}```
**◇━━━━━━━━━━━━━◇**
**» Link NTLS  :**
```{x[1].replace(" ","")}```
**◇━━━━━━━━━━━━━◇**
**» Link GRPC  :**
```{x[2].replace(" ","")}```**◇━━━━━━━━━━━━━◇**
**» Format OpenClash :** `https://{domain}:89/vless-{remarks}.txt`
**◇━━━━━━━━━━━━━◇**
**🗓️ Expired Until:** `{later}`


"""
					message = await konfirmasi.edit(msg,buttons=None)
					await bot.pin_message(event.chat_id, message, notify=True)
					await event.respond(f"""
Pembelian Akun Vless Sukses
Total Pembelian : Rp. `{harga_total:,}`
Sisa Saldo Anda : `{val["saldo"]:,}`
""",buttons=[[Button.inline("Back To Menu","menu")]])
				else:
					await event.respond("""
**__ERROR__**

**Penyebab :** `Username Sudah Digunakan Atau Server Error!`

""")

	sender = await event.get_sender()
	sender_id = sender.id
	val = valid(sender.id)
	db = get_db()
	x = db.execute("SELECT * FROM admin").fetchall()
	a = [v[0] for v in x]
	data = event.data.decode("ascii").split("-")[0]
	if val == "false":
		if sender.id not in a:
			await event.answer("Akses Ditolak")
		else:
			val = {"saldo":"100000000"}
			await vless_(event)
	else:
		await vless_(event)
		
@bot.on(events.CallbackQuery(data=b'vless'))
async def vmess(event):
    sender = await event.get_sender()
    db = get_db()
    x = db.execute("SELECT * FROM admin").fetchall()
    admin_id = [v[0] for v in x]
    val = valid(sender.id)

    s = db.execute("SELECT buttonname, harga FROM vless").fetchall()
    if not s:
        await event.answer("TIDAK ADA SERVER DI PROTOCOL VLESS", alert=True)
        return

    # Buat tombol server dari DB
    server_buttons = []
    for buttonname in s:
        server_buttons.append([Button.inline(buttonname, f"{buttonname}")])

    if sender.id in admin_id:
        serv = "\n".join([f"• {buttonname} - Rp. {harga}" for buttonname, harga in s])
        msg_admin = f"""
SERVER VLESS :
{serv}
"""
        a = await event.edit(msg_admin, buttons=[
            [Button.inline("CREATE VLESS", b"cvless"),
             Button.inline("TRIAL VLESS", b"tvless")],
            [Button.inline("RENEW VLESS", b"rvless")],
            [Button.inline("MENU", b"menu")]
        ])
        if not a:
            await event.respond(msg_admin, buttons=[
                [Button.inline("CREATE VLESS", b"cvmess"),
                 Button.inline("TRIAL VLESS", b"tvmess")],
                [Button.inline("RENEW VLESS", b"rvmess")],
                [Button.inline("MENU", b"menu")]
            ])
    else:
        if val == "false":
            try:
                await event.answer("ACCESS DENIED", alert=True)
            except:
                await event.answer("ACCESS DENIED", alert=True)
        else:
            serv = "\n".join([f"• {buttonname} - Rp. {harga}" for buttonname, harga in s])
            msg_user = f"""
SERVER VLESS :
{serv}
"""
            u = await event.edit(msg_user, buttons=[
                [Button.inline("CREATE VLESS", b"cvless")],
                [Button.inline("MENU", b"menu")]
            ])
            if not u:
                await event.respond(msg_user, buttons=[
                    [Button.inline("CREATE VLESS", b"cvless")]
                    [Button.inline("MENU", b"menu")]
                ])