import streamlit as st
from groq import Groq
from google import genai
from google.genai import types
import tempfile
import os

st.set_page_config(
    page_title="Ornis IA",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Cormorant+Garamond:wght@300;400;600;700&family=Tajawal:wght@300;400;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.stApp { background: #04080f; font-family: 'Tajawal', serif; }

.space-bg {
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background:
        radial-gradient(ellipse at 15% 40%, rgba(40,10,80,0.6) 0%, transparent 55%),
        radial-gradient(ellipse at 85% 15%, rgba(10,30,80,0.5) 0%, transparent 55%),
        radial-gradient(ellipse at 50% 90%, rgba(60,15,10,0.3) 0%, transparent 50%),
        #04080f;
}

.stars-layer {
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background-image:
        radial-gradient(1.5px 1.5px at 8%  12%, #fff 0%, transparent 100%),
        radial-gradient(1px   1px   at 22%  5%, rgba(255,255,255,0.8) 0%, transparent 100%),
        radial-gradient(2px   2px   at 37% 22%, #fff 0%, transparent 100%),
        radial-gradient(1px   1px   at 53%  8%, rgba(255,220,150,0.9) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 68% 18%, #fff 0%, transparent 100%),
        radial-gradient(1px   1px   at 82%  6%, rgba(180,200,255,0.8) 0%, transparent 100%),
        radial-gradient(2px   2px   at 91% 30%, #fff 0%, transparent 100%),
        radial-gradient(1px   1px   at 14% 45%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 28% 55%, #fff 0%, transparent 100%),
        radial-gradient(1px   1px   at 43% 48%, rgba(255,240,180,0.7) 0%, transparent 100%),
        radial-gradient(2px   2px   at 59% 62%, #fff 0%, transparent 100%),
        radial-gradient(1px   1px   at 74% 50%, rgba(200,210,255,0.8) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 88% 45%, #fff 0%, transparent 100%),
        radial-gradient(1px   1px   at 6%  72%, rgba(255,255,255,0.7) 0%, transparent 100%),
        radial-gradient(2px   2px   at 20% 80%, #fff 0%, transparent 100%),
        radial-gradient(1px   1px   at 35% 88%, rgba(255,220,150,0.6) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 50% 75%, #fff 0%, transparent 100%),
        radial-gradient(1px   1px   at 65% 85%, rgba(180,200,255,0.7) 0%, transparent 100%),
        radial-gradient(2px   2px   at 79% 78%, #fff 0%, transparent 100%),
        radial-gradient(1px   1px   at 94% 68%, rgba(255,255,255,0.5) 0%, transparent 100%);
    animation: twinkle 5s ease-in-out infinite alternate;
}

.stars-layer-2 {
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background-image:
        radial-gradient(1px 1px at 11% 28%, rgba(255,255,255,0.5) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 26% 15%, #fff 0%, transparent 100%),
        radial-gradient(1px 1px at 41% 35%, rgba(255,230,160,0.6) 0%, transparent 100%),
        radial-gradient(2px 2px at 57% 42%, rgba(255,255,255,0.8) 0%, transparent 100%),
        radial-gradient(1px 1px at 72% 32%, rgba(200,215,255,0.7) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 87% 58%, #fff 0%, transparent 100%),
        radial-gradient(1px 1px at 4%  62%, rgba(255,255,255,0.6) 0%, transparent 100%),
        radial-gradient(2px 2px at 18% 70%, #fff 0%, transparent 100%),
        radial-gradient(1px 1px at 33% 65%, rgba(255,220,150,0.5) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 48% 92%, #fff 0%, transparent 100%),
        radial-gradient(1px 1px at 63% 95%, rgba(255,255,255,0.7) 0%, transparent 100%),
        radial-gradient(2px 2px at 77% 88%, rgba(180,200,255,0.6) 0%, transparent 100%),
        radial-gradient(1px 1px at 92% 82%, #fff 0%, transparent 100%);
    animation: twinkle 7s ease-in-out infinite alternate-reverse;
}

@keyframes twinkle {
    0%   { opacity: 0.5; }
    50%  { opacity: 1;   }
    100% { opacity: 0.6; }
}

.landing-wrap {
    position: relative; z-index: 10;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    min-height: 90vh; padding: 60px 20px 40px;
    text-align: center;
}

.bird-icon {
    font-size: 90px; line-height: 1;
    animation: float 5s ease-in-out infinite, glow-bird 3s ease-in-out infinite alternate;
    margin-bottom: 30px;
}

@keyframes float {
    0%,100% { transform: translateY(0); }
    50%      { transform: translateY(-18px); }
}
@keyframes glow-bird {
    0%   { filter: drop-shadow(0 0 15px rgba(212,175,55,0.5)); }
    100% { filter: drop-shadow(0 0 45px rgba(255,215,0,0.9)) drop-shadow(0 0 70px rgba(212,175,55,0.4)); }
}

.brand-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(56px, 10vw, 110px);
    font-weight: 900; letter-spacing: 12px; line-height: 1;
    background: linear-gradient(180deg,#fffbe6 0%,#ffd700 15%,#d4af37 35%,#8b6914 50%,#d4af37 65%,#ffd700 80%,#c8960c 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    filter: drop-shadow(0 2px 30px rgba(212,175,55,0.6));
    animation: title-in 1.8s cubic-bezier(.23,1.01,.32,1) forwards; opacity: 0;
}
@keyframes title-in {
    0%   { opacity:0; transform:scale(0.6) translateY(40px); }
    70%  { opacity:1; transform:scale(1.04) translateY(-6px); }
    100% { opacity:1; transform:scale(1) translateY(0); }
}
.brand-ia {
    font-family: 'Cormorant Garamond', serif; font-size: clamp(12px,2vw,18px);
    font-weight: 300; letter-spacing: 14px; color: rgba(212,175,55,0.7);
    margin-top: 6px; animation: fade-up 1s ease-out 1.5s forwards; opacity: 0;
    text-transform: uppercase;
}
.gold-line {
    width: 280px; height: 1px;
    background: linear-gradient(90deg, transparent, #d4af37, #ffd700, #d4af37, transparent);
    margin: 24px auto; animation: fade-up 1s ease-out 2s forwards; opacity: 0;
}
.tagline {
    font-family: 'Tajawal', sans-serif; color: rgba(255,255,255,0.65);
    font-size: clamp(14px,2vw,18px); line-height: 1.8; max-width: 560px;
    animation: fade-up 1s ease-out 2.2s forwards; opacity: 0;
}
@keyframes fade-up {
    0%   { opacity:0; transform:translateY(20px); }
    100% { opacity:1; transform:translateY(0); }
}
.features-row {
    display: flex; gap: 12px; flex-wrap: wrap; justify-content: center;
    margin: 30px 0; animation: fade-up 1s ease-out 2.6s forwards; opacity: 0;
}
.feat-pill {
    background: rgba(212,175,55,0.08); border: 1px solid rgba(212,175,55,0.35);
    border-radius: 40px; padding: 9px 22px; color: #d4af37;
    font-family: 'Tajawal', sans-serif; font-size: 13px;
}

.chat-top {
    position: relative; z-index: 10; text-align: center;
    padding: 24px 0 8px;
    border-bottom: 1px solid rgba(212,175,55,0.15); margin-bottom: 16px;
}
.chat-logo {
    font-family: 'Playfair Display', serif;
    font-size: clamp(28px,5vw,48px); font-weight: 900; letter-spacing: 8px;
    background: linear-gradient(180deg,#ffd700 0%,#d4af37 50%,#8b6914 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    filter: drop-shadow(0 0 12px rgba(212,175,55,0.5));
}
.chat-sub {
    font-family: 'Cormorant Garamond', serif; color: rgba(212,175,55,0.5);
    letter-spacing: 5px; font-size: 11px; text-transform: uppercase; margin-top: 4px;
}

.bubble-user {
    background: linear-gradient(135deg, rgba(212,175,55,0.15), rgba(212,175,55,0.07));
    border: 1px solid rgba(212,175,55,0.35);
    border-radius: 18px 18px 4px 18px;
    padding: 14px 20px; margin: 10px 0;
    color: #fde68a; font-family: 'Tajawal', sans-serif; font-size: 15px;
    position: relative; z-index: 10;
}
.bubble-bot {
    background: rgba(8,14,35,0.85);
    border: 1px solid rgba(212,175,55,0.18);
    border-radius: 18px 18px 18px 4px;
    padding: 18px 22px; margin: 10px 0;
    color: #e8e6e0; font-family: 'Tajawal', sans-serif;
    font-size: 15px; line-height: 1.85;
    position: relative; z-index: 10; backdrop-filter: blur(12px);
}
.src-badge {
    display: inline-flex; align-items: center; gap: 6px;
    margin-top: 12px; background: rgba(212,175,55,0.08);
    border: 1px solid rgba(212,175,55,0.25); border-radius: 20px;
    padding: 5px 16px; font-size: 11px; color: #d4af37; letter-spacing: 0.5px;
}

.upload-card {
    position: relative; z-index: 10;
    background: rgba(8,14,35,0.75);
    border: 1px solid rgba(212,175,55,0.25);
    border-radius: 16px; padding: 28px;
    margin-bottom: 20px; backdrop-filter: blur(10px);
}
.upload-card-title {
    font-family: 'Playfair Display', serif;
    color: #d4af37; font-size: 20px; letter-spacing: 3px;
    margin-bottom: 20px;
}

/* ── MODE BUTTONS ── */
div[data-testid="column"] .stButton > button {
    background: rgba(212,175,55,0.08) !important;
    color: #d4af37 !important;
    border: 1px solid rgba(212,175,55,0.35) !important;
    border-radius: 30px !important;
    padding: 10px 20px !important;
    font-family: 'Tajawal', sans-serif !important;
    font-size: 14px !important;
    letter-spacing: 1px !important;
    box-shadow: none !important;
    transition: all 0.3s !important;
}
div[data-testid="column"] .stButton > button:hover {
    background: linear-gradient(135deg,#8b6914,#d4af37) !important;
    color: #000 !important;
    transform: scale(1.03) !important;
    box-shadow: 0 0 20px rgba(212,175,55,0.4) !important;
}

/* ── MAIN BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg,#6b4f00,#d4af37,#ffd700,#d4af37) !important;
    color: #0a0600 !important; border: none !important;
    border-radius: 40px !important; padding: 13px 44px !important;
    font-family: 'Playfair Display', serif !important; font-weight: 700 !important;
    font-size: 15px !important; letter-spacing: 2px !important;
    box-shadow: 0 0 25px rgba(212,175,55,0.35) !important;
    transition: all 0.3s ease !important;
}
.stButton > button:hover { transform: scale(1.06) !important; box-shadow: 0 0 45px rgba(212,175,55,0.65) !important; }

[data-testid="stFileUploader"] {
    background: rgba(212,175,55,0.04) !important;
    border: 1.5px dashed rgba(212,175,55,0.4) !important;
    border-radius: 12px !important; padding: 8px !important;
}
[data-testid="stFileUploader"] label { color: #d4af37 !important; }
[data-testid="stFileUploadDropzone"] { background: transparent !important; border: none !important; }
[data-testid="stFileUploadDropzone"] p { color: #a0896a !important; }
[data-testid="stFileUploadDropzone"] svg { fill: #d4af37 !important; color: #d4af37 !important; }

[data-testid="stSidebar"] {
    background: rgba(4,8,15,0.97) !important;
    border-right: 1px solid rgba(212,175,55,0.15) !important;
}

label, .stRadio label, .stSelectbox label { color: #d4af37 !important; }

.stChatInput textarea {
    background: rgba(10,16,40,0.9) !important;
    border: 1px solid rgba(212,175,55,0.3) !important;
    color: #fde68a !important; border-radius: 12px !important;
}

.divider { height:1px; background:linear-gradient(90deg,transparent,#d4af37,transparent); margin:16px 0; position:relative; z-index:10; }

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; max-width: 900px; }
section[data-testid="stMain"] > div { position: relative; z-index: 10; }
</style>

<div class="space-bg"></div>
<div class="stars-layer"></div>
<div class="stars-layer-2"></div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
groq_client   = Groq(api_key=st.secrets["GROQ_API_KEY"])
gemini_client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
GROQ_MODEL    = "llama-3.3-70b-versatile"
GEMINI_MODEL  = "gemini-1.5-flash-8b"

SYS = {
"العربية": """أنت Ornis IA — ذكاء اصطناعي أورنيثولوجي أكاديمي متخصص.
قواعد صارمة:
1. أجب باللغة العربية الفصحى دائماً
2. اذكر الاسم العلمي اللاتيني لكل طائر
3. نظّم كل إجابة بهذا الهيكل الإلزامي:

━━━━━━━━━━━━━━━━━━━━━━━━
🦅 [الاسم العربي] | [Scientific Name]
━━━━━━━━━━━━━━━━━━━━━━━━
📌 التصنيف العلمي: الرتبة ← العائلة ← الجنس ← النوع
🌍 الانتشار الجغرافي: ...
🏔️ البيئة والموطن: ...
🎨 الوصف المورفولوجي: ...
🔊 الصوت والتواصل: ...
🍃 الغذاء والسلوك: ...
🥚 التكاثر: ...
⚠️ الحالة الحفاظية (IUCN): ...
━━━━━━━━━━━━━━━━━━━━━━━━
📚 المصادر:
  • Cornell Lab of Ornithology — allaboutbirds.org
  • eBird — ebird.org
  • BirdLife International — birdlife.org

4. مصادر مسموحة فقط: Cornell Lab، eBird، BirdLife International، HBW Alive، Xeno-canto، IUCN Red List، Journal of Ornithology
5. ❌ محظور تماماً: Wikipedia، مواقع عامة، مدونات
6. إذا لم تعرف مصدراً دقيقاً، صرّح بذلك""",

"English": """You are Ornis IA — an academic-level ornithological AI.
Rules:
1. Always answer in English
2. Always include Latin scientific name
3. Mandatory structure:

━━━━━━━━━━━━━━━━━━━━━━━━
🦅 [Common Name] | [Scientific Name]
━━━━━━━━━━━━━━━━━━━━━━━━
📌 Taxonomy: Order → Family → Genus → Species
🌍 Geographic Range: ...
🏔️ Habitat & Ecology: ...
🎨 Morphological Description: ...
🔊 Vocalizations: ...
🍃 Diet & Behavior: ...
🥚 Reproduction: ...
⚠️ IUCN Conservation Status: ...
━━━━━━━━━━━━━━━━━━━━━━━━
📚 Sources:
  • Cornell Lab — allaboutbirds.org
  • eBird — ebird.org
  • BirdLife International — birdlife.org

4. Permitted: Cornell Lab, eBird, BirdLife, HBW, Xeno-canto, IUCN, peer-reviewed journals
5. ❌ NEVER: Wikipedia, general websites, blogs""",

"Français": """Vous êtes Ornis IA — expert IA en ornithologie académique.
Règles:
1. Répondez toujours en français
2. Toujours le nom scientifique latin
3. Structure obligatoire:

━━━━━━━━━━━━━━━━━━━━━━━━
🦅 [Nom commun] | [Nom scientifique]
━━━━━━━━━━━━━━━━━━━━━━━━
📌 Taxonomie: Ordre → Famille → Genre → Espèce
🌍 Répartition: ...
🏔️ Habitat & Écologie: ...
🎨 Description morphologique: ...
🔊 Vocalisations: ...
🍃 Alimentation & Comportement: ...
🥚 Reproduction: ...
⚠️ Statut UICN: ...
━━━━━━━━━━━━━━━━━━━━━━━━
📚 Sources:
  • Cornell Lab — allaboutbirds.org
  • eBird — ebird.org
  • BirdLife International — birdlife.org

4. Autorisé: Cornell Lab, eBird, BirdLife, HBW, Xeno-canto, UICN
5. ❌ JAMAIS: Wikipedia, sites généraux, blogs"""
}

IMG_PROMPT = {
"العربية": """حلّل هذه الصورة وحدّد الطائر بدقة علمية تامة:
━━━━━━━━━━━━━━━━━━━━━━━━
🔍 نتيجة التعرف
━━━━━━━━━━━━━━━━━━━━━━━━
🦅 الاسم العربي: | الاسم العلمي:
📌 التصنيف: الرتبة ← العائلة ← الجنس
🎨 المميزات التشخيصية المرئية في الصورة:
🌍 الموطن الطبيعي:
⚠️ حالة الحفاظ (IUCN):
📚 المصدر: Cornell Lab / eBird / BirdLife International
━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ مستوى الثقة: [عالٍ/متوسط/منخفض] + السبب""",
"English": """Analyze this image and identify the bird scientifically:
━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Identification Result
━━━━━━━━━━━━━━━━━━━━━━━━
🦅 Common Name: | Scientific Name:
📌 Taxonomy: Order → Family → Genus
🎨 Diagnostic features visible:
🌍 Natural habitat:
⚠️ IUCN Conservation status:
📚 Source: Cornell Lab / eBird / BirdLife International
━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Confidence: [High/Medium/Low] + reason""",
"Français": """Analysez cette image et identifiez l'oiseau:
━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Résultat d'identification
━━━━━━━━━━━━━━━━━━━━━━━━
🦅 Nom commun: | Nom scientifique:
📌 Taxonomie: Ordre → Famille → Genre
🎨 Caractéristiques diagnostiques:
🌍 Habitat naturel:
⚠️ Statut UICN:
📚 Source: Cornell Lab / eBird / BirdLife International
━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Niveau de confiance: [Élevé/Moyen/Faible] + raison"""
}

# ══════════════════════════════════════════════════════════════
def chat_groq(msg, lang, history):
    msgs = [{"role":"system","content":SYS[lang]}]
    for h in history[-8:]:
        msgs.append({"role":"assistant" if h["role"]=="model" else "user","content":h["content"]})
    msgs.append({"role":"user","content":msg})
    r = groq_client.chat.completions.create(model=GROQ_MODEL, messages=msgs, max_tokens=2000, temperature=0.2)
    return r.choices[0].message.content

def analyze_image(img_file, lang):
    img_bytes = img_file.read()
    ext = img_file.name.split(".")[-1].lower()
    mime = "image/png" if ext == "png" else "image/jpeg"
    r = gemini_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[types.Part.from_bytes(data=img_bytes, mime_type=mime), IMG_PROMPT[lang]]
    )
    return r.text

def analyze_audio(audio_file, lang):
    try:
        from birdnetlib import Recording
        from birdnetlib.analyzer import Analyzer
        analyzer = Analyzer()
        suffix = "." + audio_file.name.split(".")[-1]
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(audio_file.read())
            tmp_path = tmp.name
        rec = Recording(analyzer, tmp_path, lat=36.7, lon=3.0,
                        date_frmt="%Y-%m-%d", date="2024-06-01", min_conf=0.20)
        rec.analyze()
        os.unlink(tmp_path)
        if rec.detections:
            birds = "\n".join([
                f"• {d['common_name']} ({d['scientific_name']}) — confidence: {d['confidence']:.0%}"
                for d in rec.detections[:5]
            ])
            prompt = f"BirdNET audio analysis detected:\n{birds}\n\nProvide full academic profile for the top species with scientific sources."
        else:
            prompt = "BirdNET found no clear bird detection. Advise the user on how to make a better recording."
        return chat_groq(prompt, lang, [])
    except Exception as e:
        return f"⚠️ Audio analysis error: {str(e)}"

# ══════════════════════════════════════════════════════════════
if "page"     not in st.session_state: st.session_state.page = "landing"
if "messages" not in st.session_state: st.session_state.messages = []
if "lang"     not in st.session_state: st.session_state.lang = "العربية"
if "mode"     not in st.session_state: st.session_state.mode = "chat"

# ══════════════════════════════════════════════════════════════
#  LANDING PAGE
# ══════════════════════════════════════════════════════════════
if st.session_state.page == "landing":
    st.markdown("""
    <div class="landing-wrap">
        <div class="bird-icon">🦅</div>
        <div class="brand-title">ORNIS</div>
        <div class="brand-ia">INTELLIGENCE ARTIFICIELLE ORNITHOLOGIQUE</div>
        <div class="gold-line"></div>
        <div class="tagline">
            منصة ذكاء اصطناعي أكاديمية متخصصة في علم الطيور<br>
            تحليل الصور · تحليل الأصوات · معرفة علمية موثّقة<br>
            <span style="font-size:13px;opacity:0.5;font-family:'Cormorant Garamond',serif;letter-spacing:2px">
                Powered by Cornell Lab · eBird · BirdLife International
            </span>
        </div>
        <div class="features-row">
            <div class="feat-pill">🖼️ تحليل الصور</div>
            <div class="feat-pill">🎵 تحليل الأصوات</div>
            <div class="feat-pill">📚 مصادر أكاديمية</div>
            <div class="feat-pill">🌍 متعدد اللغات</div>
            <div class="feat-pill">🔬 دقة علمية</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        lang = st.selectbox("", ["العربية", "English", "Français"], label_visibility="collapsed")
        st.session_state.lang = lang
        if st.button("✦  Enter Ornis IA  ✦", use_container_width=True):
            st.session_state.page = "chat"
            st.rerun()

# ══════════════════════════════════════════════════════════════
#  CHAT PAGE
# ══════════════════════════════════════════════════════════════
else:
    with st.sidebar:
        st.markdown('<p style="font-family:Playfair Display,serif;font-size:22px;color:#d4af37;letter-spacing:4px;text-align:center">ORNIS IA</p>', unsafe_allow_html=True)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        lang = st.selectbox("🌍 Language", ["العربية", "English", "Français"],
                            index=["العربية", "English", "Français"].index(st.session_state.lang))
        st.session_state.lang = lang
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("""<p style="color:#d4af37;font-size:12px;letter-spacing:1px;margin-bottom:8px">📚 SCIENTIFIC SOURCES</p>
<p style="color:#888;font-size:11px;line-height:2.2">
🔬 Cornell Lab of Ornithology<br>
🐦 eBird Global Database<br>
🌍 BirdLife International<br>
📖 HBW Alive<br>
🎵 Xeno-canto<br>
🔴 IUCN Red List<br>
📄 Journal of Ornithology
</p>""", unsafe_allow_html=True)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()
        if st.button("🏠 Home"):
            st.session_state.page = "landing"
            st.session_state.messages = []
            st.rerun()

    # Header
    st.markdown("""
    <div class="chat-top">
        <div class="chat-logo">🦅 ORNIS IA</div>
        <div class="chat-sub">Ornithological Artificial Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    # ── MODE SELECTOR — 3 real Streamlit buttons in columns
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("💬  Chat", use_container_width=True, key="btn_chat"):
            st.session_state.mode = "chat"
            st.rerun()
    with c2:
        if st.button("🖼️  Image Analysis", use_container_width=True, key="btn_img"):
            st.session_state.mode = "image"
            st.rerun()
    with c3:
        if st.button("🎵  Audio Analysis", use_container_width=True, key="btn_aud"):
            st.session_state.mode = "audio"
            st.rerun()

    mode_labels = {
        "chat":  "💬 Chat Mode — Ask anything about birds",
        "image": "🖼️ Image Analysis Mode — Upload a bird photo",
        "audio": "🎵 Audio Analysis Mode — Upload a bird recording"
    }
    st.markdown(
        f'<p style="text-align:center;color:rgba(212,175,55,0.6);font-size:12px;'
        f'letter-spacing:2px;margin:6px 0 14px">{mode_labels[st.session_state.mode]}</p>',
        unsafe_allow_html=True
    )
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Messages
    for m in st.session_state.messages:
        if m["role"] == "user":
            st.markdown(f'<div class="bubble-user">👤 {m["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="bubble-bot">🦅 {m["content"]}'
                f'<br><span class="src-badge">📚 Cornell Lab · eBird · BirdLife Int. · IUCN</span></div>',
                unsafe_allow_html=True
            )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── IMAGE MODE
    if st.session_state.mode == "image":
        st.markdown('<div class="upload-card"><div class="upload-card-title">🖼️ &nbsp; Bird Image Analysis</div>', unsafe_allow_html=True)
        img = st.file_uploader(
            "Drop a bird photo here — JPG, PNG, WEBP supported",
            type=["jpg", "jpeg", "png", "webp"],
            key="img_uploader"
        )
        if img:
            col_img, col_gap = st.columns([1, 2])
            with col_img:
                st.image(img, caption="📸 Uploaded photo", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if img:
            if st.button("🔍  Identify Species from Image", use_container_width=True):
                with st.spinner("🔭 Analyzing with Gemini Vision AI..."):
                    res = analyze_image(img, st.session_state.lang)
                    st.session_state.messages.append({"role": "user", "content": "📸 [Bird image uploaded for identification]"})
                    st.session_state.messages.append({"role": "model", "content": res})
                    st.rerun()

    # ── AUDIO MODE
    elif st.session_state.mode == "audio":
        st.markdown('<div class="upload-card"><div class="upload-card-title">🎵 &nbsp; Bird Audio Analysis</div>', unsafe_allow_html=True)
        aud = st.file_uploader(
            "Drop a bird audio recording here — WAV, MP3, OGG, M4A supported",
            type=["wav", "mp3", "ogg", "m4a", "flac"],
            key="aud_uploader"
        )
        if aud:
            st.audio(aud)
        st.markdown('</div>', unsafe_allow_html=True)
        if aud:
            if st.button("🎧  Identify Species from Audio (BirdNET)", use_container_width=True):
                with st.spinner("🔊 Running BirdNET neural network analysis..."):
                    res = analyze_audio(aud, st.session_state.lang)
                    st.session_state.messages.append({"role": "user", "content": "🎵 [Bird audio recording uploaded]"})
                    st.session_state.messages.append({"role": "model", "content": res})
                    st.rerun()

    # ── CHAT MODE
    else:
        ph = {
            "العربية": "💬 اكتب سؤالك الأكاديمي عن الطيور...",
            "English": "💬 Ask your ornithological question...",
            "Français": "💬 Posez votre question ornithologique..."
        }
        user_input = st.chat_input(ph[st.session_state.lang])
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.spinner("🤔 Consulting ornithological databases..."):
                reply = chat_groq(user_input, st.session_state.lang, st.session_state.messages[:-1])
            st.session_state.messages.append({"role": "model", "content": reply})
            st.rerun()