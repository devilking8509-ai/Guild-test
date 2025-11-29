import asyncio
from xC4 import Emote_k

# ==========================================
# SETTINGS (Apni UID yahan dalein)
# ==========================================
MY_BOSS_UID = "13947421096"  
DELAY = 4  # 4 Second ka gap

# ==========================================
# SYSTEM VARIABLES
# ==========================================
evo_running = False
mix_running = False
current_task = None

# ==========================================
# LOCAL FUNCTION: PACKET SENDER
# ==========================================
async def SEndPacKeT(whisper_writer, online_writer, TypE, PacKeT):
    if TypE == 'ChaT' and whisper_writer:
        whisper_writer.write(PacKeT)
        await whisper_writer.drain()
    elif TypE == 'OnLine' and online_writer:
        online_writer.write(PacKeT)
        await online_writer.drain()

# ==========================================
# EMOTE LISTS
# ==========================================
EVO_LIST = [
    909000063, 909000081, 909000075, 909000085, 909000134,
    909000098, 909035007, 909051012, 909000141, 909034008,
    909051015, 909041002, 909039004, 909042008, 909051014,
    909039012, 909040010, 909035010, 909041005, 909051003, 
    909034001
]

MIX_LIST = [
    909000014, 909000034, 909000010, 909000006, 909000012, 
    909000020, 909000008, 909000045, 909049012, 909050028,
    909042007, 909050002, 909050015, 909050014, 909041013
]

# ==========================================
# LOGIC FUNCTIONS
# ==========================================
async def run_evo_loop(uid, key, iv, region, whisper_writer, online_writer):
    global evo_running
    print(">>> EVO LOOP STARTED")
    while evo_running:
        for emote_id in EVO_LIST:
            if not evo_running: break
            try:
                H = await Emote_k(int(uid), int(emote_id), key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                await asyncio.sleep(DELAY)
            except Exception as e:
                print(f"Loop Error: {e}")

async def run_mix_loop(uid, key, iv, region, whisper_writer, online_writer):
    global mix_running
    print(">>> MIX LOOP STARTED")
    while mix_running:
        for emote_id in MIX_LIST:
            if not mix_running: break
            try:
                H = await Emote_k(int(uid), int(emote_id), key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                await asyncio.sleep(DELAY)
            except Exception as e:
                print(f"Loop Error: {e}")

# ==========================================
# MAIN COMMAND HANDLER 
# (Corrected Name: handle_vip_command)
# ==========================================
async def handle_vip_command(msg, uid, key, iv, region, whisper_writer, online_writer):
    global evo_running, mix_running, current_task

    # 1. SECURITY CHECK
    if str(uid) != MY_BOSS_UID:
        return f"❌ Hat bey! Tu Boss nahi hai. (Your UID: {uid})"

    # 2. STOP COMMAND
    if msg == '/stop all':
        evo_running = False
        mix_running = False
        if current_task: current_task.cancel()
        return "🛑 Boss! Saare emotes rok diye."

    # 3. COMMAND: /all_evo
    if msg == '/all_evo':
        evo_running = False
        mix_running = False
        if current_task: current_task.cancel()
        await asyncio.sleep(1)
        evo_running = True
        current_task = asyncio.create_task(run_evo_loop(uid, key, iv, region, whisper_writer, online_writer))
        return "✅ Boss! EVO Emotes ki line laga di (4s gap)."

    # 4. COMMAND: /all
    if msg == '/all':
        evo_running = False
        mix_running = False
        if current_task: current_task.cancel()
        await asyncio.sleep(1)
        mix_running = True
        current_task = asyncio.create_task(run_mix_loop(uid, key, iv, region, whisper_writer, online_writer))
        return "✅ Boss! MIX Emotes (Flag/Throne) chalu ho gaye."

    return None
