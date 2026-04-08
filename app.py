import streamlit as st
from groq import Groq
from google import genai
from google.genai import types
import requests
import tempfile
import os
import base64
from PIL import Image
import io

# ══════════════════════════════════════════════════════════════
#  إعداد الصفحة
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Ornis IA",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ══════════════════════════════════════════════════════════════
#  CSS — واجهة الفضاء + Ornis IA
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;900&family=Tajawal:wght@300;400;700&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }

.stApp {
    background: #000510;
    font-family: 'Tajawal', sans-serif;
}

/* ── نجوم متحركة ── */
.stars-container {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    overflow: hidden;
    z-index: 0;
    pointer-events: none;
}

.stars {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: 
        radial-gradient(2px 2px at 10% 15%, #fff 0%, transparent 100%),
        radial-gradient(1px 1px at 25% 35%, rgba(255,255,255,0.8) 0%, transparent 100%),
        radial-gradient(2px 2px at 40% 10%, #fff 0%, transparent 100%),
        radial-gradient(1px 1px at 55% 50%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1px 1px at 70% 20%, #fff 0%, transparent 100%),
        radial-gradient(2px 2px at 85% 40%, rgba(255,255,255,0.9) 0%, transparent 100%),
        radial-gradient(1px 1px at 15% 60%, rgba(255,255,255,0.7) 0%, transparent 100%),
        radial-gradient(2px 2px at 30% 80%, #fff 0%, transparent 100%),
        radial-gradient(1px 1px at 60% 70%, rgba(255,255,255,0.8) 0%, transparent 100%),
        radial-gradient(1px 1px at 75% 85%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(2px 2px at 90% 65%, #fff 0%, transparent 100%),
        radial-gradient(1px 1px at 5%  90%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1px 1px at 45% 45%, rgba(255,200,100,0.8) 0%, transparent 100%),
        radial-gradient(2px 2px at 62% 30%, rgba(180,180,255,0.7) 0%, transparent 100%),
        radial-gradient(1px 1px at 20% 25%, rgba(255,255,200,0.9) 0%, transparent 100%);
    animation: twinkle 4s infinite alternate;
}

.stars2 {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background:
        radial-gradient(1px 1px at 8%  45%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(2px 2px at 33% 18%, #fff 0%, transparent 100%),
        radial-gradient(1px 1px at 48% 75%, rgba(255,255,255,0.7) 0%, transparent 100%),
        radial-gradient(1px 1px at 65% 55%, rgba(200,200,255,0.6) 0%, transparent 100%),
        radial-gradient(2px 2px at 78% 10%, rgba(255,255,255,0.9) 0%, transparent 100%),
        radial-gradient(1px 1px at 92% 30%, rgba(255,255,255,0.4) 0%, transparent 100%),
        radial-gradient(1px 1px at 18% 88%, rgba(255,220,150,0.7) 0%, transparent 100%),
        radial-gradient(2px 2px at 50% 95%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1px 1px at 82% 78%, #fff 0%, transparent 100%);
    animation: twinkle 6s infinite alternate-reverse;
}

/* سديم خلفي */
.nebula {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background:
        radial-gradient(ellipse at 20% 50%, rgba(30,0,80,0.4) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(0,30,80,0.3) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 80%, rgba(80,20,0,0.2) 0%, transparent 50%);
    z-index: 0;
    pointer-events: none;
}

@keyframes twinkle {
    0%   { opacity: 0.6; transform: scale(1); }
    50%  { opacity: 1;   transform: scale(1.02); }
    100% { opacity: 0.7; transform: scale(0.99); }
}

/* ── شاشة الترحيب ── */
.landing-container {
    position: relative;
    z-index: 10;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 85vh;
    text-align: center;
    padding: 40px 20px;
}

.logo-container {
    margin-bottom: 20px;
    animation: float 6s ease-in-out infinite;
}

@keyframes float {
    0%,100% { transform: translateY(0px); }
    50%      { transform: translateY(-15px); }
}

.logo-bird {
    font-size: 100px;
    filter: drop-shadow(0 0 30px rgba(212,175,55,0.8));
    animation: glow-pulse 3s ease-in-out infinite;
}

@keyframes glow-pulse {
    0%,100% { filter: drop-shadow(0 0 20px rgba(212,175,55,0.6)); }
    50%      { filter: drop-shadow(0 0 50px rgba(212,175,55,1)) drop-shadow(0 0 80px rgba(255,200,50,0.4)); }
}

.brand-name {
    font-family: 'Cinzel', serif;
    font-size: 80px;
    font-weight: 900;
    background: linear-gradient(135deg, #1a1a2e 0%, #d4af37 30%, #ffd700 50%, #d4af37 70%, #8b6914 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 8px;
    text-shadow: none;
    filter: drop-shadow(0 0 20px rgba(212,175,55,0.5));
    animation: brand-appear 2s ease-out forwards, shimmer 4s ease-in-out 2s infinite;
    opacity: 0;
}

@keyframes brand-appear {
    0%   { opacity: 0; transform: scale(0.5) translateY(30px); }
    60%  { opacity: 1; transform: scale(1.05) translateY(-5px); }
    100% { opacity: 1; transform: scale(1) translateY(0); }
}

@keyframes shimmer {
    0%,100% { filter: drop-shadow(0 0 15px rgba(212,175,55,0.4)); }
    50%      { filter: drop-shadow(0 0 40px rgba(255,215,0,0.8)); }
}

.brand-subtitle {
    font-family: 'Cinzel', serif;
    font-size: 14px;
    color: #d4af37;
    letter-spacing: 6px;
    margin-top: -10px;
    opacity: 0;
    animation: fade-in 1s ease-out 1.5s forwards;
}

@keyframes fade-in {
    to { opacity: 0.8; }
}

.tagline {
    font-family: 'Tajawal', sans-serif;
    color: rgba(255,255,255,0.7);
    font-size: 18px;
    margin: 30px 0;
    opacity: 0;
    animation: fade-in 1s ease-out 2s forwards;
}

.feature-pills {
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
    justify-content: center;
    margin: 20px 0 40px;
    opacity: 0;
    animation: fade-in 1s ease-out 2.5s forwards;
}

.pill {
    background: rgba(212,175,55,0.1);
    border: 1px solid rgba(212,175,55,0.4);
    border-radius: 30px;
    padding: 8px 20px;
    color: #d4af37;
    font-size: 14px;
}

/* ── زر الدخول ── */
.enter-btn-wrapper {
    opacity: 0;
    animation: fade-in 1s ease-out 3s forwards;
}

/* ── منطقة الشات ── */
.chat-header {
    position: relative;
    z-index: 10;
    text-align: center;
    padding: 20px 0 10px;
}

.chat-brand {
    font-family: 'Cinzel', serif;
    font-size: 36px;
    font-weight: 700;
    background: linear-gradient(135deg, #d4af37, #ffd700, #d4af37);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 4px;
}

.chat-bubble-user {
    background: linear-gradient(135deg, rgba(212,175,55,0.2), rgba(212,175,55,0.1));
    border: 1px solid rgba(212,175,55,0.4);
    border-radius: 20px 20px 5px 20px;
    padding: 15px 20px;
    margin: 10px 0;
    color: #ffd700;
    text-align: right;
    position: relative;
    z-index: 10;
}

.chat-bubble-bot {
    background: rgba(10,15,40,0.8);
    border: 1px solid rgba(212,175,55,0.2);
    border-radius: 20px 20px 20px 5px;
    padding: 15px 20px;
    margin: 10px 0;
    color: #e8e8e8;
    position: relative;
    z-index: 10;
    backdrop-filter: blur(10px);
}

.source-badge {
    display: inline-block;
    margin-top: 10px;
    background: rgba(212,175,55,0.1);
    border: 1px solid rgba(212,175,55,0.3);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.78em;
    color: #d4af37;
}

.stButton > button {
    background: linear-gradient(135deg, #8b6914, #d4af37, #ffd700) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 30px !important;
    padding: 12px 40px !important;
    font-family: 'Cinzel', serif !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    letter-spacing: 2px !important;
    transition: all 0.3s !important;
    box-shadow: 0 0 20px rgba(212,175,55,0.4) !important;
}
.stButton > button:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 0 40px rgba(212,175,55,0.7) !important;
}

.stSelectbox > div, .stRadio > div {
    background: transparent !important;
    color: #d4af37 !important;
}

label, .stRadio label { color: #d4af37 !important; }

.main > div { position: relative; z-index: 10; }

.divider-gold {
    height: 1px;
    background: linear-gradient(90deg, transparent, #d4af37, transparent);
    margin: 20px 0;
    position: relative;
    z-index: 10;
}

/* إخفاء عناصر Streamlit الزائدة */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; }
</style>

<!-- خلفية الفضاء -->
<div class="nebula"></div>
<div class="stars-container">
    <div class="stars"></div>
    <div class="stars2"></div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  إعداد APIs
# ══════════════════════════════════════════════════════════════
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
gemini_client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
EBIRD_KEY = st.secrets["EBIRD_API_KEY"]
GROQ_MODEL = "llama-3.3-70b-versatile"
GEMINI_MODEL = "gemini-1.5-flash-8b"

# ══════════════════════════════════════════════════════════════
#  System Prompts
# ══════════════════════════════════════════════════════════════
SYSTEM_PROMPTS = {
    "العربية": """أنت Ornis IA، خبير أورنيثولوجي (علم الطيور) متخصص.

قواعد صارمة لا تُخالَف أبداً:
1. أجب دائماً باللغة العربية الفصحى
2. اذكر الاسم العلمي اللاتيني لكل طائر
3. اذكر الاسم الشائع بالعربية والإنجليزية
4. كل معلومة تقدمها يجب أن يرافقها مصدر من هذه القائمة فقط:
   - Cornell Lab of Ornithology / AllAboutBirds.org
   - eBird (ebird.org)
   - BirdLife International (birdlife.org)
   - Handbook of the Birds of the World (HBW Alive)
   - Xeno-canto (xeno-canto.org) — للأصوات
   - Journal of Ornithology
   - The Auk: Ornithological Advances
   - Ostrich: Journal of African Ornithology
5. لا تستخدم أبداً: Wikipedia، مواقع عامة، مدونات
6. إذا لم تعرف المصدر الدقيق قل ذلك بصراحة
7. هيكل إجابتك دائماً:
   📋 المعلومة: [المعلومة العلمية]
   📚 المصدر: [اسم المصدر + رابطه إن أمكن]""",

    "English": """You are Ornis IA, a specialized ornithological expert AI.

Strict rules never to be broken:
1. Always answer in English
2. Always provide the Latin scientific name
3. Always provide common name in English and Arabic
4. Every piece of information MUST cite a source from this list ONLY:
   - Cornell Lab of Ornithology / AllAboutBirds.org
   - eBird (ebird.org)
   - BirdLife International (birdlife.org)
   - Handbook of the Birds of the World (HBW Alive)
   - Xeno-canto (xeno-canto.org) — for sounds
   - Journal of Ornithology
   - The Auk: Ornithological Advances
5. NEVER use: Wikipedia, general websites, blogs
6. If unsure about a source, say so honestly
7. Always structure answers as:
   📋 Information: [scientific fact]
   📚 Source: [source name + link if possible]""",

    "Français": """Vous êtes Ornis IA, un expert en ornithologie spécialisé.

Règles strictes:
1. Répondez toujours en français
2. Donnez toujours le nom scientifique latin
3. Chaque information DOIT citer une source de cette liste uniquement:
   - Cornell Lab of Ornithology / AllAboutBirds.org
   - eBird (ebird.org)
   - BirdLife International (birdlife.org)
   - Handbook of the Birds of the World (HBW Alive)
   - Xeno-canto (xeno-canto.org) — pour les sons
   - Journal of Ornithology
4. N'utilisez JAMAIS: Wikipedia, sites généraux, blogs
5. Structure de réponse:
   📋 Information: [fait scientifique]
   📚 Source: [nom de la source + lien si possible]"""
}

IMAGE_PROMPTS = {
    "العربية": """حدد هذا الطائر بدقة علمية تامة. قدم:
1. الاسم العربي الشائع
2. الاسم العلمي اللاتيني
3. العائلة (Family) والرتبة (Order)
4. الموطن الجغرافي والبيئي
5. المميزات المرئية التشخيصية
6. المصدر: Cornell Lab أو eBird أو BirdLife International فقط
لا تستخدم Wikipedia أو مصادر عامة.""",

    "English": """Identify this bird with full scientific precision. Provide:
1. Common English name
2. Latin scientific name
3. Family and Order
4. Geographic and ecological habitat
5. Diagnostic visual features
6. Source: Cornell Lab, eBird, or BirdLife International ONLY
Never use Wikipedia or general sources.""",

    "Français": """Identifiez cet oiseau avec précision scientifique. Fournissez:
1. Nom commun français
2. Nom scientifique latin
3. Famille et Ordre
4. Habitat géographique et écologique
5. Caractéristiques visuelles diagnostiques
6. Source: Cornell Lab, eBird, ou BirdLife International UNIQUEMENT"""
}

# ══════════════════════════════════════════════════════════════
#  دوال
# ══════════════════════════════════════════════════════════════
def chat_with_groq(user_message, language, history):
    messages = [{"role": "system", "content": SYSTEM_PROMPTS[language]}]
    for h in history[-10:]:  # آخر 10 رسائل فقط لتوفير الحصة
        role = "assistant" if h["role"] == "model" else "user"
        messages.append({"role": role, "content": h["content"]})
    messages.append({"role": "user", "content": user_message})
    
    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        max_tokens=1500,
        temperature=0.3
    )
    return response.choices[0].message.content

def analyze_bird_image(image_file, language):
    img_bytes = image_file.read()
    prompt = IMAGE_PROMPTS[language]
    response = gemini_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[
            types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg"),
            prompt
        ]
    )
    return response.text

def analyze_bird_audio(audio_file, language):
    try:
        from birdnetlib import Recording
        from birdnetlib.analyzer import Analyzer
        analyzer = Analyzer()
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio_file.read())
            tmp_path = tmp.name
        recording = Recording(
            analyzer, tmp_path,
            lat=36.7, lon=3.0,
            date_frmt="%Y-%m-%d", date="2024-06-01",
            min_conf=0.25
        )
        recording.analyze()
        os.unlink(tmp_path)
        
        if recording.detections:
            birds_text = "\n".join([
                f"- {d['common_name']} ({d['scientific_name']}): {d['confidence']:.0%} confidence"
                for d in recording.detections[:3]
            ])
            prompt = f"BirdNET detected these birds from audio:\n{birds_text}\n\nProvide detailed scientific info with sources from Cornell Lab/eBird/BirdLife only."
        else:
            prompt = "No bird was detected. Advise the user on how to make a better recording."
        
        return chat_with_groq(prompt, language, [])
    except Exception as e:
        return f"⚠️ خطأ في تحليل الصوت: {str(e)}"

# ══════════════════════════════════════════════════════════════
#  حالة التطبيق
# ══════════════════════════════════════════════════════════════
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "language" not in st.session_state:
    st.session_state.language = "العربية"

# ══════════════════════════════════════════════════════════════
#  صفحة الترحيب
# ══════════════════════════════════════════════════════════════
if st.session_state.page == "landing":
    st.markdown("""
    <div class="landing-container">
        <div class="logo-container">
            <div class="logo-bird">🦅</div>
        </div>
        <div class="brand-name">ORNIS IA</div>
        <div class="brand-subtitle">ORNITHOLOGICAL INTELLIGENCE</div>
        <div class="tagline">
            خبير الطيور الذكي — تعرّف، استكشف، تعلّم<br>
            <span style="font-size:14px;opacity:0.6">Powered by Advanced AI × Scientific Databases</span>
        </div>
        <div class="feature-pills">
            <div class="pill">🖼️ تحليل الصور</div>
            <div class="pill">🎵 تحليل الأصوات</div>
            <div class="pill">📚 مصادر علمية</div>
            <div class="pill">🌍 متعدد اللغات</div>
            <div class="pill">🔬 دقة أكاديمية</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        lang = st.selectbox("🌍 اختر لغتك", ["العربية", "English", "Français"], label_visibility="collapsed")
        st.session_state.language = lang
        if st.button("✦  ابدأ الاستكشاف  ✦", use_container_width=True):
            st.session_state.page = "chat"
            st.rerun()

# ══════════════════════════════════════════════════════════════
#  صفحة الشات
# ══════════════════════════════════════════════════════════════
else:
    # الشريط الجانبي
    with st.sidebar:
        st.markdown('<p style="color:#d4af37;font-family:Cinzel,serif;font-size:18px;letter-spacing:3px">⚙ ORNIS IA</p>', unsafe_allow_html=True)
        st.markdown('<div class="divider-gold"></div>', unsafe_allow_html=True)
        
        language = st.selectbox("🌍 اللغة", ["العربية", "English", "Français"],
                                index=["العربية", "English", "Français"].index(st.session_state.language))
        mode = st.radio("📌 الوضع", ["💬 محادثة", "🖼️ تحليل صورة", "🎵 تحليل صوت"])
        
        st.markdown('<div class="divider-gold"></div>', unsafe_allow_html=True)
        st.markdown("""
        <p style="color:#d4af37;font-size:13px">📚 المصادر العلمية</p>
        <p style="color:#aaa;font-size:12px">
        🔬 Cornell Lab of Ornithology<br>
        🐦 eBird Global Database<br>
        🌍 BirdLife International<br>
        📖 HBW Alive<br>
        🎵 Xeno-canto<br>
        📄 Journal of Ornithology
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="divider-gold"></div>', unsafe_allow_html=True)
        
        if st.button("🗑️ مسح المحادثة"):
            st.session_state.messages = []
            st.rerun()
        if st.button("🏠 الصفحة الرئيسية"):
            st.session_state.page = "landing"
            st.session_state.messages = []
            st.rerun()

    # رأس الصفحة
    st.markdown("""
    <div class="chat-header">
        <div class="chat-brand">🦅 ORNIS IA</div>
        <p style="color:rgba(212,175,55,0.6);font-size:13px;letter-spacing:3px">ORNITHOLOGICAL INTELLIGENCE</p>
    </div>
    <div class="divider-gold"></div>
    """, unsafe_allow_html=True)

    # عرض الرسائل
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-bubble-user">👤 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="chat-bubble-bot">🦅 {msg["content"]}'
                f'<br><span class="source-badge">📚 المصادر: Cornell Lab · eBird · BirdLife Int.</span></div>',
                unsafe_allow_html=True
            )

    st.markdown('<div class="divider-gold"></div>', unsafe_allow_html=True)

    # ── وضع الصورة
    if "🖼️" in mode:
        uploaded_img = st.file_uploader("📸 ارفع صورة الطائر", type=["jpg", "jpeg", "png", "webp"])
        if uploaded_img and st.button("🔍 تحليل الصورة"):
            with st.spinner("🔭 جارٍ التعرف على الطائر..."):
                result = analyze_bird_image(uploaded_img, language)
                st.session_state.messages.append({"role": "user", "content": "📸 [صورة طائر مرفوعة]"})
                st.session_state.messages.append({"role": "model", "content": result})
                st.rerun()

    # ── وضع الصوت
    elif "🎵" in mode:
        uploaded_audio = st.file_uploader("🎤 ارفع تسجيل صوت الطائر", type=["wav", "mp3", "ogg"])
        if uploaded_audio and st.button("🎧 تحليل الصوت"):
            with st.spinner("🔊 جارٍ تحليل الصوت..."):
                result = analyze_bird_audio(uploaded_audio, language)
                st.session_state.messages.append({"role": "user", "content": "🎵 [تسجيل صوتي مرفوع]"})
                st.session_state.messages.append({"role": "model", "content": result})
                st.rerun()

    # ── وضع المحادثة
    else:
        placeholder = {"العربية": "💬 اكتب سؤالك عن الطيور...",
                       "English": "💬 Ask anything about birds...",
                       "Français": "💬 Posez votre question sur les oiseaux..."}
        user_input = st.chat_input(placeholder[language])
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.spinner("🤔 ..."):
                reply = chat_with_groq(user_input, language, st.session_state.messages[:-1])
            st.session_state.messages.append({"role": "model", "content": reply})
            st.rerun()