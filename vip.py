import asyncio
from xC4 import Emote_k, SEndPacKeT  # Ye functions xC4 se utha lega

# --- SETTINGS ---
MY_BOSS_UID = "13947421096"  # <--- YAHAN APNI UID DALO
DELAY = 4  # Gap in seconds

# --- STATE VARIABLES ---
is_running = False
current_task = None

# --- EMOTE LISTS ---
EVO_IDS = [
    909000063, 909000081, 909000075, 909000085, 909000134,
    909000098, 909035007, 909051012, 909000141, 909034008,
    909051015, 909041002, 909039004, 909042008, 909051014,
    909039012, 909040010, 909035010, 909041005, 909051003, 909034001
]

MIX_IDS = [
    909000014, 909000034, 909000010, 909000006, 909000012, 
    909000020, 909000008, 909000045, 909049012, 909050028,
    909042007, 909050002, 909050015, 909050014, 909041013
]

async def start_loop(mode, uid, key, iv, region, whisper_writer, online_writer):
    global is_running
    is_running = True
    
    # Select List based on command
    target_list = EVO_IDS if mode == 'evo' else MIX_IDS
    
    print(f"VIP Loop Started: {mode}")
    
    while is_running:
        for emote_id in target_list:
            if not is_running: break
            try:
                # Send Emote
                H = await Emote_k(int(uid), int(emote_id), key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                
                # 4 Second Gap
                await asyncio.sleep(DELAY)
            except Exception as e:
                print(f"VIP Error: {e}")

async def handle_vip_command(msg, uid, key, iv, region, whisper_writer, online_writer):
    global is_running, current_task
    
    # 1. Security Check (Sirf tum chala paoge)
    if str(uid) != MY_BOSS_UID:
        return "❌ Tum Boss nahi ho!"

    # 2. Stop Command
    if msg == '/stop all':
        if is_running:
            is_running = False
            if current_task: current_task.cancel()
            return "🛑 Boss! Sab rok diya."
        return "⚠️ Pehle se band hai."

    # 3. Start Commands
    mode = None
    if msg == '/all_evo': mode = 'evo'
    elif msg == '/all': mode = 'mix'
    
    if mode:
        # Purana task roko agar chal raha ho
        if is_running:
            is_running = False
            if current_task: current_task.cancel()
            await asyncio.sleep(1)

        # Naya task shuru karo
        current_task = asyncio.create_task(
            start_loop(mode, uid, key, iv, region, whisper_writer, online_writer)
        )
        return f"✅ Boss! {mode.upper()} loop shuru kar diya (4s gap)."
    
    return None