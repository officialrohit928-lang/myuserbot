import asyncio
import os
import time
from pyrogram import Client, filters, idle
from pyrogram.types import Message

# ───── CONFIG ─────
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("SESSION")

if not API_ID or not API_HASH or not SESSION:
    raise ValueError("Environment variables missing!")

app = Client(
    "userbot",
    api_id=int(API_ID),
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

    # Check if user is owner
    if m.from_user.id != OWNER_ID:
        return await m.edit("❌ Sirf owner hi ye command use kar sakta hai")

    # Check if bot has admin permissions
    me = await app.get_chat_member(m.chat.id, "me")
    if not me.can_restrict_members:
        return await m.edit("❌ Userbot ke paas ban karne ki permission nahi hai")

    await m.edit("⚠️ BanAll started...")

    count = 0
    async for mem in app.get_chat_members(m.chat.id):
        try:
            if not mem.user.is_bot and mem.user.id != OWNER_ID and mem.user.id != m.from_user.id:
                await m.chat.ban_member(mem.user.id)
                count += 1
                await asyncio.sleep(0.3)
        except Exception as e:
            # Show failed bans for debugging
            await m.reply(f"❌ Failed to ban {mem.user.first_name} | Error: {e}")

    await m.edit(f"🚫 **BanAll Done**\n\nBanned: `{count}` users")

from pyrogram import Client, filters
import asyncio

app = Client("my_userbot")

# Stop flags
tag_running = False


# ================== ONETAG ==================
@app.on_message(filters.me & filters.command("onetag", prefixes="."))
async def one_tag(client, message):
    global tag_running
    tag_running = True

    if not message.chat.type in ["group", "supergroup"]:
        return await message.reply("❌ This command only works in groups.")

    text = " ".join(message.command[1:])
    if not text:
        return await message.reply("❌ Give some text.\nExample: .onetag Hello")

    await message.delete()

    async for member in client.get_chat_members(message.chat.id):
        if not tag_running:
            break

        user = member.user
        if user.is_bot:
            continue

        mention = user.mention
        try:
            await client.send_message(
                message.chat.id,
                f"{text} {mention}"
            )
            await asyncio.sleep(2)  # delay (important)
        except:
            continue


# ================== TAGALL ==================
@app.on_message(filters.me & filters.command("tagall", prefixes="."))
async def tag_all(client, message):
    global tag_running
    tag_running = True

    if not message.chat.type in ["group", "supergroup"]:
        return await message.reply("❌ This command only works in groups.")

    text = " ".join(message.command[1:])
    if not text:
        return await message.reply("❌ Give some text.\nExample: .tagall Hello")

    await message.delete()

    async for member in client.get_chat_members(message.chat.id):
        if not tag_running:
            break

        user = member.user
        if user.is_bot:
            continue

        mention = user.mention
        try:
            await client.send_message(
                message.chat.id,
                f"{text} {mention}"
            )
            await asyncio.sleep(1.5)
        except:
            continue


# ================== STOP COMMAND ==================
@app.on_message(filters.me & filters.command(["cancel", "tagstop"], prefixes="."))
async def stop_tag(client, message):
    global tag_running
    tag_running = False
    await message.reply("🛑 Tagging Stopped.")

    
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
if __name__ == "__main__":
    app.run()
