import streamlit as st
from groq import Groq
import base64, tempfile, os, uuid
from datetime import datetime
import streamlit.components.v1 as components
from history import load_all, save_session, delete_session, get_session

st.set_page_config(
    page_title="Ornis IA",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════
#  CSS — Claude-like sidebar + space theme
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Cormorant+Garamond:wght@300;400;600&family=Tajawal:wght@300;400;700&display=swap');

html, body, .stApp { background: #04080f !important; }

/* SPACE */
.stApp::before {
    content: ''; position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background:
        radial-gradient(ellipse at 20% 50%, rgba(40,10,80,.5) 0%, transparent 55%),
        radial-gradient(ellipse at 80% 20%, rgba(10,30,80,.4) 0%, transparent 55%);
}

/* ══ SIDEBAR ══ */
section[data-testid="stSidebar"] {
    background: #060c1c !important;
    border-right: 1px solid rgba(212,175,55,.13) !important;
    width: 280px !important;
}
section[data-testid="stSidebar"] > div { padding: 0 !important; }

.sb-logo {
    font-family: 'Playfair Display', serif; font-size: 20px; font-weight: 900;
    letter-spacing: 5px; display: block; padding: 20px 16px 2px;
    background: linear-gradient(135deg, #ffd700, #d4af37, #8b6914);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.sb-tagline {
    font-size: 9px; color: rgba(212,175,55,.35); letter-spacing: 3px;
    font-family: 'Cormorant Garamond', serif; display: block; padding: 0 16px 14px;
}
.sb-div { height: 1px; background: rgba(212,175,55,.1); margin: 6px 0; }
.sb-section {
    font-size: 10px; color: rgba(212,175,55,.38); letter-spacing: 2px;
    text-transform: uppercase; padding: 8px 16px 4px;
}
.ch-item {
    padding: 9px 14px; margin: 2px 8px; border-radius: 8px;
    color: #9a8060; font-size: 12px; font-family: 'Tajawal', sans-serif;
    border: 1px solid transparent; transition: all .18s;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis; cursor: pointer;
}
.ch-item:hover { background: rgba(212,175,55,.07); color: #d4af37; border-color: rgba(212,175,55,.15); }
.ch-item.active { background: rgba(212,175,55,.12); color: #ffd700; border-color: rgba(212,175,55,.28); }
.ch-date { font-size: 9px; color: rgba(212,175,55,.22); padding: 0 14px; margin-bottom: 4px; }

/* ══ LANDING ══ */
.land {
    position: relative; z-index: 10; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    min-height: 88vh; padding: 50px 24px; text-align: center;
}
.bird-em {
    font-size: 80px; line-height: 1; margin-bottom: 20px;
    animation: fl 5s ease-in-out infinite, gl 3s ease-in-out infinite alternate;
}
@keyframes fl { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-15px)} }
@keyframes gl {
    0%   { filter: drop-shadow(0 0 14px rgba(212,175,55,.5)); }
    100% { filter: drop-shadow(0 0 40px rgba(255,215,0,.9)); }
}
.brand {
    font-family: 'Playfair Display', serif;
    font-size: clamp(50px, 9vw, 96px); font-weight: 900; letter-spacing: 12px;
    background: linear-gradient(180deg,#fffbe6 0%,#ffd700 15%,#d4af37 35%,#8b6914 50%,#d4af37 65%,#ffd700 80%,#c8960c 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    filter: drop-shadow(0 2px 26px rgba(212,175,55,.5));
    animation: bin 1.8s cubic-bezier(.23,1.01,.32,1) both;
}
@keyframes bin {
    0%  { opacity:0; transform:scale(.65) translateY(38px); }
    70% { opacity:1; transform:scale(1.04) translateY(-4px); }
    100%{ opacity:1; transform:scale(1) translateY(0); }
}
.brand-sub {
    font-family: 'Cormorant Garamond', serif; letter-spacing: 10px;
    font-size: clamp(10px,1.4vw,13px); color: rgba(212,175,55,.58); margin-top: 3px;
    animation: fi 1s ease-out 1.5s both;
}
.gold-hr {
    width: 240px; height: 1px;
    background: linear-gradient(90deg, transparent, #d4af37, transparent);
    margin: 18px auto; animation: fi 1s ease-out 2s both;
}
.tagline {
    color: rgba(255,255,255,.6); font-size: clamp(13px,1.7vw,16px);
    line-height: 1.85; max-width: 520px; animation: fi 1s ease-out 2.2s both;
}
@keyframes fi { 0%{opacity:0;transform:translateY(14px)} 100%{opacity:1;transform:translateY(0)} }
.pills {
    display: flex; gap: 9px; flex-wrap: wrap; justify-content: center;
    margin: 22px 0; animation: fi 1s ease-out 2.5s both;
}
.pl {
    background: rgba(212,175,55,.07); border: 1px solid rgba(212,175,55,.28);
    border-radius: 40px; padding: 7px 18px; color: #d4af37; font-size: 12px;
}

/* ══ CHAT HEADER ══ */
.chdr {
    text-align: center; padding: 16px 0 5px;
    border-bottom: 1px solid rgba(212,175,55,.1); margin-bottom: 10px;
    position: relative; z-index: 10;
}
.clogo {
    font-family: 'Playfair Display', serif;
    font-size: clamp(20px,3.5vw,36px); font-weight: 900; letter-spacing: 7px;
    background: linear-gradient(180deg, #ffd700, #d4af37, #8b6914);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.csub {
    font-family: 'Cormorant Garamond', serif; color: rgba(212,175,55,.38);
    letter-spacing: 4px; font-size: 9px; text-transform: uppercase;
}

/* ══ BUBBLES ══ */
.bu {
    background: linear-gradient(135deg, rgba(212,175,55,.12), rgba(212,175,55,.05));
    border: 1px solid rgba(212,175,55,.26); border-radius: 16px 16px 4px 16px;
    padding: 13px 17px; margin: 7px 0; color: #fde68a;
    font-family: 'Tajawal', sans-serif; font-size: 15px;
    position: relative; z-index: 10;
}
.bb {
    background: rgba(5,10,26,.93); border: 1px solid rgba(212,175,55,.12);
    border-radius: 16px 16px 16px 4px; padding: 17px 20px; margin: 7px 0;
    color: #e3e0d8; font-family: 'Tajawal', sans-serif; font-size: 15px;
    line-height: 1.9; position: relative; z-index: 10; backdrop-filter: blur(8px);
}
.src-footer {
    margin-top: 10px; padding-top: 8px;
    border-top: 1px solid rgba(212,175,55,.12);
    font-size: 11px; color: rgba(212,175,55,.55);
}

/* ══ CARD ══ */
.card {
    position: relative; z-index: 10; background: rgba(5,10,26,.88);
    border: 1px solid rgba(212,175,55,.16); border-radius: 12px;
    padding: 18px; margin-bottom: 12px; backdrop-filter: blur(7px);
}
.ctitle {
    font-family: 'Playfair Display', serif; color: #d4af37;
    font-size: 16px; letter-spacing: 2px; margin-bottom: 10px;
}
.divider { height:1px; background:linear-gradient(90deg,transparent,rgba(212,175,55,.22),transparent); margin:10px 0; position:relative; z-index:10; }

/* ══ STREAMLIT ══ */
.stButton > button {
    background: linear-gradient(135deg,#4a3500,#c49b20,#ffd700) !important;
    color: #050200 !important; border: none !important; border-radius: 28px !important;
    padding: 10px 32px !important; font-family: 'Playfair Display',serif !important;
    font-weight: 700 !important; font-size: 13px !important; letter-spacing: 1.5px !important;
    box-shadow: 0 0 16px rgba(212,175,55,.2) !important; transition: all .3s !important;
}
.stButton > button:hover { transform:scale(1.04) !important; box-shadow: 0 0 28px rgba(212,175,55,.45) !important; }

[data-testid="stFileUploader"] {
    background: rgba(212,175,55,.03) !important;
    border: 1.5px dashed rgba(212,175,55,.3) !important; border-radius: 10px !important;
}
[data-testid="stFileUploader"] label { color: #d4af37 !important; }
[data-testid="stFileUploadDropzone"] { background: transparent !important; border: none !important; }
[data-testid="stFileUploadDropzone"] p { color: #7a6040 !important; }
[data-testid="stFileUploadDropzone"] svg { fill: #d4af37 !important; }

div[data-testid="stAudioInput"] {
    background: rgba(212,175,55,.03) !important;
    border: 1.5px dashed rgba(212,175,55,.38) !important; border-radius: 10px !important;
}
.stChatInput textarea {
    background: rgba(5,10,28,.96) !important; border: 1px solid rgba(212,175,55,.24) !important;
    color: #fde68a !important; border-radius: 12px !important;
}
.stTextInput input {
    background: rgba(5,10,28,.9) !important; border: 1px solid rgba(212,175,55,.22) !important;
    color: #fde68a !important; border-radius: 7px !important;
}
label, .stRadio label, .stSelectbox label { color: #d4af37 !important; }
.stExpander {
    border: 1px solid rgba(212,175,55,.18) !important;
    border-radius: 10px !important; background: rgba(5,10,26,.7) !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 820px; }
section[data-testid="stMain"] > div { position: relative; z-index: 10; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  CLIENT
# ═══════════════════════════════════════════════════════════════
client       = Groq(api_key=st.secrets["GROQ_API_KEY"])
CHAT_MODEL   = "llama-3.3-70b-versatile"
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

# ═══════════════════════════════════════════════════════════════
#  SYSTEM PROMPTS — inline citations + summary at end
# ═══════════════════════════════════════════════════════════════
SYS = {

"العربية": """أنت البروفيسور Ornis — عالم أورنيثولوجيا دكتوراه من Cornell University، مساهم في HBW وBirdLife International، خبرة ميدانية 30+ عاماً.

قاعدة الاستشهاد الأهم:
➤ بعد كل جملة أو معلومة، اكتب فوراً المصدر بين قوسين مائلين هكذا: *(Cornell Lab, 2024)* أو *(Gill, 2020, p.142)* أو *(Ibis, 114:203)* إلخ.
➤ في نهاية الإجابة: قسم "📚 المراجع الكاملة" يُدرج فيه كل المصادر المذكورة مرتبة.

هيكل الإجابة عن نوع طائر (إلزامي):
━━━━━━━━━━━━━━━━━━━━━━━━
🦅 **[الاسم العربي]** | *[Genus species]*
━━━━━━━━━━━━━━━━━━━━━━━━
**📌 التصنيف الفيلوجيني:**
[المعلومة] *(المصدر)*

**🌍 الانتشار الجغرافي والهجرة:**
[المعلومة] *(المصدر)* [معلومة أخرى] *(مصدر آخر)*

**🏔️ البيئة الإيكولوجية:**
[المعلومة] *(المصدر)*

**🎨 الوصف المورفولوجي والتشخيصي:**
[المعلومة] *(المصدر)*

**🔊 الصوت والتواصل:**
[المعلومة] *(Xeno-canto أو Macaulay Library أو المصدر)*

**🍃 الغذاء والسلوك:**
[المعلومة] *(المصدر)*

**🥚 التكاثر وعلم الأعشاش:**
[المعلومة] *(المصدر)*

**🔬 ملاحظات علمية متخصصة:**
[المعلومة] *(المصدر)*

**⚠️ الحالة الحفاظية:**
[المعلومة] *(IUCN Red List, 2024)*
━━━━━━━━━━━━━━━━━━━━━━━━
**📚 المراجع الكاملة:**
• [كل المصادر المذكورة في الإجابة مرتبة أبجدياً بصيغة APA]

قائمة المصادر المعتمدة للاستشهاد:
Cornell Lab of Ornithology | eBird | BirdLife International | Avibase (Lepage, D.) |
Macaulay Library | Birds of the World (Cornell/BirdLife) | IUCN Red List |
Xeno-canto | Biodiversity Heritage Library | SORA |
The Auk / Ornithology (AOS) | Ibis (BOU) | Journal of Ornithology (DO-G) |
The Condor | Emu – Austral Ornithology | Current Ornithology (D.M. Power, ed.) |
PubMed/NCBI | HBW Alive | Ornithology — Frank Gill (4th ed., 2020) |
ResearchGate | Google Scholar

❌ محظور: Wikipedia، مواقع عامة، مدونات
⚠️ للأسئلة العامة: استخدم نفس نظام الاستشهاد المباشر بعد كل معلومة.""",

"English": """You are Professor Ornis — ornithologist PhD Cornell University, HBW & BirdLife contributor, 30+ years field research.

CRITICAL citation rule:
➤ After EVERY sentence or fact, immediately write the source in parentheses: *(Cornell Lab, 2024)* or *(Gill, 2020, p.142)* or *(The Auk, 138:45)* etc.
➤ At the END of the answer: a "📚 Full References" section listing all cited sources in APA format.

Mandatory structure for species questions:
━━━━━━━━━━━━━━━━━━━━━━━━
🦅 **[Common Name]** | *[Genus species]*
━━━━━━━━━━━━━━━━━━━━━━━━
**📌 Phylogenetic Classification:**
[fact] *(source)* [fact] *(source)*

**🌍 Geographic Distribution & Migration:**
[fact] *(source)*

**🏔️ Ecological Habitat:**
[fact] *(source)*

**🎨 Morphological & Diagnostic Description:**
[fact] *(source)*

**🔊 Vocalizations:**
[fact] *(Xeno-canto or Macaulay Library or source)*

**🍃 Diet & Foraging Behavior:**
[fact] *(source)*

**🥚 Breeding Biology:**
[fact] *(source)*

**🔬 Specialist Scientific Notes:**
[fact] *(source)*

**⚠️ Conservation Status:**
[fact] *(IUCN Red List, 2024)*
━━━━━━━━━━━━━━━━━━━━━━━━
**📚 Full References:**
• [All cited sources alphabetically in APA format]

Approved sources:
Cornell Lab | eBird | BirdLife International | Avibase (Lepage, D.) |
Macaulay Library | Birds of the World | IUCN Red List | Xeno-canto |
Biodiversity Heritage Library | SORA | The Auk/Ornithology (AOS) |
Ibis (BOU) | Journal of Ornithology | The Condor | Emu – Austral Ornithology |
Current Ornithology (D.M. Power) | PubMed/NCBI | HBW Alive |
Ornithology — Frank Gill (4th ed., 2020) | ResearchGate | Google Scholar

❌ NEVER: Wikipedia, general websites, blogs
⚠️ For general questions: use the same inline citation system after every fact.""",

"Français": """Vous êtes le Professeur Ornis — ornithologue PhD Cornell, contributeur HBW & BirdLife, 30+ ans de terrain.

RÈGLE DE CITATION CRITIQUE:
➤ Après CHAQUE phrase ou fait, écrivez immédiatement la source entre parenthèses: *(Cornell Lab, 2024)* ou *(Gill, 2020, p.142)* ou *(Ibis, 114:203)* etc.
➤ En FIN de réponse: section "📚 Références complètes" listant toutes les sources citées en format APA.

Structure obligatoire pour une espèce:
━━━━━━━━━━━━━━━━━━━━━━━━
🦅 **[Nom commun]** | *[Genre espèce]*
━━━━━━━━━━━━━━━━━━━━━━━━
**📌 Classification phylogénétique:** [fait] *(source)*
**🌍 Répartition & Migration:** [fait] *(source)*
**🏔️ Habitat écologique:** [fait] *(source)*
**🎨 Description morphologique:** [fait] *(source)*
**🔊 Vocalisations:** [fait] *(Xeno-canto ou source)*
**🍃 Alimentation & Comportement:** [fait] *(source)*
**🥚 Reproduction:** [fait] *(source)*
**🔬 Notes spécialisées:** [fait] *(source)*
**⚠️ Statut UICN:** [fait] *(UICN, 2024)*
━━━━━━━━━━━━━━━━━━━━━━━━
**📚 Références complètes:** [toutes les sources citées en APA]

Sources approuvées:
Cornell Lab | eBird | BirdLife International | Avibase (Lepage, D.) |
Macaulay Library | Birds of the World | UICN | Xeno-canto |
Biodiversity Heritage Library | SORA | The Auk/Ornithology | Ibis (BOU) |
Journal of Ornithology | The Condor | Emu | Current Ornithology (D.M. Power) |
PubMed/NCBI | HBW Alive | Ornithology — Frank Gill (4e éd., 2020) |
ResearchGate | Google Scholar

❌ JAMAIS: Wikipedia, sites généraux, blogs"""
}

# ═══════════════════════════════════════════════════════════════
#  IMAGE PROMPTS — defined here to avoid NameError
# ═══════════════════════════════════════════════════════════════
IMG_P = {

"العربية": """أنت البروفيسور Ornis. حلّل هذه الصورة بعين عالم متخصص.
قاعدة أساسية: بعد كل معلومة اكتب مصدرها فوراً بين قوسين مائلين.

━━━━━━━━━━━━━━━━━━━━━━━━
🔍 **التشخيص الميداني المتخصص**
━━━━━━━━━━━━━━━━━━━━━━━━
🦅 **الاسم العربي:** | ***Genus species:*** *(Cornell Lab / Birds of the World)*
📌 **التصنيف:** الرتبة | العائلة | الجنس *(Avibase, Lepage D.)*

🎨 **السمات التشخيصية في هذه الصورة تحديداً:**
[صف كل سمة مرئية مع مصدرها] *(HBW Alive أو Gill, 2020)*

🔍 **التمييز عن الأنواع المشابهة:**
[لماذا هذا النوع وليس غيره؟] *(The Auk / Ibis / Journal of Ornithology)*

🌍 **الموطن الطبيعي:** *(eBird / BirdLife International)*
⚠️ **حالة الحفاظ:** *(IUCN Red List, 2024)*
━━━━━━━━━━━━━━━━━━━━━━━━
**📚 المراجع:** [قائمة المصادر المستخدمة]
⚠️ **ثقة التشخيص:** [عالية جداً/عالية/متوسطة/منخفضة] — **السبب:**""",

"English": """You are Professor Ornis. Analyze this bird image with specialist eyes.
CRITICAL: After every fact, write its source immediately in parentheses.

━━━━━━━━━━━━━━━━━━━━━━━━
🔍 **Specialist Field Identification**
━━━━━━━━━━━━━━━━━━━━━━━━
🦅 **Common Name:** | ***Genus species:*** *(Cornell Lab / Birds of the World)*
📌 **Taxonomy:** Order | Family | Genus *(Avibase, Lepage D.)*

🎨 **Diagnostic features visible in THIS image:**
[describe each feature with its source] *(HBW Alive or Gill, 2020)*

🔍 **Separation from similar species:**
[why this species specifically?] *(The Auk / Ibis / Journal of Ornithology)*

🌍 **Habitat:** *(eBird / BirdLife International)*
⚠️ **IUCN Status:** *(IUCN Red List, 2024)*
━━━━━━━━━━━━━━━━━━━━━━━━
**📚 References:** [list of all sources used]
⚠️ **ID Confidence:** [Very High/High/Medium/Low] — **Rationale:**""",

"Français": """Vous êtes le Professeur Ornis. Analysez cette image en spécialiste.
RÈGLE: Après chaque fait, écrivez sa source immédiatement entre parenthèses.

━━━━━━━━━━━━━━━━━━━━━━━━
🔍 **Identification de terrain spécialisée**
━━━━━━━━━━━━━━━━━━━━━━━━
🦅 **Nom commun:** | ***Genre espèce:*** *(Cornell Lab / Birds of the World)*
📌 **Taxonomie:** Ordre | Famille | Genre *(Avibase, Lepage D.)*

🎨 **Caractéristiques diagnostiques dans CETTE image:**
[chaque caractéristique + sa source] *(HBW Alive ou Gill, 2020)*

🔍 **Séparation des espèces similaires:** *(The Auk / Ibis / Journal of Ornithology)*
🌍 **Habitat:** *(eBird / BirdLife International)*
⚠️ **Statut UICN:** *(UICN, 2024)*
━━━━━━━━━━━━━━━━━━━━━━━━
**📚 Références:** [liste de toutes les sources utilisées]
⚠️ **Confiance:** [Très élevée/Élevée/Moyenne/Faible] — **Justification:**"""
}

# ═══════════════════════════════════════════════════════════════
#  CORE FUNCTIONS
# ═══════════════════════════════════════════════════════════════
def chat_groq(msg, lang, history):
    msgs = [{"role": "system", "content": SYS[lang]}]
    for h in history[-10:]:
        msgs.append({
            "role": "assistant" if h["role"] == "model" else "user",
            "content": h["content"]
        })
    msgs.append({"role": "user", "content": msg})
    r = client.chat.completions.create(
        model=CHAT_MODEL, messages=msgs, max_tokens=2500, temperature=0.15
    )
    return r.choices[0].message.content

def analyze_image(img_file, lang):
    try:
        img_bytes = img_file.read()
        b64 = base64.b64encode(img_bytes).decode()
        mime = "image/png" if img_file.name.lower().endswith("png") else "image/jpeg"
        r = client.chat.completions.create(
            model=VISION_MODEL,
            messages=[{"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
                {"type": "text", "text": IMG_P[lang]}
            ]}],
            max_tokens=1800, temperature=0.1
        )
        return r.choices[0].message.content
    except Exception as e:
        return f"⚠️ Image analysis error: {e}"

def transcribe(audio_bytes):
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name
        with open(tmp_path, "rb") as f:
            result = client.audio.transcriptions.create(
                model="whisper-large-v3", file=("audio.wav", f)
            )
        os.unlink(tmp_path)
        return result.text
    except Exception as e:
        return ""

def speak(text, lang):
    vl = {"العربية": "ar", "English": "en-US", "Français": "fr-FR"}.get(lang, "en-US")
    clean = text.replace('"', ' ').replace("'", " ").replace("\n", " ")[:600]
    components.html(f"""<script>
const u = new SpeechSynthesisUtterance("{clean}");
u.lang = "{vl}"; u.rate = 0.9;
window.speechSynthesis.cancel();
window.speechSynthesis.speak(u);
</script>""", height=0)

# ═══════════════════════════════════════════════════════════════
#  SESSION HELPERS
# ═══════════════════════════════════════════════════════════════
def commit():
    if st.session_state.messages:
        title = next(
            (m["content"][:55] for m in st.session_state.messages if m["role"] == "user"),
            "Chat"
        )
        save_session(st.session_state.sid, title, st.session_state.messages)

def new_chat():
    commit()
    st.session_state.messages = []
    st.session_state.sid = str(uuid.uuid4())[:8]
    st.session_state.show_img = False

# ═══════════════════════════════════════════════════════════════
#  STATE INIT
# ═══════════════════════════════════════════════════════════════
DEFAULTS = {
    "page": "landing", "messages": [], "lang": "العربية",
    "sid": str(uuid.uuid4())[:8], "show_img": False,
    "speak_it": False, "search_q": ""
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ═══════════════════════════════════════════════════════════════
#  LANDING PAGE
# ═══════════════════════════════════════════════════════════════
if st.session_state.page == "landing":
    st.markdown("""
    <div class="land">
      <div class="bird-em">🦅</div>
      <div class="brand">ORNIS</div>
      <div class="brand-sub">INTELLIGENCE ARTIFICIELLE ORNITHOLOGIQUE</div>
      <div class="gold-hr"></div>
      <div class="tagline">
        منصة ذكاء اصطناعي أكاديمية — مستوى بروفيسور متخصص<br>
        كل معلومة بمصدرها المباشر · صور · صوت · تاريخ المحادثات<br>
        <span style="font-size:11px;opacity:.38;font-family:'Cormorant Garamond',serif;letter-spacing:2px">
          Cornell Lab · eBird · BirdLife · HBW · IUCN · The Auk · Ibis
        </span>
      </div>
      <div class="pills">
        <div class="pl">🖼️ Bird Photo ID</div>
        <div class="pl">🎤 Voice Questions</div>
        <div class="pl">🔊 Voice Answers</div>
        <div class="pl">📍 Inline Citations</div>
        <div class="pl">🕓 Persistent History</div>
      </div>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        lg = st.selectbox("", ["العربية", "English", "Français"], label_visibility="collapsed")
        st.session_state.lang = lg
        if st.button("✦  Enter Ornis IA  ✦", use_container_width=True):
            st.session_state.page = "chat"
            st.rerun()

# ═══════════════════════════════════════════════════════════════
#  CHAT PAGE
# ═══════════════════════════════════════════════════════════════
else:
    lang = st.session_state.lang

    # ── SIDEBAR ─────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <span class="sb-logo">ORNIS IA</span>
        <span class="sb-tagline">Ornithological Intelligence</span>
        """, unsafe_allow_html=True)

        # New Chat button
        if st.button("＋  New Chat", use_container_width=True, key="new_btn"):
            new_chat()
            st.rerun()

        st.markdown('<div class="sb-div"></div>', unsafe_allow_html=True)

        # Language
        lg2 = st.selectbox(
            "🌍 Language", ["العربية", "English", "Français"],
            index=["العربية", "English", "Français"].index(lang),
            key="lang_sb"
        )
        st.session_state.lang = lg2

        st.markdown('<div class="sb-div"></div>', unsafe_allow_html=True)

        # Search
        st.text_input(
            "", key="search_q",
            placeholder="🔍  Search conversations...",
            label_visibility="collapsed"
        )
        q = st.session_state.search_q.strip().lower()

        # History list — loaded fresh from disk every render
        st.markdown('<div class="sb-section">🕓 Chat History</div>', unsafe_allow_html=True)

        all_sessions = load_all()
        filtered = [s for s in all_sessions if (not q or q in s["title"].lower())]

        if not filtered:
            st.markdown(
                '<p style="color:rgba(212,175,55,.25);font-size:11px;padding:3px 14px">No history yet</p>',
                unsafe_allow_html=True
            )

        for s in filtered:
            is_active = (s["id"] == st.session_state.sid)
            cls = "ch-item active" if is_active else "ch-item"
            st.markdown(
                f'<div class="{cls}">💬 {s["title"][:36]}</div>'
                f'<div class="ch-date">{s["date"]}</div>',
                unsafe_allow_html=True
            )
            col_o, col_d = st.columns([3, 1])
            with col_o:
                if st.button("↗ Open", key=f"open_{s['id']}"):
                    commit()
                    loaded = get_session(s["id"])
                    if loaded:
                        st.session_state.messages = loaded["messages"]
                        st.session_state.sid = s["id"]
                    st.rerun()
            with col_d:
                if st.button("🗑", key=f"del_{s['id']}"):
                    delete_session(s["id"])
                    if s["id"] == st.session_state.sid:
                        st.session_state.messages = []
                        st.session_state.sid = str(uuid.uuid4())[:8]
                    st.rerun()

        st.markdown('<div class="sb-div"></div>', unsafe_allow_html=True)
        st.markdown("""<div style="padding:3px 14px;font-size:10px;color:#4a3f30;line-height:2.1">
<b style="color:rgba(212,175,55,.4);letter-spacing:1px">📚 SOURCES</b><br>
Cornell Lab · eBird · BirdLife<br>
Avibase · Macaulay Lib. · HBW<br>
IUCN · Xeno-canto · SORA · BHL<br>
The Auk · Ibis · J.Ornithology<br>
The Condor · Emu · PubMed<br>
Frank Gill (2020) · ResearchGate
</div>""", unsafe_allow_html=True)

        st.markdown('<div class="sb-div"></div>', unsafe_allow_html=True)
        sc1, sc2 = st.columns(2)
        with sc1:
            if st.button("🗑️ Clear", use_container_width=True, key="clr"):
                st.session_state.messages = []
                st.rerun()
        with sc2:
            if st.button("🏠 Home", use_container_width=True, key="hm"):
                commit()
                st.session_state.page = "landing"
                st.rerun()

    # ── HEADER ──────────────────────────────────────────────
    st.markdown("""
    <div class="chdr">
      <div class="clogo">🦅 ORNIS IA</div>
      <div class="csub">Professor-Level Ornithological Intelligence · Inline Citations</div>
    </div>""", unsafe_allow_html=True)

    # ── MESSAGES ────────────────────────────────────────────
    for m in st.session_state.messages:
        if m["role"] == "user":
            st.markdown(f'<div class="bu">👤 {m["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="bb">🦅 {m["content"]}'
                f'<div class="src-footer">📚 Sources cited inline — Cornell Lab · eBird · BirdLife · HBW · IUCN · The Auk · Ibis · Xeno-canto</div></div>',
                unsafe_allow_html=True
            )

    # TTS trigger
    if st.session_state.speak_it:
        last = next(
            (m["content"] for m in reversed(st.session_state.messages) if m["role"] == "model"),
            None
        )
        if last:
            speak(last, lang)
        st.session_state.speak_it = False

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── IMAGE PANEL ─────────────────────────────────────────
    if st.session_state.show_img:
        st.markdown('<div class="card"><div class="ctitle">🖼️  Bird Photo Identification</div>', unsafe_allow_html=True)
        img = st.file_uploader(
            "Upload a clear bird photo",
            type=["jpg", "jpeg", "png", "webp"],
            key="img_up"
        )
        if img:
            ci, _ = st.columns([1, 2])
            with ci:
                st.image(img, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if img and st.button("🔍  Identify Species", use_container_width=True, key="id_img"):
            with st.spinner("🔭 Professor Ornis analyzing with inline citations..."):
                res = analyze_image(img, lang)
                st.session_state.messages.append({"role": "user", "content": "📸 [Bird photo submitted]"})
                st.session_state.messages.append({"role": "model", "content": res})
                st.session_state.show_img = False
                commit()
                st.rerun()

    # ── VOICE INPUT ─────────────────────────────────────────
    with st.expander("🎤  Record question (voice)", expanded=False):
        aud = st.audio_input("🎤 Tap to record", key="voice_in")
        if aud and st.button("📝  Transcribe & Send", use_container_width=True, key="trans_btn"):
            with st.spinner("🎙️ Transcribing..."):
                ab = aud.read() if hasattr(aud, "read") else bytes(aud)
                text = transcribe(ab)
            if text:
                st.session_state.messages.append({"role": "user", "content": f"🎤 {text}"})
                with st.spinner("🤔 Professor Ornis thinking..."):
                    rep = chat_groq(text, lang, st.session_state.messages[:-1])
                st.session_state.messages.append({"role": "model", "content": rep})
                commit()
                st.rerun()
            else:
                st.warning("Could not transcribe — please try again.")

    # ── BOTTOM BAR ──────────────────────────────────────────
    b1, b2, b3 = st.columns([1, 10, 1])
    with b1:
        if st.button("➕", key="plus", help="Attach bird photo"):
            st.session_state.show_img = not st.session_state.show_img
            st.rerun()
    with b2:
        ph = {
            "العربية": "💬 اسأل البروفيسور Ornis — كل معلومة بمصدرها مباشرة...",
            "English": "💬 Ask Professor Ornis — every fact cited inline...",
            "Français": "💬 Posez votre question — chaque fait cité en ligne..."
        }
        user_input = st.chat_input(ph[lang])
    with b3:
        if st.button("🔊", key="tts", help="Read last answer aloud"):
            st.session_state.speak_it = True
            st.rerun()

    # ── PROCESS INPUT ────────────────────────────────────────
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("🤔 Consulting ornithological literature..."):
            rep = chat_groq(user_input, lang, st.session_state.messages[:-1])
        st.session_state.messages.append({"role": "model", "content": rep})
        commit()
        st.rerun()