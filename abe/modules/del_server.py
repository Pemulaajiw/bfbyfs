from abe import *

@bot.on(events.CallbackQuery(data=b'del_ssh'))
async def delvm(event):
    async def delvm_(event):
        s = db.execute("SELECT buttonname, harga FROM ssh").fetchall()
        if not s:
            await event.answer("TIDAK ADA SERVER DI PROTOCOL ssh", alert=True)
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
            conv_event = await conv.wait_event(events.CallbackQuery)
            # Decode menggunakan utf-8
            buttonname = conv_event.data.decode("utf-8")
        
        # Mendapatkan domain berdasarkan buttonname yang dipilih
        result = db.execute("SELECT domain FROM ssh WHERE buttonname = ?", (buttonname,)).fetchone()
        if result is None:
            await event.edit(
                f"**Server dengan buttonname `{buttonname}` tidak ditemukan.**",
                buttons=[[Button.inline("Back To Menu", "menu")]]
            )
            return
        
        domain = result[0]
        print(domain)
        print(buttonname)
        
        ip = db.execute("SELECT limitip FROM ssh WHERE buttonname = ?", (buttonname,)).fetchone()[0]
        quota = db.execute("SELECT quota FROM ssh WHERE buttonname = ?", (buttonname,)).fetchone()[0]
        harga = db.execute("SELECT harga FROM ssh WHERE buttonname = ?", (buttonname,)).fetchone()[0]
        
        msg = f"""
**----------------------------------**
** Detail Server ssh**
**----------------------------------**
** Server Name:** `{buttonname}`
** Domain:** `{domain}`
** Limit IP:** `{ip}` Device
** Harga:** `{harga}`
**----------------------------------**
** Klik Ya untuk menghapus server? **
**----------------------------------**
"""
        await event.edit(msg, buttons=[
            [Button.inline("Ya", "y"), Button.inline("Tidak", "n")],
            [Button.inline("«« Back To Menu ««", "menu")]
        ])
        
        async with bot.conversation(event.chat_id) as con:
            con_event = await con.wait_event(events.CallbackQuery)
            # Decode menggunakan utf-8
            confirmation = con_event.data.decode("utf-8")
        
        if confirmation == "y":
            db.execute("DELETE FROM ssh WHERE buttonname = ?", (buttonname,))
            db.commit()
            await event.edit("**Berhasil menghapus Server ssh**", buttons=[[Button.inline("Back To Menu", "menu")]])
        elif con.data.decode("ascii") != "y" and con.data.decode("ascii") != "menu":
            await event.edit("**Dibatalkan.**",buttons=[[Button.inline("Back To Menu","menu")]])

    # Verifikasi apakah user adalah admin
    db = get_db()
    x = db.execute("SELECT * FROM admin").fetchall()
    a = [v[0] for v in x]
    sender = await event.get_sender()
    if sender.id in a:
        await delvm_(event)
    else:
        await event.answer("Akses Ditolak!")

@bot.on(events.CallbackQuery(data=b'del_vmess'))
async def delvm(event):
    async def delvm_(event):
        s = db.execute("SELECT buttonname, harga FROM vmess").fetchall()
        if not s:
            await event.answer("TIDAK ADA SERVER DI PROTOCOL VMESS", alert=True)
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
            conv_event = await conv.wait_event(events.CallbackQuery)
            # Decode menggunakan utf-8
            buttonname = conv_event.data.decode("utf-8")
        
        # Mendapatkan domain berdasarkan buttonname yang dipilih
        result = db.execute("SELECT domain FROM vmess WHERE buttonname = ?", (buttonname,)).fetchone()
        if result is None:
            await event.edit(
                f"**Server dengan buttonname `{buttonname}` tidak ditemukan.**",
                buttons=[[Button.inline("Back To Menu", "menu")]]
            )
            return
        
        domain = result[0]
        print(domain)
        print(buttonname)
        
        ip = db.execute("SELECT limitip FROM vmess WHERE buttonname = ?", (buttonname,)).fetchone()[0]
        quota = db.execute("SELECT quota FROM vmess WHERE buttonname = ?", (buttonname,)).fetchone()[0]
        harga = db.execute("SELECT harga FROM vmess WHERE buttonname = ?", (buttonname,)).fetchone()[0]
        
        msg = f"""
**----------------------------------**
** Detail Server VMESS**
**----------------------------------**
** Server Name:** `{buttonname}`
** Domain:** `{domain}`
** Quota:** `{quota}` GB
** Limit IP:** `{ip}` Device
** Harga:** `{harga}`
**----------------------------------**
** Klik Ya untuk menghapus server? **
**----------------------------------**
"""
        await event.edit(msg, buttons=[
            [Button.inline("Ya", "y"), Button.inline("Tidak", "n")],
            [Button.inline("«« Back To Menu ««", "menu")]
        ])
        
        async with bot.conversation(event.chat_id) as con:
            con_event = await con.wait_event(events.CallbackQuery)
            # Decode menggunakan utf-8
            confirmation = con_event.data.decode("utf-8")
        
        if confirmation == "y":
            db.execute("DELETE FROM vmess WHERE buttonname = ?", (buttonname,))
            db.commit()
            await event.edit("**Berhasil menghapus Server VMESS**", buttons=[[Button.inline("Back To Menu", "menu")]])
        elif con.data.decode("ascii") != "y" and con.data.decode("ascii") != "menu":
            await event.edit("**Dibatalkan.**",buttons=[[Button.inline("Back To Menu","menu")]])

    # Verifikasi apakah user adalah admin
    db = get_db()
    x = db.execute("SELECT * FROM admin").fetchall()
    a = [v[0] for v in x]
    sender = await event.get_sender()
    if sender.id in a:
        await delvm_(event)
    else:
        await event.answer("Akses Ditolak!")
 
@bot.on(events.CallbackQuery(data=b'del_vless'))
async def delvm(event):
    async def delvm_(event):
        s = db.execute("SELECT buttonname, harga FROM vless").fetchall()
        if not s:
            await event.answer("TIDAK ADA SERVER DI PROTOCOL vless", alert=True)
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
            conv_event = await conv.wait_event(events.CallbackQuery)
            # Decode menggunakan utf-8
            buttonname = conv_event.data.decode("utf-8")
        
        # Mendapatkan domain berdasarkan buttonname yang dipilih
        result = db.execute("SELECT domain FROM vless WHERE buttonname = ?", (buttonname,)).fetchone()
        if result is None:
            await event.edit(
                f"**Server dengan buttonname `{buttonname}` tidak ditemukan.**",
                buttons=[[Button.inline("Back To Menu", "menu")]]
            )
            return
        
        domain = result[0]
        print(domain)
        print(buttonname)
        
        ip = db.execute("SELECT limitip FROM vless WHERE buttonname = ?", (buttonname,)).fetchone()[0]
        quota = db.execute("SELECT quota FROM vless WHERE buttonname = ?", (buttonname,)).fetchone()[0]
        harga = db.execute("SELECT harga FROM vless WHERE buttonname = ?", (buttonname,)).fetchone()[0]
        
        msg = f"""
**----------------------------------**
** Detail Server vless**
**----------------------------------**
** Server Name:** `{buttonname}`
** Domain:** `{domain}`
** Quota:** `{quota}` GB
** Limit IP:** `{ip}` Device
** Harga:** `{harga}`
**----------------------------------**
** Klik Ya untuk menghapus server? **
**----------------------------------**
"""
        await event.edit(msg, buttons=[
            [Button.inline("Ya", "y"), Button.inline("Tidak", "n")],
            [Button.inline("«« Back To Menu ««", "menu")]
        ])
        
        async with bot.conversation(event.chat_id) as con:
            con_event = await con.wait_event(events.CallbackQuery)
            # Decode menggunakan utf-8
            confirmation = con_event.data.decode("utf-8")
        
        if confirmation == "y":
            db.execute("DELETE FROM vless WHERE buttonname = ?", (buttonname,))
            db.commit()
            await event.edit("**Berhasil menghapus Server vless**", buttons=[[Button.inline("Back To Menu", "menu")]])
        elif con.data.decode("ascii") != "y" and con.data.decode("ascii") != "menu":
            await event.edit("**Dibatalkan.**",buttons=[[Button.inline("Back To Menu","menu")]])

    # Verifikasi apakah user adalah admin
    db = get_db()
    x = db.execute("SELECT * FROM admin").fetchall()
    a = [v[0] for v in x]
    sender = await event.get_sender()
    if sender.id in a:
        await delvm_(event)
    else:
        await event.answer("Akses Ditolak!")

@bot.on(events.CallbackQuery(data=b'del_trojan'))
async def delvm(event):
    async def delvm_(event):
        s = db.execute("SELECT buttonname, harga FROM trojan").fetchall()
        if not s:
            await event.answer("TIDAK ADA SERVER DI PROTOCOL trojan", alert=True)
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
            conv_event = await conv.wait_event(events.CallbackQuery)
            # Decode menggunakan utf-8
            buttonname = conv_event.data.decode("utf-8")
        
        # Mendapatkan domain berdasarkan buttonname yang dipilih
        result = db.execute("SELECT domain FROM trojan WHERE buttonname = ?", (buttonname,)).fetchone()
        if result is None:
            await event.edit(
                f"**Server dengan buttonname `{buttonname}` tidak ditemukan.**",
                buttons=[[Button.inline("Back To Menu", "menu")]]
            )
            return
        
        domain = result[0]
        print(domain)
        print(buttonname)
        
        ip = db.execute("SELECT limitip FROM trojan WHERE buttonname = ?", (buttonname,)).fetchone()[0]
        quota = db.execute("SELECT quota FROM trojan WHERE buttonname = ?", (buttonname,)).fetchone()[0]
        harga = db.execute("SELECT harga FROM trojan WHERE buttonname = ?", (buttonname,)).fetchone()[0]
        
        msg = f"""
**----------------------------------**
** Detail Server trojan**
**----------------------------------**
** Server Name:** `{buttonname}`
** Domain:** `{domain}`
** Quota:** `{quota}` GB
** Limit IP:** `{ip}` Device
** Harga:** `{harga}`
**----------------------------------**
** Klik Ya untuk menghapus server? **
**----------------------------------**
"""
        await event.edit(msg, buttons=[
            [Button.inline("Ya", "y"), Button.inline("Tidak", "n")],
            [Button.inline("«« Back To Menu ««", "menu")]
        ])
        
        async with bot.conversation(event.chat_id) as con:
            con_event = await con.wait_event(events.CallbackQuery)
            # Decode menggunakan utf-8
            confirmation = con_event.data.decode("utf-8")
        
        if confirmation == "y":
            db.execute("DELETE FROM trojan WHERE buttonname = ?", (buttonname,))
            db.commit()
            await event.edit("**Berhasil menghapus Server trojan**", buttons=[[Button.inline("Back To Menu", "menu")]])
        elif con.data.decode("ascii") != "y" and con.data.decode("ascii") != "menu":
            await event.edit("**Dibatalkan.**",buttons=[[Button.inline("Back To Menu","menu")]])

    # Verifikasi apakah user adalah admin
    db = get_db()
    x = db.execute("SELECT * FROM admin").fetchall()
    a = [v[0] for v in x]
    sender = await event.get_sender()
    if sender.id in a:
        await delvm_(event)
    else:
        await event.answer("Akses Ditolak!")
        
@bot.on(events.CallbackQuery(data=b'del_server'))
async def sub_menu(event):
  db = get_db()
  sender = await event.get_sender()
  x = db.execute("SELECT * FROM admin").fetchall()
  admin_id = [v[0] for v in x]
  if sender.id not in admin_id:
    await event.edit("ACCESS DENIED", alert=True)
    return
  tombol = [
    [Button.inline("DEL SSH","del_ssh"),
    Button.inline("DEL VMESS","del_vmess")],
    [Button.inline("DEL VLESS","del_vless"),
    Button.inline("DEL TROJAN","del_trojan")],
    [Button.inline("MENU SERVER","menu_server"),
    Button.inline("MENU UTAMA","menu")]]
  await event.edit(buttons=tombol)
