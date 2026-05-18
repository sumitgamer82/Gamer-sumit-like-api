from flask import Flask, request, jsonify, render_template_string
import asyncio
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from google.protobuf.json_format import MessageToJson
import binascii
import aiohttp
import requests
import json
import like_pb2
import like_count_pb2
import uid_generator_pb2
from google.protobuf.message import DecodeError

app = Flask(__name__)

# =============================================================================
#  PREMIUM RED & GOLD HOMEPAGE (SUMIT GMR, SUMIT_GAMER, SUMIT_LIKE)
# =============================================================================
HOME_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>SUMIT GMR | OB53 Premium Gaming API</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --gold: #ffd700;
            --premium-red: #dc2626;
            --deep-red: #450a0a;
        }
        body {
            font-family: 'Inter', sans-serif;
            background-color: #0f0101;
            color: white;
            margin: 0;
            overflow-x: hidden;
            -webkit-tap-highlight-color: transparent;
        }
        .text-gradient {
            background: linear-gradient(to right, var(--gold), var(--premium-red), var(--gold));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .glass-premium {
            background: linear-gradient(to bottom, rgba(255,255,255,0.1), transparent);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 215, 0, 0.2);
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }
        .animate-pulse-gold {
            animation: pulse-gold 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }
        @keyframes pulse-gold {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: .8; transform: scale(1.02); box-shadow: 0 0 20px rgba(255, 215, 0, 0.3); }
        }
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }
        .animate-shake {
            animation: shake 0.2s ease-in-out infinite;
        }
        .safe-bottom { padding-bottom: env(safe-area-inset-bottom); }
        html { scroll-behavior: smooth; }
        .hidden { display: none !important; }
    </style>
</head>
<body class="pb-20 selection:bg-gold/30">

    <!-- 🔐 ACCESS OVERLAY -->
    <div id="auth-overlay" class="fixed inset-0 z-[100] bg-[#0f0101] flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-gradient-to-br from-red-900/20 via-transparent to-yellow-500/5 blur-[100px]"></div>
        <div class="glass-premium p-8 rounded-[2.5rem] w-full max-w-sm text-center space-y-6 relative z-10">
            <div class="w-20 h-20 bg-gradient-to-br from-red-950 via-red-600 to-red-950 rounded-3xl mx-auto flex items-center justify-center text-yellow-400 shadow-2xl border border-yellow-400/30">
                <i data-lucide="shield-check" class="w-10 h-10"></i>
            </div>
            <div class="space-y-2">
                <h2 class="text-2xl font-black text-gradient uppercase tracking-tighter">OB53 Premium Access</h2>
                <p class="text-[10px] text-white/40 font-black uppercase tracking-[0.2em]">Enter your elite access key</p>
            </div>
            <div class="space-y-4">
                <input type="text" id="access-key-input" placeholder="XXXX-XXXX-XXXX" 
                    class="w-full p-4 bg-black/60 rounded-2xl border border-yellow-400/20 focus:border-yellow-400 focus:outline-none text-center text-yellow-400 font-black tracking-widest uppercase transition-all">
                <button onclick="checkAccess()" 
                    class="w-full py-4 bg-gradient-to-r from-yellow-400 via-yellow-500 to-yellow-400 text-black font-black rounded-2xl shadow-xl shadow-yellow-400/20 active:scale-95 transition-all uppercase tracking-[0.2em] text-xs">
                    Unlock SUMIT
                </button>
            </div>
            <p class="text-[8px] text-white/20 font-black uppercase tracking-widest">Contact @SUMIT_GMR for access</p>
        </div>
    </div>

    <!-- MAIN CONTENT (hidden until authenticated) -->
    <div id="main-content" class="hidden">

        <!-- HEADER -->
        <header class="sticky top-0 z-50 bg-black/50 backdrop-blur-md border-b border-yellow-400/10">
            <div class="max-w-7xl mx-auto px-4 h-14 flex items-center justify-between">
                <div class="flex items-center gap-2">
                    <div class="w-8 h-8 bg-gradient-to-br from-red-950 via-red-600 to-red-950 rounded-lg flex items-center justify-center font-black text-yellow-400 text-sm border border-yellow-400/30 shadow-lg shadow-red-600/20">SG</div>
                    <h1 class="text-lg font-black tracking-tighter text-gradient uppercase">SUMIT GMR</h1>
                </div>
                <div class="flex items-center gap-2">
                    <button onclick="sharePage()" class="p-2 text-yellow-400/60 hover:text-yellow-400 transition-colors">
                        <i data-lucide="share-2" class="w-5 h-5"></i>
                    </button>
                    <button onclick="logout()" class="w-8 h-8 rounded-full bg-yellow-400/10 border border-yellow-400/20 flex items-center justify-center text-yellow-400 active:bg-yellow-400 active:text-black transition-all">
                        <i data-lucide="user" class="w-4 h-4"></i>
                    </button>
                </div>
            </div>
        </header>

        <main class="max-w-7xl mx-auto px-4 py-6 space-y-12">

            <!-- HERO SECTION -->
            <section id="home" class="text-center space-y-6 py-6">
                <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-red-600/10 border border-yellow-400/20 text-yellow-400 text-[9px] font-black uppercase tracking-widest">
                    <i data-lucide="flame" class="w-3 h-3 text-red-600 animate-pulse"></i> OB53 PREMIUM EDITION
                </div>
                <h2 class="text-3xl md:text-5xl font-black tracking-tighter leading-none uppercase">
                    The Ultimate <br><span class="text-gradient">Gaming SUMIT</span>
                </h2>
                <p class="max-w-xs mx-auto text-white/40 text-[11px] font-medium leading-relaxed">
                    Fastest, most reliable Free Fire OB53 profile enhancement in the world.
                </p>

                <!-- STATS CARDS -->
                <div class="grid grid-cols-2 md:grid-cols-4 gap-2 max-w-md mx-auto md:max-w-none">
                    <div class="glass-premium p-4 rounded-2xl text-center border-yellow-400/10" id="stat-delivered">
                        <p class="text-[8px] text-yellow-400/60 font-black uppercase mb-1">Delivered</p>
                        <p class="text-xl font-black text-white">1.2M+</p>
                    </div>
                    <div class="glass-premium p-4 rounded-2xl text-center border-yellow-400/10" id="stat-active">
                        <p class="text-[8px] text-yellow-400/60 font-black uppercase mb-1">Active</p>
                        <p class="text-xl font-black text-white">45K+</p>
                    </div>
                    <div class="glass-premium p-4 rounded-2xl text-center border-yellow-400/10" id="stat-uptime">
                        <p class="text-[8px] text-yellow-400/60 font-black uppercase mb-1">Uptime</p>
                        <p class="text-xl font-black text-white">99.9%</p>
                    </div>
                    <div class="glass-premium p-4 rounded-2xl text-center border-yellow-400/10" id="stat-status">
                        <p class="text-[8px] text-yellow-400/60 font-black uppercase mb-1">Status</p>
                        <p class="text-xl font-black text-white">Online</p>
                    </div>
                </div>
            </section>

            <!-- API TESTER -->
            <section id="api" class="space-y-4 scroll-mt-20">
                <h3 class="text-lg font-black text-white uppercase tracking-tight flex items-center gap-2">
                    <i data-lucide="terminal" class="w-5 h-5 text-yellow-400"></i> API TESTER (OB53)
                </h3>
                <div class="glass-premium p-5 rounded-3xl space-y-5 border-yellow-400/10">
                    <div class="space-y-4">
                        <input type="text" id="uid" placeholder="Enter Player UID" value="123456789"
                            class="w-full p-4 bg-black/40 rounded-xl border border-yellow-400/10 focus:border-yellow-400/50 focus:outline-none text-white font-mono text-sm transition-all">
                        <select id="region" class="w-full p-4 bg-black/40 rounded-xl border border-yellow-400/10 focus:border-yellow-400/50 focus:outline-none text-white font-black appearance-none transition-all">
                            <option value="BD">Bangladesh (BD)</option>
                            <option value="IND">India (IND)</option>
                            <option value="BR">Brazil (BR)</option>
                            <option value="US">USA (US)</option>
                        </select>
                    </div>
                    <button onclick="testApi()" 
                        class="w-full py-4 bg-gradient-to-r from-red-950 via-red-600 to-red-950 text-yellow-400 font-black rounded-xl border border-yellow-400/30 animate-pulse-gold uppercase tracking-widest text-[10px] active:scale-[0.96] transition-all flex items-center justify-center gap-2">
                        <i data-lucide="zap" class="w-4 h-4"></i> EXECUTE TEST (OB53)
                    </button>
                    <!-- RESPONSE AREA -->
                    <div id="response" class="bg-black/60 rounded-xl p-4 font-mono text-[9px] text-green-400 border border-yellow-400/10 min-h-[120px] whitespace-pre-wrap">
                        // OB53 System ready. Click execute to test.
                    </div>
                </div>
            </section>

            <!-- CHANNELS (YOUR  NAME)-->
            <section id="channels" class="space-y-4 scroll-mt-20">
                <h3 class="text-lg font-black text-white uppercase tracking-tight flex items-center gap-2">
                    <i data-lucide="layout-grid" class="w-5 h-5 text-yellow-400"></i> OUR SUMIT
                </h3>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                    <!-- SUMIT GMR -->
                    <div class="glass-premium p-5 rounded-3xl border-white/5">
                        <div class="flex items-start gap-4">
                            <div class="w-12 h-12 bg-gradient-to-br from-red-950 via-red-600 to-red-950 rounded-xl flex items-center justify-center text-yellow-400 border border-yellow-400/20">SG</div>
                            <div>
                                <h4 class="text-base font-black text-yellow-400 uppercase">SUMIT GMR</h4>
                                <p class="text-white/40 text-[10px] font-medium">Main channel – OB53 exclusive content</p>
                            </div>
                        </div>
                        <a href="https://t.me/SUMIT_GMR" target="_blank" class="mt-4 flex items-center justify-center gap-2 w-full py-3 bg-white/5 active:bg-yellow-400 text-white active:text-black rounded-xl text-[10px] font-black uppercase tracking-widest border border-white/10 transition-all">
                            Subscribe <i data-lucide="external-link" class="w-3 h-3"></i>
                        </a>
                    </div>
                    <!-- SUMIT GAMER -->
                    <div class="glass-premium p-5 rounded-3xl border-white/5">
                        <div class="flex items-start gap-4">
                            <div class="w-12 h-12 bg-gradient-to-br from-red-950 via-red-600 to-red-950 rounded-xl flex items-center justify-center text-yellow-400 border border-yellow-400/20">KK</div>
                            <div>
                                <h4 class="text-base font-black text-yellow-400 uppercase">SUMIT GAMER</h4>
                                <p class="text-white/40 text-[10px] font-medium">Gaming channel – OB53 tips & gameplay</p>
                            </div>
                        </div>
                        <a href="https://t.me/SUMIT_GMR" target="_blank" class="mt-4 flex items-center justify-center gap-2 w-full py-3 bg-white/5 active:bg-yellow-400 text-white active:text-black rounded-xl text-[10px] font-black uppercase tracking-widest border border-white/10 transition-all">
                            Subscribe <i data-lucide="external-link" class="w-3 h-3"></i>
                        </a>
                    </div>
                    <!-- SUMIT X SUMIT -->
                    <div class="glass-premium p-5 rounded-3xl border-white/5">
                        <div class="flex items-start gap-4">
                            <div class="w-12 h-12 bg-gradient-to-br from-red-950 via-red-600 to-red-950 rounded-xl flex items-center justify-center text-yellow-400 border border-yellow-400/20">RK</div>
                            <div>
                                <h4 class="text-base font-black text-yellow-400 uppercase">SUMIT X SUMIT</h4>
                                <p class="text-white/40 text-[10px] font-medium">Competitive OB53 tournament coverage</p>
                            </div>
                        </div>
                        <a href="https://t.me/SUMIT_GMR" target="_blank" class="mt-4 flex items-center justify-center gap-2 w-full py-3 bg-white/5 active:bg-yellow-400 text-white active:text-black rounded-xl text-[10px] font-black uppercase tracking-widest border border-white/10 transition-all">
                            Subscribe <i data-lucide="external-link" class="w-3 h-3"></i>
                        </a>
                    </div>
                </div>
            </section>

            <!-- DOCUMENTATION -->
            <section id="docs" class="glass-premium p-6 rounded-[2rem] border-yellow-400/10 scroll-mt-20">
                <h3 class="text-lg font-black text-white uppercase tracking-tight flex items-center gap-2 mb-4">
                    <i data-lucide="book-open" class="w-5 h-5 text-yellow-400"></i> OB53 DOCS
                </h3>
                <div class="space-y-3 text-[10px]">
                    <div class="bg-black/40 p-3 rounded-xl border border-yellow-400/10 font-mono">GET /like?uid={UID}&server_name={SERVER}</div>
                    <div class="grid grid-cols-2 gap-2 text-white/60">
                        <span class="font-black text-yellow-400">uid</span> <span>required</span>
                        <span class="font-black text-yellow-400">server</span> <span>BD, IND, BR, US</span>
                    </div>
                    <div class="mt-2 text-yellow-400/40 text-[8px]">Release Version: OB53</div>
                </div>
            </section>
        </main>

        <!-- FOOTER -->
        <footer class="glass-premium border-t border-yellow-400/20 mt-12 rounded-t-[3rem] overflow-hidden">
            <div class="max-w-7xl mx-auto px-6 py-12 space-y-10">
                <div class="flex flex-col md:flex-row justify-between items-center gap-8">
                    <div class="text-center md:text-left space-y-4">
                        <div class="flex items-center justify-center md:justify-start gap-3">
                            <div class="w-10 h-10 bg-gradient-to-br from-red-950 via-red-600 to-red-950 rounded-xl flex items-center justify-center font-black text-yellow-400 border border-yellow-400/30">SG</div>
                            <h1 class="text-2xl font-black tracking-tighter text-gradient uppercase">SUMIT GMR</h1>
                        </div>
                        <p class="text-white/40 text-[11px] max-w-xs">The world's most advanced OB53 profile enhancement infrastructure. Built for performance, secured for the elite.</p>
                    </div>
                    <div class="flex flex-wrap justify-center gap-3">
                        <a href="https://t.me/SUMIT_GMR" target="_blank" class="p-3 bg-white/5 rounded-xl text-yellow-400/60 hover:text-yellow-400 border border-yellow-400/5 transition-colors"><i data-lucide="message-square" class="w-5 h-5"></i></a>
                        <a href="#" class="p-3 bg-white/5 rounded-xl text-yellow-400/60 hover:text-yellow-400 border border-yellow-400/5 transition-colors"><i data-lucide="globe" class="w-5 h-5"></i></a>
                        <a href="mailto:support@SUMIT_GMR.com" class="p-3 bg-white/5 rounded-xl text-yellow-400/60 hover:text-yellow-400 border border-yellow-400/5 transition-colors"><i data-lucide="mail" class="w-5 h-5"></i></a>
                    </div>
                </div>
                <div class="pt-8 border-t border-yellow-400/10 flex flex-col md:flex-row justify-between items-center gap-4">
                    <p class="text-[8px] font-black uppercase tracking-[0.4em] text-white/20">
                        © 2026 SUMIT GMR · OB53 RED & GOLD EDITION
                    </p>
                    <div class="flex items-center gap-2 text-[8px] font-black text-white/20">
                        <span class="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse"></span> OB53 ACTIVE
                    </div>
                </div>
            </div>
        </footer>

        <!-- BOTTOM NAVIGATION -->
        <nav class="fixed bottom-0 left-0 right-0 z-50 bg-black/80 backdrop-blur-lg border-t border-yellow-400/10 safe-bottom md:hidden">
            <div class="flex justify-around items-center h-16">
                <a href="#home" class="flex flex-col items-center gap-1 text-yellow-400">
                    <i data-lucide="home" class="w-5 h-5"></i>
                    <span class="text-[8px] font-black uppercase">Home</span>
                </a>
                <a href="#api" class="flex flex-col items-center gap-1 text-white/40">
                    <i data-lucide="terminal" class="w-5 h-5"></i>
                    <span class="text-[8px] font-black uppercase">API</span>
                </a>
                <a href="#channels" class="flex flex-col items-center gap-1 text-white/40">
                    <i data-lucide="layout-grid" class="w-5 h-5"></i>
                    <span class="text-[8px] font-black uppercase">Elite</span>
                </a>
            </div>
        </nav>
    </div>

    <script>
        lucide.createIcons();

        function checkAccess() {
            const key = document.getElementById('access-key-input').value.toUpperCase();
            const input = document.getElementById('access-key-input');
            if (key === 'SUMIT_ZX') {
                localStorage.setItem('SUMIT_access_key', key);
                document.getElementById('auth-overlay').classList.add('hidden');
                document.getElementById('main-content').classList.remove('hidden');
                fetchStats();
            } else {
                input.classList.add('animate-shake', 'border-red-500');
                setTimeout(() => input.classList.remove('animate-shake', 'border-red-500'), 500);
            }
        }

        function logout() {
            localStorage.removeItem('SUMIT_access_key');
            location.reload();
        }

        function sharePage() {
            if (navigator.share) {
                navigator.share({ title: 'SUMIT GMR OB53', url: window.location.href });
            } else {
                navigator.clipboard.writeText(window.location.href);
                alert('Link copied!');
            }
        }

        async function fetchStats() {
            try {
                const res = await fetch('/api/stats');
                const data = await res.json();
                document.querySelector('#stat-delivered p:last-child').innerText = data.delivered;
                document.querySelector('#stat-active p:last-child').innerText = data.active;
                document.querySelector('#stat-uptime p:last-child').innerText = data.uptime;
                document.querySelector('#stat-status p:last-child').innerText = data.status;
            } catch (e) { console.error('Stats fetch failed', e); }
        }

        async function testApi() {
            const uid = document.getElementById('uid').value.trim();
            const region = document.getElementById('region').value;
            const responseDiv = document.getElementById('response');
            if (!uid) { responseDiv.innerText = '// Please enter a UID'; return; }
            responseDiv.innerText = '> Connecting to OB53 SUMIT API...\\n> Processing UID: ' + uid + '\\n> Region: ' + region;
            try {
                const res = await fetch(`/like?uid=${uid}&server_name=${region}`);
                const data = await res.json();
                responseDiv.innerText = JSON.stringify(data, null, 2);
                fetchStats();
            } catch (error) {
                responseDiv.innerText = '// OB53 Error: ' + error.message;
            }
        }

        window.onload = () => {
            if (localStorage.getItem('SUMIT_access_key') === 'SUMIT_ZX') {
                document.getElementById('auth-overlay').classList.add('hidden');
                document.getElementById('main-content').classList.remove('hidden');
                fetchStats();
            }
            lucide.createIcons();
        };
    </script>
</body>
</html>
'''

# =============================================================================
#  BACKEND FUNCTIONS (UPDATED FOR OB53)
# =============================================================================

def load_tokens(server_name):
    try:
        if server_name == "IND":
            with open("token_ind.json", "r") as f:
                tokens = json.load(f)
        elif server_name in {"BR", "US", "SAC", "NA"}:
            with open("token_br.json", "r") as f:
                tokens = json.load(f)
        else:
            with open("token_bd.json", "r") as f:
                tokens = json.load(f)
        return tokens
    except Exception as e:
        app.logger.error(f"Error loading tokens for server {server_name}: {e}")
        return None

def encrypt_message(plaintext):
    try:
        key = b'Yg&tc%DEuh6%Zc^8'
        iv = b'6oyZDr22E3ychjM%'
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_message = pad(plaintext, AES.block_size)
        encrypted_message = cipher.encrypt(padded_message)
        return binascii.hexlify(encrypted_message).decode('utf-8')
    except Exception as e:
        app.logger.error(f"Error encrypting message: {e}")
        return None

def create_protobuf_message(user_id, region):
    try:
        message = like_pb2.like()
        message.uid = int(user_id)
        message.region = region
        return message.SerializeToString()
    except Exception as e:
        app.logger.error(f"Error creating protobuf message: {e}")
        return None

async def send_request(encrypted_uid, token, url):
    try:
        edata = bytes.fromhex(encrypted_uid)
        headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Authorization': f"Bearer {token}",
            'Content-Type': "application/x-www-form-urlencoded",
            'Expect': "100-continue",
            'X-Unity-Version': "2018.4.11f1",
            'X-GA': "v1 1",
            'ReleaseVersion': "OB53"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=edata, headers=headers) as response:
                if response.status != 200:
                    app.logger.error(f"Request failed with status code: {response.status}")
                    return response.status
                return await response.text()
    except Exception as e:
        app.logger.error(f"Exception in send_request: {e}")
        return None

async def send_multiple_requests(uid, server_name, url):
    try:
        region = server_name
        protobuf_message = create_protobuf_message(uid, region)
        if protobuf_message is None:
            app.logger.error("Failed to create protobuf message.")
            return None
        encrypted_uid = encrypt_message(protobuf_message)
        if encrypted_uid is None:
            app.logger.error("Encryption failed.")
            return None
        tasks = []
        tokens = load_tokens(server_name)
        if tokens is None:
            app.logger.error("Failed to load tokens.")
            return None
        for i in range(100):
            token = tokens[i % len(tokens)]["token"]
            tasks.append(send_request(encrypted_uid, token, url))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
    except Exception as e:
        app.logger.error(f"Exception in send_multiple_requests: {e}")
        return None

def create_protobuf(uid):
    try:
        message = uid_generator_pb2.uid_generator()
        message.saturn_ = int(uid)
        message.garena = 1
        return message.SerializeToString()
    except Exception as e:
        app.logger.error(f"Error creating uid protobuf: {e}")
        return None

def enc(uid):
    protobuf_data = create_protobuf(uid)
    if protobuf_data is None:
        return None
    encrypted_uid = encrypt_message(protobuf_data)
    return encrypted_uid

def make_request(encrypt, server_name, token):
    try:
        if server_name == "IND":
            url = "https://client.ind.freefiremobile.com/GetPlayerPersonalShow"
        elif server_name in {"BR", "US", "SAC", "NA"}:
            url = "https://client.us.freefiremobile.com/GetPlayerPersonalShow"
        else:
            url = "https://clientbp.ggpolarbear.com/GetPlayerPersonalShow"
        edata = bytes.fromhex(encrypt)
        headers = {
            'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Authorization': f"Bearer {token}",
            'Content-Type': "application/x-www-form-urlencoded",
            'Expect': "100-continue",
            'X-Unity-Version': "2018.4.11f1",
            'X-GA': "v1 1",
            'ReleaseVersion': "OB53"
        }
        response = requests.post(url, data=edata, headers=headers, verify=False)
        hex_data = response.content.hex()
        binary = bytes.fromhex(hex_data)
        decode = decode_protobuf(binary)
        if decode is None:
            app.logger.error("Protobuf decoding returned None.")
        return decode
    except Exception as e:
        app.logger.error(f"Error in make_request: {e}")
        return None

def decode_protobuf(binary):
    try:
        items = like_count_pb2.Info()
        items.ParseFromString(binary)
        return items
    except DecodeError as e:
        app.logger.error(f"Error decoding Protobuf data: {e}")
        return None
    except Exception as e:
        app.logger.error(f"Unexpected error during protobuf decoding: {e}")
        return None

def fetch_player_info(uid):
    try:
        url = f"https://mafuuuu-info-api.vercel.app/mafu-info?uid={uid}"
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            data = response.json()
            account_info = data.get("AccountInfo", {})
            return {
                "Level": account_info.get("AccountLevel", "NA"),
                "Region": account_info.get("AccountRegion", "NA"),
                "ReleaseVersion": account_info.get("ReleaseVersion", "NA")
            }
        else:
            app.logger.error(f"Player info API failed with status code: {response.status_code}")
            return {"Level": "NA", "Region": "NA", "ReleaseVersion": "NA"}
    except Exception as e:
        app.logger.error(f"Error fetching player info from API: {e}")
        return {"Level": "NA", "Region": "NA", "ReleaseVersion": "NA"}

# =============================================================================
#  ROUTES
# =============================================================================

@app.route('/')
def home():
    return render_template_string(HOME_PAGE)

@app.route('/api/stats')
def stats():
    return jsonify({
        "delivered": "2.5M+",
        "active": "67K+",
        "uptime": "99.99%",
        "status": "OB53 Online"
    })

@app.route('/like', methods=['GET'])
def handle_requests():
    uid = request.args.get("uid")
    server_name = request.args.get("server_name", "").upper()
    if not uid or not server_name:
        return jsonify({"error": "UID and server_name are required"}), 400

    try:
        def process_request():
            player_info = fetch_player_info(uid)
            region = player_info["Region"]
            level = player_info["Level"]
            release_version = player_info["ReleaseVersion"]

            if region != "NA" and server_name != region:
                app.logger.warning(f"Server name {server_name} does not match API region {region}. Using API region.")
                server_name_used = region
            else:
                server_name_used = server_name

            tokens = load_tokens(server_name_used)
            if tokens is None:
                raise Exception("Failed to load tokens.")
            token = tokens[0]['token']
            encrypted_uid = enc(uid)
            if encrypted_uid is None:
                raise Exception("Encryption of UID failed.")

            before = make_request(encrypted_uid, server_name_used, token)
            if before is None:
                raise Exception("Failed to retrieve initial player info.")
            try:
                jsone = MessageToJson(before)
            except Exception as e:
                raise Exception(f"Error converting 'before' protobuf to JSON: {e}")
            data_before = json.loads(jsone)
            before_like = data_before.get('AccountInfo', {}).get('Likes', 0)
            try:
                before_like = int(before_like)
            except Exception:
                before_like = 0
            app.logger.info(f"Likes before command: {before_like}")

            if server_name_used == "IND":
                url = "https://client.ind.freefiremobile.com/LikeProfile"
            elif server_name_used in {"BR", "US", "SAC", "NA"}:
                url = "https://client.us.freefiremobile.com/LikeProfile"
            else:
                url = "https://clientbp.ggpolarbear.com/LikeProfile"

            asyncio.run(send_multiple_requests(uid, server_name_used, url))

            after = make_request(encrypted_uid, server_name_used, token)
            if after is None:
                raise Exception("Failed to retrieve player info after like requests.")
            try:
                jsone_after = MessageToJson(after)
            except Exception as e:
                raise Exception(f"Error converting 'after' protobuf to JSON: {e}")
            data_after = json.loads(jsone_after)
            after_like = int(data_after.get('AccountInfo', {}).get('Likes', 0))
            player_uid = int(data_after.get('AccountInfo', {}).get('UID', 0))
            player_name = str(data_after.get('AccountInfo', {}).get('PlayerNickname', ''))
            like_given = after_like - before_like
            status = 1 if like_given != 0 else 2
            result = {
                "LikesGivenByAPI": like_given,
                "LikesafterCommand": after_like,
                "LikesbeforeCommand": before_like,
                "PlayerNickname": player_name,
                "Region": region,
                "Level": level,
                "UID": player_uid,
                "ReleaseVersion": release_version,
                "status": status,
                "OB53": "Active"
            }
            return result

        result = process_request()
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
