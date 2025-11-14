from abe import *

@bot.on(events.CallbackQuery(data=b'min_saldo'))
async def minsaldo(event):
    db = get_db()
    is_active, message_or_duration = await check_bot_expiration()
    if not is_active:
        await event.respond(message_or_duration)
        return
    x = db.execute("SELECT * FROM admin").fetchall()
    a = [v[0] for v in x]
    sender = await event.get_sender()
    
    if sender.id in a:
        await event.edit("**Silahkan Masukkan User ID yang Ingin Dikurangi Saldo Nya:**")
        
        async with bot.conversation(event.chat_id) as conv:
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
        saldo2 = f"{saldo:,}"
        xs = await bot.get_entity(user_id)
        
        msg = f"""
**━━━━━━━━━━━━━━━━**
**⟨ Informasi Member ⟩**
**━━━━━━━━━━━━━━━━**
**» Nama:** `{xs.first_name}`
**» Username:** `{xs.username}`
**» Member ID:** `{user_id}`
**» Saldo Tersisa:** `RP.{saldo2}`
**» Email:** `{email}`
**━━━━━━━━━━━━━━━━**
**Lanjutkan Mengurangi Saldo?**
**━━━━━━━━━━━━━━━━**
"""
        hahaa = await event.respond(msg, buttons=[
            [Button.inline("Ya", "y"), Button.inline("Tidak", "n")],
            [Button.inline("«🔙 Back To Menu «", "menu")]
        ])
        
        async with bot.conversation(event.chat_id) as con:
            con = await con.wait_event(events.CallbackQuery)
        
        if con.data.decode("ascii") == "y":
            # Hapus tombol dan ubah pesan menjadi instruksi untuk memasukkan saldo
            await hahaa.edit("**Masukkan Saldo Yang Akan Dikurangi:**", buttons=None)
            
            async with bot.conversation(event.chat_id) as sal:
                sal_msg = await sal.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
                sal_amount = sal_msg.message.message
                
                try:
                    sal_amount = int(sal_amount)
                except ValueError:
                    await event.respond("**Jumlah saldo tidak valid. Harap masukkan angka yang benar.**",buttons=[[Button.inline("Back To Menu","menu")]])
                    return
                
                if sal_amount > saldo:
                    await event.respond("**Saldo tidak cukup untuk dikurangi.**",buttons=[[Button.inline("Back To Menu","menu")]])
                    return

            db.execute("UPDATE user SET saldo = ? WHERE member = ?", (saldo - sal_amount, user_id))
            db.commit()
            
            saldo_akhir = db.execute("SELECT saldo FROM user WHERE member = ?", (user_id,)).fetchone()[0]
            msg = f"""
**━━━━━━━━━━━━━━━━**
**⟨ Sukses Mengurangi Saldo ⟩**
**━━━━━━━━━━━━━━━━**
**» Nama:** `{xs.first_name}`
**» Username:** `{xs.username}`
**» Member ID:** `{user_id}`
**» Total Saldo:** RP.`{saldo_akhir}`
**» Email:** `{email}`
**━━━━━━━━━━━━━━━━**
"""
            await event.respond(msg, buttons=[[Button.inline("BACK TO MENU", "menu")]])
        else:
            await hahaa.edit("**Dibatalkan.**", buttons=[[Button.inline("Back To Menu","menu")]])
