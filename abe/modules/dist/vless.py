from kyt import *

#delete
@bot.on(events.CallbackQuery(data=b'delete7-vless'))
async def delete_vless(event):
	async def delete_vless_(event):
		async with bot.conversation(chat) as user:
			cmd2 = f" cat /etc/xray/config.json | grep '^#vlg' |  cut -d ' ' -f 2-3 | nl -s ') '".strip()
			x = subprocess.check_output(cmd2, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
			print(x)
			z = subprocess.check_output(cmd2, shell=True).decode("ascii")
			await event.edit(f"""
**✨ LIST DELETE USER**
{z}
**👉 Input Your Number :**
/cancel Kembali KeMENU
""")
			user = user.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
			user = (await user).raw_text
		per = "/cancel"
		if user == per:
			await event.respond(f"""
**» CANCEL**
""",buttons=[[Button.inline("‹ Main Menu ›","menu")]])
		else:
			cmd = f'printf "%s\n" "4" "{user}" | m-vless | sleep 2 | exit'
			subprocess.check_output(cmd, shell=True)
			await event.respond(f"""
**» SUCCES**
""",buttons=[[Button.inline("‹ Main Menu ›","menu")]])
	chat = event.chat_id
	sender = await event.get_sender()
	a = valid(str(sender.id))
	if a == "true":
		await delete_vless_(event)
	else:
		await event.answer("Akses Ditolak",alert=True)

#renew
@bot.on(events.CallbackQuery(data=b'renew7-vless'))
async def renew_vless(event):
	async def renew_vless_(event):
		async with bot.conversation(chat) as user:
			cmd2 = f" cat /etc/xray/config.json | grep '^#vlg' |  cut -d ' ' -f 2-3 | nl -s ') '".strip()
			x = subprocess.check_output(cmd2, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
			print(x)
			z = subprocess.check_output(cmd2, shell=True).decode("ascii")
			await event.edit(f"""
**✨ LIST RENEW USER**
{z}
**👉 Input Your Number :**
/cancel Kembali KeMENU
""")
			user = user.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
			user = (await user).raw_text
		per = "/cancel"
		if user == per:
			await event.respond(f"""
**» CANCEL**
""",buttons=[[Button.inline("‹ Main Menu ›","menu")]])
		else:
			async with bot.conversation(chat) as exp:
				await event.respond(f"""
**👉 Input Your New Expired (day) :**
""")
				exp = exp.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
				exp = (await exp).raw_text
			cmd = f'printf "%s\n" "3" "{user}" "{exp}" | m-vless | sleep 2 | exit'
			subprocess.check_output(cmd, shell=True)
			await event.respond(f"""
**» SUCCES**
""",buttons=[[Button.inline("‹ Main Menu ›","menu")]])
	chat = event.chat_id
	sender = await event.get_sender()
	a = valid(str(sender.id))
	if a == "true":
		await renew_vless_(event)
	else:
		await event.answer("Akses Ditolak",alert=True)


#limit
@bot.on(events.CallbackQuery(data=b'limit7-vless'))
async def limit_vless(event):
	async def limit_vless_(event):
		async with bot.conversation(chat) as user:
			cmd2 = f" cat /etc/xray/config.json | grep '^#vlg' |  cut -d ' ' -f 2-3 | nl -s ') '".strip()
			x = subprocess.check_output(cmd2, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
			print(x)
			z = subprocess.check_output(cmd2, shell=True).decode("ascii")
			await event.edit(f"""
**✨ CHANGE LIMIT USER**
{z}
**👉 Input Your Number :**
/cancel Kembali KeMENU
""")
			user = user.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
			user = (await user).raw_text
		per = "/cancel"
		if user == per:
			await event.respond(f"""
**» CANCEL**
""",buttons=[[Button.inline("‹ Main Menu ›","menu")]])
		else:
			async with bot.conversation(chat) as exp:
				await event.respond(f"""
**👉 Input Your New Limit IP Login :**
0 For Unlimited
""")
				exp = exp.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
				exp = (await exp).raw_text
			async with bot.conversation(chat) as pw:
				await event.respond(f"""
**👉 Input Your New Quota User :**
0 For Unlimited
""")
				pw = pw.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
				pw = (await pw).raw_text
			cmd = f'printf "%s\n" "7" "{user}" "{exp}" "{pw}" | m-vless | sleep 2 | exit'
			subprocess.check_output(cmd, shell=True)
			await event.respond(f"""
**» SUCCES CHANGE**
""",buttons=[[Button.inline("‹ Main Menu ›","menu")]])
	chat = event.chat_id
	sender = await event.get_sender()
	a = valid(str(sender.id))
	if a == "true":
		await limit_vless_(event)
	else:
		await event.answer("Akses Ditolak",alert=True)

#CekConfig
@bot.on(events.CallbackQuery(data=b'akun7-vless'))
async def akun_vless(event):
	async def akun_vless_(event):
		async with bot.conversation(chat) as user:
			cmd2 = f" cat /etc/xray/config.json | grep '^#vlg' |  cut -d ' ' -f 2-3 | nl -s ') '".strip()
			x = subprocess.check_output(cmd2, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
			print(x)
			z = subprocess.check_output(cmd2, shell=True).decode("ascii")
			await event.edit(f"""
**✨ CEK CONFIG USER**
{z}
**👉 Input Your Number :**
/cancel Kembali KeMENU
""")
			user = user.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
			user = (await user).raw_text
		per = "/cancel"
		if user == per:
			await event.respond(f"""
**» CANCEL**
""",buttons=[[Button.inline("‹ Main Menu ›","menu")]])
		else:
			cmd = f'printf "%s\n" "6" "{user}" | m-vless | sleep 2 | exit'
			subprocess.check_output(cmd, shell=True)
			await event.respond(f"""
**» SUCCES CEK AKUN**
""",buttons=[[Button.inline("‹ Main Menu ›","menu")]])
	chat = event.chat_id
	sender = await event.get_sender()
	a = valid(str(sender.id))
	if a == "true":
		await akun_vless_(event)
	else:
		await event.answer("Akses Ditolak",alert=True)
		
		
#restore
@bot.on(events.CallbackQuery(data=b'restore7-vless'))
async def restore_vless(event):
	async def restore_vless_(event):
		async with bot.conversation(chat) as user:
			cmd2 = f" cat /etc/vless/akundelete | grep '^###' |  cut -d ' ' -f 2-3 | nl -s ') '".strip()
			x = subprocess.check_output(cmd2, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
			print(x)
			z = subprocess.check_output(cmd2, shell=True).decode("ascii")
			await event.edit(f"""
**✨ LIST AKUN RESTORE **
{z}
**👉 Input Your Number :**
/cancel Kembali KeMENU
""")
			user = user.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
			user = (await user).raw_text
		per = "/cancel"
		if user == per:
			await event.respond(f"""
**» CANCEL**
""",buttons=[[Button.inline("‹ Main Menu ›","menu")]])
		else:
			async with bot.conversation(chat) as exp:
				await event.respond(f"""
**👉 Input Your Expired (day) :**
""")
				exp = exp.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
				exp = (await exp).raw_text
			async with bot.conversation(chat) as pw:
				await event.respond(f"""
**👉 Input Your New Limit IP Login :**
0 For Unlimited
""")
				pw = pw.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
				pw = (await pw).raw_text
			async with bot.conversation(chat) as pw2:
				await event.respond(f"""
**👉 Input Your New Quota User:**
0 For Unlimited
""")
				pw2 = pw2.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
				pw2 = (await pw2).raw_text
			cmd = f'printf "%s\n" "11" "{user}" "{exp}" "{pw}" "{pw2}" | m-vless | sleep 2 | exit'
			subprocess.check_output(cmd, shell=True)
			await event.respond(f"""
**» SUCCES CHANGE**
""",buttons=[[Button.inline("‹ Main Menu ›","menu")]])
	chat = event.chat_id
	sender = await event.get_sender()
	a = valid(str(sender.id))
	if a == "true":
		await restore_vless_(event)
	else:
		await event.answer("Akses Ditolak",alert=True)


#MultiLogin Login
@bot.on(events.CallbackQuery(data=b'loginip7-vless'))
async def loginip_vless(event):
	async def loginip_vless_(event):
		async with bot.conversation(chat) as user:
			cmd2 = f" cat /etc/vless/listlock | grep '^###' |  cut -d ' ' -f 2-3 | nl -s ') '".strip()
			x = subprocess.check_output(cmd2, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
			print(x)
			z = subprocess.check_output(cmd2, shell=True).decode("ascii")
			await event.edit(f"""
**✨ LIST MULTI LOGIN IP USER**
{z}
**👉 Input Your Number :**
/cancel Kembali KeMENU
""")
			user = user.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
			user = (await user).raw_text
		per = "/cancel"
		if user == per:
			await event.respond(f"""
**» CANCEL**
""",buttons=[[Button.inline("‹ Main Menu ›","menu")]])
		else:
			cmd = f'printf "%s\n" "9" "{user}" | m-vless | sleep 2 | exit'
			subprocess.check_output(cmd, shell=True)
			await event.respond(f"""
**» SUCCES UNLOCK**
""",buttons=[[Button.inline("‹ Main Menu ›","menu")]])
	chat = event.chat_id
	sender = await event.get_sender()
	a = valid(str(sender.id))
	if a == "true":
		await loginip_vless_(event)
	else:
		await event.answer("Akses Ditolak",alert=True)
		
#MultiLogin Quota
@bot.on(events.CallbackQuery(data=b'logingb7-vless'))
async def logingb_vless(event):
	async def logingb_vless_(event):
		async with bot.conversation(chat) as user:
			cmd2 = f" cat /etc/vless/userQuota | grep '^###' |  cut -d ' ' -f 2-3 | nl -s ') '".strip()
			x = subprocess.check_output(cmd2, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
			print(x)
			z = subprocess.check_output(cmd2, shell=True).decode("ascii")
			await event.edit(f"""
**✨ LIST LOGIN QUOTA USER**
{z}
**👉 Input Your Number :**
/cancel Kembali KeMENU
""")
			user = user.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
			user = (await user).raw_text
		per = "/cancel"
		if user == per:
			await event.respond(f"""
**» CANCEL**
""",buttons=[[Button.inline("‹ Main Menu ›","menu")]])
		else:
			cmd = f'printf "%s\n" "10" "{user}" | m-vless | sleep 2 | exit'
			subprocess.check_output(cmd, shell=True)
			await event.respond(f"""
**» SUCCES UNLOCK**
""",buttons=[[Button.inline("‹ Main Menu ›","menu")]])
	chat = event.chat_id
	sender = await event.get_sender()
	a = valid(str(sender.id))
	if a == "true":
		await logingb_vless_(event)
	else:
		await event.answer("Akses Ditolak",alert=True)
		
#CRATE VLESS
@bot.on(events.CallbackQuery(data=b'create7-vless'))
async def create_vless(event):
	async def create_vless_(event):
		async with bot.conversation(chat) as user:
			await event.edit(f"""
**✨ 𝙽𝚊𝚖𝚊 𝚋𝚎𝚛𝚞𝚙𝚊 𝚌𝚊𝚖𝚙𝚞𝚛𝚊𝚗, 
 𝙷𝚞𝚛𝚞𝚏 𝚔𝚊𝚙𝚒𝚝𝚊𝚕, 𝚍𝚊𝚗 𝙰𝚗𝚐𝚔𝚊**
**✨ No Space**
**✨ No double Name**
**✨ Bot : @abecasdee13**

**👉 Input Your UserName :**
/cancel Kembali KeMENU
""")
			user = user.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
			user = (await user).raw_text
		per = "/cancel"
		if user == per:
			await event.respond(f"""
**» CANCEL**
""",buttons=[[Button.inline("‹ Main Menu ›","menu")]])
		else:
			async with bot.conversation(chat) as exp:
				await event.respond(f"""
**👉 Input Your Expired (day) :**
""")
				exp = exp.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
				exp = (await exp).raw_text
			async with bot.conversation(chat) as pw:
				await event.respond(f"""
**👉 Input Your Limit IP Login :**
0 For Unlimited
""")
				pw = pw.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
				pw = (await pw).raw_text
			async with bot.conversation(chat) as pw2:
				await event.respond(f"""
**👉 Input Your Quota User :**
0 For Unlimited
""")
				pw2 = pw2.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
				pw2 = (await pw2).raw_text
			cmd = f'printf "%s\n" "1" "{user}" "{exp}" "{pw}" "{pw2}" | m-vless | sleep 2 | exit'
			subprocess.check_output(cmd, shell=True)
			await event.respond(f"""
**» SUCCES CREATE**
**» DONE**
""",buttons=[[Button.inline("‹ Main Menu ›","menu")]])
	chat = event.chat_id
	sender = await event.get_sender()
	a = valid(str(sender.id))
	if a == "true":
		await create_vless_(event)
	else:
		await event.answer("Akses Ditolak",alert=True)

# TRIAL vless
@bot.on(events.CallbackQuery(data=b'trial7-vless'))
async def trial_vless(event):
	async def trial_vless_(event):
		async with bot.conversation(chat) as exp:
			await event.edit(f"""
**👉 Input Your Timer (Minutes) :**
/cancel Kembali KeMENU
""")
			exp = exp.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
			exp = (await exp).raw_text
		per = "/cancel"
		if exp == per:
			await event.respond(f"""
**» CANCEL**
""",buttons=[[Button.inline("‹ Main Menu ›","menu")]])
		else:
			cmd = f'printf "%s\n" {2} "{exp}" | m-vless | sleep 2 | exit'
			subprocess.check_output(cmd, shell=True).decode("utf-8")
			await event.respond(f"""
**» SUCCES CREATE**
**» DONE**
""",buttons=[[Button.inline("‹ Main Menu ›","menu")]])
	chat = event.chat_id
	sender = await event.get_sender()
	a = valid(str(sender.id))
	if a == "true":
		await trial_vless_(event)
	else:
		await event.answer("Akses Ditolak",alert=True)

#CEK
@bot.on(events.CallbackQuery(data=b'cek7-vless'))
async def cek_vless(event):
	async def cek_vless_(event):
		time.sleep(0)
		await event.edit("`Processing... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
		time.sleep(0)
		await event.edit("`Processing... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
		time.sleep(0)
		await event.edit("`Processing... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
		time.sleep(0)
		cmd = 'bot-cek-vless'.strip()
		x = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
		print(x)
		z = subprocess.check_output(cmd, shell=True).decode("utf-8")
		await event.edit("`Processing... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
		time.sleep(1)
		await event.edit("`Processing... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
		time.sleep(1)
		await event.edit("`Processing... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `")
		time.sleep(1)
		await event.edit("`Processing... 84%\n█████████████████████▒▒▒▒ `")
		time.sleep(0)
		await event.edit("`Processing... 100%\n█████████████████████████ `")
		await event.edit(f"""
**⚠️ VLESS USER ONLINE**
{z}
""",buttons=[[Button.inline("‹ Main Menu ›","menu")]])
	sender = await event.get_sender()
	a = valid(str(sender.id))
	if a == "true":
		await cek_vless_(event)
	else:
		await event.answer("Access Denied",alert=True)

@bot.on(events.CallbackQuery(data=b'login7-vless'))
async def vless(event):
	async def vless_(event):
		inline = [
[Button.inline(" UNLOCK LOGIN ","loginip7-vless"),
Button.inline(" UNLOCK QUOTA ","logingb7-vless")],
[Button.inline("‹ Back ›","vless")]]
		await event.edit(buttons=inline)
	sender = await event.get_sender()
	a = valid(str(sender.id))
	if a == "true":
		await vless_(event)
	else:
		await event.answer("Access Denied",alert=True)
		
@bot.on(events.CallbackQuery(data=b'vless'))
async def vless(event):
	async def vless_(event):
		inline = [
[Button.inline(" Trial ","trial7-vless"),
Button.inline(" Create ","create7-vless"),
Button.inline(" Login ","cek7-vless")],
[Button.inline(" Delete ","delete7-vless"),
Button.inline(" Unlock ","login7-vless"),
Button.inline(" Limit ","limit7-vless")],
[Button.inline(" Renew","renew7-vless"),
Button.inline(" Restore ","restore7-vless"),
Button.inline(" Akun ","akun7-vless")],
[Button.inline("‹ BACK ›","menu")]]
		z = requests.get(f"http://ip-api.com/json/?fields=country,region,city,timezone,isp").json()
		vl = f' cat /etc/xray/config.json | grep "#vlg" | wc -l'
		vls = subprocess.check_output(vl, shell=True).decode("ascii")
		msg = f"""
**✧◇───────────────────◇✧** 
**🔥 MENU VLESS 🔥**
**✧◇───────────────────◇✧** 
✨ **» Service:** `VLESS`
✨ **» Total Account  :** `{vls.strip()}` __account__
✨ **» Host:** `{DOMAIN}`
✨ **» ISP:** `{z["isp"]}`
✨ **» Country:** `{z["country"]}`
🤖 **» @abecasdee13**
**✧◇───────────────────◇✧** 
"""
		await event.edit(msg,buttons=inline)
	sender = await event.get_sender()
	a = valid(str(sender.id))
	if a == "true":
		await vless_(event)
	else:
		await event.answer("Access Denied",alert=True)