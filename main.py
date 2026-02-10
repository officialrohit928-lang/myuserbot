import asyncio
import os
import time
from pyrogram import Client, filters, idle
from pyrogram.types import Message

# ───── CONFIG ─────
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")
OWNER_ID = 7480255911  # 👈 Yaha apna Telegram ID daala

print("API_ID:", bool(API_ID))
print("API_HASH:", bool(API_HASH))
print("SESSION:", bool(SESSION))

# ───── CLIENT ─────
app = Client(
    "userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION
)

start_time = time.time()
AUTO_REPLY = False

# ───── BASIC COMMANDS ─────
@app.on_message(filters.me & filters.command("alive", "."))
async def alive(_, m: Message):
    await m.edit("✅ **Userbot Alive & Running**")

@app.on_message(filters.me & filters.command("ping", "."))
async def ping(_, m: Message):
    t1 = time.time()
    x = await m.edit("🏓 Pinging...")
    t2 = time.time()
    await x.edit(f"🏓 Pong `{int((t2-t1)*1000)}ms`")

@app.on_message(filters.me & filters.command("uptime", "."))
async def uptime(_, m: Message):
    up = int(time.time() - start_time)
    await m.edit(f"⏱ Uptime: `{up}s`")

# ───── FUN ─────
@app.on_message(filters.me & filters.command("love", "."))
async def love(_, m: Message):
    await m.edit("❤️ Love is in the air ✨")

@app.on_message(filters.me & filters.command("lover", "."))
async def lover(_, m: Message):
    await m.edit("💖 Hey lover 😌")

@app.on_message(filters.me & filters.command("hug", "."))
async def hug(_, m: Message):
    await m.edit("🤗 Virtual hug!")

@app.on_message(filters.me & filters.command("kiss", "."))
async def kiss(_, m: Message):
    await m.edit("😘 Sending a kiss")

# ───── AUTO REPLY ─────
@app.on_message(filters.me & filters.command("autoreply", "."))
async def autoreply(_, m: Message):
    global AUTO_REPLY
    AUTO_REPLY = not AUTO_REPLY
    await m.edit(f"🤖 Auto Reply: `{AUTO_REPLY}`")

@app.on_message(filters.private & ~filters.me)
async def auto(_, m: Message):
    if AUTO_REPLY:
        await m.reply("👋 Abhi busy hoon, baad me baat karte hain")

# ───── PROFILE ─────
@app.on_message(filters.me & filters.command("profile", ".") & filters.reply)
async def profile(_, m: Message):
    u = m.reply_to_message.from_user
    await m.edit(
        f"👤 **User Info**\n\n"
        f"• Name: {u.first_name}\n"
        f"• Username: @{u.username}\n"
        f"• ID: `{u.id}`"
    )

@app.on_message(filters.me & filters.command("bio", ".") & filters.reply)
async def bio(_, m: Message):
    u = await app.get_users(m.reply_to_message.from_user.id)
    await m.edit(f"📝 Bio:\n{u.bio or 'No bio'}")

@app.on_message(filters.me & filters.command("pfp", ".") & filters.reply)
async def pfp(_, m: Message):
    uid = m.reply_to_message.from_user.id
    async for p in app.get_chat_photos(uid, limit=1):
        await app.send_photo(m.chat.id, p.file_id)
        return
    await m.edit("❌ No profile photo")

@app.on_message(filters.me & filters.command("copyname", ".") & filters.reply)
async def copyname(_, m: Message):
    name = m.reply_to_message.from_user.first_name
    await m.edit(f"📋 Copied name:\n`{name}`")

# ───── TAGS ─────
@app.on_message(filters.me & filters.command("tagall", "."))
async def tagall(_, m: Message):
    if m.chat.type == "private":
        return await m.edit("❌ Group only")
    text = "🔔 **Tag All**\n"
    count = 0
    async for mem in app.get_chat_members(m.chat.id):
        if count >= 10:
            break
        if not mem.user.is_bot:
            text += f"[{mem.user.first_name}](tg://user?id={mem.user.id}) "
            count += 1
    await m.edit(text)

@app.on_message(filters.me & filters.command("onetag", "."))
async def onetag(_, m: Message):
    async for mem in app.get_chat_members(m.chat.id):
        if not mem.user.is_bot:
            return await m.edit(
                f"👋 [{mem.user.first_name}](tg://user?id={mem.user.id})"
            )

@app.on_message(filters.me & filters.command("adminstag", "."))
async def adminstag(_, m: Message):
    text = "👮 **Admins**\n"
    async for mem in app.get_chat_members(m.chat.id, filter="administrators"):
        text += f"[{mem.user.first_name}](tg://user?id={mem.user.id}) "
    await m.edit(text)

# ───── ADMIN ─────
@app.on_message(filters.me & filters.command("ban", ".") & filters.reply)
async def ban(_, m: Message):
    await m.chat.ban_member(m.reply_to_message.from_user.id)
    await m.edit("🚫 User banned")

@app.on_message(filters.me & filters.command("unban", "."))
async def unban(_, m: Message):
    await m.chat.unban_member(m.chat.id)
    await m.edit("✅ Unbanned")

@app.on_message(filters.me & filters.command("banall", "."))
async def banall(_, m: Message):
    if m.chat.type == "private":
        return await m.edit("❌ Group me use karo")

    await m.edit("⚠️ BanAll started...")

    count = 0
    async for mem in app.get_chat_members(m.chat.id):
        try:
            if not mem.user.is_bot and mem.user.id != OWNER_ID and mem.user.id != m.from_user.id:
                await m.chat.ban_member(mem.user.id)
                count += 1
                await asyncio.sleep(0.3)
        except:
            pass

    await m.edit(f"🚫 **BanAll Done**\n\nBanned: `{count}` users")

# ───── HELP ─────
@app.on_message(filters.me & filters.command("help", "."))
async def help(_, m: Message):
    await m.edit("""
🤖 **Userbot Commands**

.alive .ping .uptime
.love .lover .hug .kiss
.autoreply

.profile (reply)
.bio (reply)
.pfp (reply)
.copyname (reply)

.tagall .onetag .adminstag
.ban (reply) .unban
.banall (owner)

.help
""")

# ───── MAIN ─────
async def main():
    await app.start()
    print("✅ Userbot Started")
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
