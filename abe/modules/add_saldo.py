from abe import *

@bot.on(events.CallbackQuery(data=b'add_saldo'))
async def addsaldo(event):
    db = get_db()
    x = db.execute("SELECT * FROM admin").fetchall()
    a = [v[0] for v in x]
    sender = await event.get_sender()
    
    if sender.id in a:
        # Hapus tombol email dan tampilkan pesan untuk memasukkan User ID
        await event.edit("**Silahkan Masukkan User ID yang Ingin Ditambah Saldo Nya:**")
        
        async with bot.conversation(event.chat_id) as conv:
            # Tunggu pesan baru dari pengguna yang berisi User ID
            user_id_msg = await conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            user_id = user_id_msg.message.message
            
            try:
                user_id = int(user_id)
            except ValueError:
                await event.respond("**User ID tidak valid. Harap masukkan angka yang benar.**",buttons=[[Button.inline("Back To Menu","menu")]])
                return

        # Validasi apakah user_id ada di database
        email = db.execute("SELECT email FROM user WHERE member = ?", (user_id,)).fetchone()
        if email is None:
            await event.respond("**User ID tidak ditemukan.**",buttons=[[Button.inline("Back To Menu","menu")]])
            return
        
        email = email[0]
        saldo = db.execute("SELECT saldo FROM user WHERE member = ?", (user_id,)).fetchone()[0]
        member = db.execute("SELECT member FROM user WHERE email = ?", (email,)).fetchone()[0]
        
        xs = await bot.get_entity(user_id)
        msg = f"""
**━━━━━━━━━━━━━━━━**
**⟨ Informasi Member ⟩**
**━━━━━━━━━━━━━━━━**
**» Nama:** `{xs.first_name}`
**» Username:** `{xs.username}`
**» Member ID:** `{user_id}`
**» Saldo Tersisa:** `RP.{saldo:,}`
**» Email:** `{email}`
**━━━━━━━━━━━━━━━━**
**Lanjutkan Mengisi Saldo?**
**━━━━━━━━━━━━━━━━**
"""
        hahaa = await event.respond(msg, buttons=[
            [Button.inline("Ya", "y"), Button.inline("Tidak", "n")],
            [Button.inline("«🔙 Back To Menu «", "menu")]
        ])
        
        async with bot.conversation(event.chat_id) as con:
            con = await con.wait_event(events.CallbackQuery)
        
        if con.data.decode("ascii") == "y":
            await hahaa.edit("**Masukkan Saldo Yang Akan Ditambahkan:**",buttons=None)
            
            async with bot.conversation(event.chat_id) as sal:
                sal_msg = await sal.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
                sal_amount = sal_msg.message.message
                
                try:
                    sal_amount = int(sal_amount)
                except ValueError:
                    await event.respond("**Jumlah saldo tidak valid. Harap masukkan angka yang benar.**",buttons=[[Button.inline("Back To Menu","menu")]])
                    return
            
            db.execute("UPDATE user SET saldo = ? WHERE member = ?", (int(saldo) + sal_amount, user_id))
            db.commit()
            
            saldo_akhir = db.execute("SELECT saldo FROM user WHERE member = ?", (user_id,)).fetchone()[0]
            msg = f"""
**━━━━━━━━━━━━━━━━**
**⟨ Sukses Menambahkan Saldo ⟩**
**━━━━━━━━━━━━━━━━**
**» Nama:** `{xs.first_name}`
**» Username:** `{xs.username}`
**» Member ID:** `{user_id}`
**» Total Saldo:** RP.`{int(saldo) + sal_amount}`
**» Email:** `{email}`
**━━━━━━━━━━━━━━━━**
"""
            await event.respond(msg, buttons=[[Button.inline("BACK TO MENU", "menu")]])
            
            await bot.send_message(user_id, f"""
**━━━━━━━━━━━━━━━━**
**⟨ Pembayaran berhasil ⟩**
**━━━━━━━━━━━━━━━━**
**» Penambahan Saldo:** RP.`{sal_amount}`
**» Saldo Awal:** RP.`{saldo2}`
**» Saldo Saat Ini:** RP.`{saldo_akhir}`
**━━━━━━━━━━━━━━━━**
""")
        else:
            await event.edit("**Dibatalkan.**", buttons=[[Button.inline("BACK TO MENU", "menu")]])
