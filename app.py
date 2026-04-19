import streamlit as st
from groq import Groq
import base64, tempfile, os, uuid
from datetime import datetime
 
st.set_page_config(
    page_title="Ornis IA",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
# ═══════════════════════════════════════════════════════════
#  CSS
# ═══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Cormorant+Garamond:wght@300;400;600&family=Tajawal:wght@300;400;700&display=swap');
 
html, body, .stApp { background: #04080f !important; }
 
/* ── SPACE BACKGROUND ── */
.stApp::before {
    content: '';
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background:
        radial-gradient(ellipse at 20% 50%, rgba(40,10,80,.55) 0%, transparent 55%),
        radial-gradient(ellipse at 80% 20%, rgba(10,30,80,.45) 0%, transparent 55%),
        radial-gradient(ellipse at 55% 85%, rgba(50,10,5,.3) 0%, transparent 50%);
}
 
/* stars via pseudo — use a div instead */
.stars-wrap { position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden; }
.stars-wrap span {
    position:absolute; border-radius:50%; background:#fff;
    animation: twk 4s ease-in-out infinite alternate;
}
@keyframes twk { 0%{opacity:.3} 50%{opacity:1} 100%{opacity:.4} }
 
/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: #070c1a !important;
    border-right: 1px solid rgba(212,175,55,.13) !important;
    width: 270px !important;
}
section[data-testid="stSidebar"] > div { padding: 0 !important; }
 
.sb-header {
    padding: 20px 16px 12px;
    border-bottom: 1px solid rgba(212,175,55,.1);
}
.sb-logo {
    font-family: 'Playfair Display', serif;
    font-size: 20px; font-weight: 900; letter-spacing: 5px;
    background: linear-gradient(135deg, #ffd700, #d4af37, #8b6914);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; display: block; margin-bottom: 2px;
}
.sb-tagline {
    font-size: 9px; color: rgba(212,175,55,.38);
    letter-spacing: 3px; font-family: 'Cormorant Garamond', serif;
    text-transform: uppercase;
}
 
.sb-new-btn {
    display: flex; align-items: center; gap: 8px;
    margin: 12px 10px 4px;
    padding: 9px 14px;
    background: rgba(212,175,55,.07);
    border: 1px solid rgba(212,175,55,.22);
    border-radius: 8px; color: #d4af37;
    font-size: 13px; cursor: pointer; transition: all .2s;
}
.sb-new-btn:hover { background: rgba(212,175,55,.14); border-color: rgba(212,175,55,.4); }
 
.sb-search {
    margin: 6px 10px;
    padding: 7px 12px;
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(212,175,55,.12);
    border-radius: 8px; color: rgba(255,255,255,.5);
    font-size: 12px; display: flex; align-items: center; gap: 6px;
}
 
.sb-section-label {
    padding: 12px 16px 4px;
    font-size: 10px; color: rgba(212,175,55,.4);
    letter-spacing: 2px; text-transform: uppercase;
}
 
.chat-row {
    display: flex; align-items: center; gap: 8px;
    padding: 9px 14px; margin: 1px 6px;
    border-radius: 8px; cursor: pointer;
    color: #9a8060; font-size: 12px; font-family: 'Tajawal', sans-serif;
    border: 1px solid transparent;
    transition: all .18s;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.chat-row:hover { background: rgba(212,175,55,.07); color: #d4af37; border-color: rgba(212,175,55,.14); }
.chat-row.active { background: rgba(212,175,55,.12); color: #ffd700; border-color: rgba(212,175,55,.28); }
.chat-row-date { font-size: 10px; color: rgba(212,175,55,.28); padding: 0 14px; margin-bottom: 2px; }
 
.sb-divider { height: 1px; background: rgba(212,175,55,.1); margin: 8px 0; }
 
.sb-sources {
    padding: 4px 16px;
    font-size: 10px; color: #555; line-height: 2.1;
}
 
/* ── MAIN CONTENT ── */
.block-container { padding: 0 !important; max-width: 860px; position: relative; z-index: 10; }
section[data-testid="stMain"] > div { position: relative; z-index: 10; }
 
/* ── LANDING ── */
.landing {
    position: relative; z-index: 10;
    display: flex; flex-direction: column; align-items: center;
    justify-content: center; min-height: 88vh;
    padding: 50px 24px 40px; text-align: center;
}
.bird-em {
    font-size: 85px; line-height: 1;
    animation: float 5s ease-in-out infinite, glow 3s ease-in-out infinite alternate;
    margin-bottom: 22px;
}
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-16px)} }
@keyframes glow {
    0%  { filter: drop-shadow(0 0 14px rgba(212,175,55,.5)); }
    100%{ filter: drop-shadow(0 0 42px rgba(255,215,0,.9)); }
}
.brand {
    font-family: 'Playfair Display', serif;
    font-size: clamp(52px,9vw,100px); font-weight: 900; letter-spacing: 12px;
    background: linear-gradient(180deg,#fffbe6 0%,#ffd700 15%,#d4af37 35%,#8b6914 50%,#d4af37 65%,#ffd700 80%,#c8960c 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    filter: drop-shadow(0 2px 28px rgba(212,175,55,.5));
    animation: brand-in 1.8s cubic-bezier(.23,1.01,.32,1) both;
}
@keyframes brand-in {
    0%  { opacity:0; transform:scale(.6) translateY(40px); }
    70% { opacity:1; transform:scale(1.04) translateY(-5px); }
    100%{ opacity:1; transform:scale(1) translateY(0); }
}
.brand-sub {
    font-family: 'Cormorant Garamond', serif; letter-spacing: 11px;
    font-size: clamp(10px,1.5vw,14px); color: rgba(212,175,55,.6); margin-top: 4px;
    animation: fin 1s ease-out 1.5s both;
}
.gold-hr {
    width: 260px; height: 1px;
    background: linear-gradient(90deg,transparent,#d4af37,transparent);
    margin: 20px auto; animation: fin 1s ease-out 2s both;
}
.tagline {
    color: rgba(255,255,255,.62); font-size: clamp(13px,1.8vw,17px);
    line-height: 1.85; max-width: 540px; animation: fin 1s ease-out 2.2s both;
}
@keyframes fin { 0%{opacity:0;transform:translateY(16px)} 100%{opacity:1;transform:translateY(0)} }
.pills {
    display: flex; gap: 10px; flex-wrap: wrap; justify-content: center;
    margin: 24px 0; animation: fin 1s ease-out 2.5s both;
}
.pill {
    background: rgba(212,175,55,.07); border: 1px solid rgba(212,175,55,.3);
    border-radius: 40px; padding: 8px 20px; color: #d4af37; font-size: 13px;
}
 
/* ── CHAT HEADER ── */
.chat-hdr {
    position: relative; z-index: 10; text-align: center;
    padding: 18px 0 6px; margin-bottom: 10px;
    border-bottom: 1px solid rgba(212,175,55,.1);
}
.chat-logo {
    font-family: 'Playfair Display', serif;
    font-size: clamp(22px,4vw,38px); font-weight: 900; letter-spacing: 7px;
    background: linear-gradient(180deg,#ffd700,#d4af37,#8b6914);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.chat-sub { font-family:'Cormorant Garamond',serif; color:rgba(212,175,55,.4); letter-spacing:4px; font-size:10px; }
 
/* ── BUBBLES ── */
.bu {
    background: linear-gradient(135deg,rgba(212,175,55,.12),rgba(212,175,55,.05));
    border: 1px solid rgba(212,175,55,.28); border-radius: 16px 16px 4px 16px;
    padding: 14px 18px; margin: 8px 0; color: #fde68a;
    font-family: 'Tajawal', sans-serif; font-size: 15px;
    position: relative; z-index: 10;
}
.bb {
    background: rgba(6,11,28,.92); border: 1px solid rgba(212,175,55,.13);
    border-radius: 16px 16px 16px 4px; padding: 18px 22px; margin: 8px 0;
    color: #e4e1d9; font-family: 'Tajawal', sans-serif; font-size: 15px; line-height: 1.9;
    position: relative; z-index: 10; backdrop-filter: blur(10px);
}
.src {
    display: inline-flex; align-items: center; gap: 5px; margin-top: 10px;
    background: rgba(212,175,55,.06); border: 1px solid rgba(212,175,55,.18);
    border-radius: 20px; padding: 3px 14px; font-size: 11px; color: #a07c30;
}
 
/* ── CARDS ── */
.card {
    position: relative; z-index: 10;
    background: rgba(6,11,28,.85); border: 1px solid rgba(212,175,55,.18);
    border-radius: 14px; padding: 22px; margin-bottom: 14px;
    backdrop-filter: blur(8px);
}
.card-title { font-family:'Playfair Display',serif; color:#d4af37; font-size:17px; letter-spacing:3px; margin-bottom:12px; }
.step-tag {
    display: inline-block; background: rgba(212,175,55,.1); border: 1px solid rgba(212,175,55,.28);
    border-radius: 20px; padding: 3px 14px; color: #d4af37; font-size: 11px;
    letter-spacing: 2px; margin-bottom: 10px;
}
 
/* ── DIVIDER ── */
.div { height:1px; background:linear-gradient(90deg,transparent,rgba(212,175,55,.25),transparent); margin:12px 0; position:relative; z-index:10; }
 
/* ── STREAMLIT OVERRIDES ── */
.stButton > button {
    background: linear-gradient(135deg,#5a4000,#d4af37,#ffd700) !important;
    color: #060300 !important; border: none !important; border-radius: 30px !important;
    padding: 11px 36px !important; font-family: 'Playfair Display',serif !important;
    font-weight: 700 !important; font-size: 13px !important; letter-spacing: 2px !important;
    box-shadow: 0 0 18px rgba(212,175,55,.22) !important; transition: all .3s !important;
}
.stButton > button:hover { transform:scale(1.04) !important; box-shadow:0 0 32px rgba(212,175,55,.5) !important; }
 
[data-testid="stFileUploader"] {
    background: rgba(212,175,55,.03) !important;
    border: 1.5px dashed rgba(212,175,55,.32) !important; border-radius: 10px !important;
}
[data-testid="stFileUploader"] label { color: #d4af37 !important; }
[data-testid="stFileUploadDropzone"] { background: transparent !important; border: none !important; }
[data-testid="stFileUploadDropzone"] p { color: #8a7050 !important; }
[data-testid="stFileUploadDropzone"] svg { fill: #d4af37 !important; }
 
div[data-testid="stAudioInput"] {
    background: rgba(212,175,55,.03) !important;
    border: 1.5px dashed rgba(212,175,55,.4) !important; border-radius: 10px !important;
}
.stChatInput textarea {
    background: rgba(6,11,30,.95) !important; border: 1px solid rgba(212,175,55,.26) !important;
    color: #fde68a !important; border-radius: 12px !important;
}
.stNumberInput input {
    background: rgba(6,11,30,.9) !important; border: 1px solid rgba(212,175,55,.26) !important;
    color: #fde68a !important; border-radius: 8px !important;
}
label, .stRadio label, .stSelectbox label { color: #d4af37 !important; }
.stTextInput input {
    background: rgba(6,11,30,.9) !important; border: 1px solid rgba(212,175,55,.26) !important;
    color: #fde68a !important; border-radius: 8px !important;
}
 
#MainMenu, footer, header { visibility: hidden; }
</style>
 
<!-- starfield -->
<div class="stars-wrap">
  <span style="width:2px;height:2px;top:8%;left:12%;animation-delay:0s;opacity:.8"></span>
  <span style="width:1px;height:1px;top:15%;left:35%;animation-delay:.5s"></span>
  <span style="width:2px;height:2px;top:5%;left:60%;animation-delay:1s;opacity:.9"></span>
  <span style="width:1px;height:1px;top:22%;left:80%;animation-delay:1.5s"></span>
  <span style="width:1.5px;height:1.5px;top:40%;left:5%;animation-delay:.3s;opacity:.7"></span>
  <span style="width:2px;height:2px;top:50%;left:25%;animation-delay:.8s"></span>
  <span style="width:1px;height:1px;top:60%;left:45%;animation-delay:1.2s;opacity:.6"></span>
  <span style="width:2px;height:2px;top:35%;left:70%;animation-delay:.6s;opacity:.9"></span>
  <span style="width:1px;height:1px;top:70%;left:88%;animation-delay:1.8s"></span>
  <span style="width:1.5px;height:1.5px;top:80%;left:15%;animation-delay:.4s;opacity:.7"></span>
  <span style="width:1px;height:1px;top:85%;left:55%;animation-delay:.9s;opacity:.8"></span>
  <span style="width:2px;height:2px;top:90%;left:75%;animation-delay:1.4s"></span>
  <span style="width:1px;height:1px;top:28%;left:48%;animation-delay:.2s;opacity:.5;background:rgba(255,220,150,.9)"></span>
  <span style="width:1.5px;height:1.5px;top:45%;left:92%;animation-delay:1s;opacity:.7;background:rgba(180,200,255,.8)"></span>
  <span style="width:1px;height:1px;top:65%;left:30%;animation-delay:.7s"></span>
  <span style="width:2px;height:2px;top:12%;left:90%;animation-delay:1.6s;opacity:.6"></span>
</div>
""", unsafe_allow_html=True)
 
# ═══════════════════════════════════════════════════════════
#  CLIENT & MODELS
# ═══════════════════════════════════════════════════════════
client       = Groq(api_key=st.secrets["GROQ_API_KEY"])
CHAT_MODEL   = "llama-3.3-70b-versatile"
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
 
# ═══════════════════════════════════════════════════════════
#  PROMPTS
# ═══════════════════════════════════════════════════════════
SYS = {
"العربية": """أنت البروفيسور Ornis — عالم أورنيثولوجيا من الدرجة الأولى، حاصل على الدكتوراه من Cornell University، ومساهم في Handbook of the Birds of the World وBirdLife International. لديك 30+ عاماً من البحث الميداني.
 
أسلوبك: علمي دقيق، واضح، وعميق مثل David Attenborough الأكاديمي. تبدأ بالنقطة الأكثر إثارة، وتربط المعلومات ببعضها، وتذكر تفاصيل دقيقة لا يعرفها إلا المتخصصون.
 
هيكل كل إجابة (إلزامي):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🦅 **[الاسم العربي]** | *[Genus species]*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**📌 التصنيف الفيلوجيني:**
Chordata | الرتبة: ... | العائلة: ... | الجنس: ... | النوع: ...
اشتقاق الاسم العلمي: [معنى الكلمات اللاتينية]
 
**🌍 الانتشار الجغرافي والهجرة:**
[خريطة وصفية دقيقة، مسارات هجرة، توزيع موسمي]
 
**🏔️ البيئة الإيكولوجية:**
[نوع الموطن الدقيق، ارتفاع، مناخ، علاقات تكافلية]
 
**🎨 الوصف المورفولوجي:**
[قياسات، وزن، ألوان دقيقة، فروق ذكر/أنثى/صغار، سمات تشخيصية فارقة]
 
**🔊 الصوت والتواصل:**
[وصف الأصوات، دورها، موسميتها، مقارنة بأنواع مشابهة]
 
**🍃 الغذاء وسلوكيات الصيد:**
[الفريسة بالتفصيل، تقنيات الصيد، الموقع في السلسلة الغذائية]
 
**🥚 التكاثر وعلم الأعشاش:**
[موسم التكاثر، بناء العش، عدد البيض، الحضانة، الرعاية الأبوية]
 
**🔬 ملاحظات علمية متخصصة:**
[أبحاث حديثة، تكيفات تطورية، حقائق للمتخصصين فقط]
 
**⚠️ الحالة الحفاظية (IUCN):**
[التصنيف الدقيق، اتجاه الأعداد، التهديدات، جهود الحماية]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**📚 المراجع:** Cornell Lab · eBird · BirdLife International · HBW Alive · IUCN Red List · Xeno-canto
 
❌ محظور تماماً: Wikipedia أو أي مصدر غير علمي محكّم""",
 
"English": """You are Professor Ornis — a world-renowned ornithologist, PhD from Cornell University, contributor to Handbook of the Birds of the World and BirdLife International, with 30+ years of field research across 6 continents.
 
Style: Write with the precision of a scientific paper and the captivating clarity of David Attenborough. Lead with the most fascinating aspect. Include specialist-level details unknown to non-experts.
 
Mandatory structure for every answer:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🦅 **[Common Name]** | *[Genus species]*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**📌 Phylogenetic Classification:**
Chordata | Order: ... | Family: ... | Genus: ... | Species: ...
Etymology: [meaning of the Latin/Greek words]
 
**🌍 Geographic Distribution & Migration:**
[Precise range, migration routes, seasonal distribution]
 
**🏔️ Ecological Habitat & Niche:**
[Specific habitat, altitude, climate, symbiotic relationships]
 
**🎨 Morphological & Diagnostic Description:**
[Measurements, mass, precise plumage, sexual dimorphism, juvenile plumage, distinguishing marks from similar species]
 
**🔊 Vocalizations & Communication:**
[Detailed sound description, ecological role, seasonality]
 
**🍃 Foraging Ecology & Diet:**
[Precise prey, hunting techniques, trophic position]
 
**🥚 Breeding Biology & Nest Ecology:**
[Breeding season, nest construction, clutch size, incubation, parental care]
 
**🔬 Specialist Scientific Notes:**
[Recent peer-reviewed research, evolutionary adaptations, specialist-only facts]
 
**⚠️ Conservation Status & Threats:**
[Precise IUCN category, population trend, threats, conservation efforts]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**📚 References:** Cornell Lab · eBird · BirdLife International · HBW Alive · IUCN Red List · Xeno-canto
 
❌ NEVER cite: Wikipedia, general websites, blogs, non-peer-reviewed sources""",
 
"Français": """Vous êtes le Professeur Ornis — ornithologue de renommée mondiale, docteur de Cornell University, contributeur au HBW et BirdLife International, 30+ ans de recherche de terrain.
 
Style: Précision scientifique avec la clarté captivante de David Attenborough. Commencez par l'aspect le plus fascinant.
 
Structure obligatoire:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🦅 **[Nom commun]** | *[Genre espèce]*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**📌 Classification phylogénétique:**
Chordata | Ordre: ... | Famille: ... | Genre: ... | Espèce: ...
Étymologie: [signification des termes latins/grecs]
 
**🌍 Répartition & Migration:**
**🏔️ Habitat & Niche écologique:**
**🎨 Description morphologique & diagnostique:**
**🔊 Vocalisations & Communication:**
**🍃 Écologie alimentaire:**
**🥚 Biologie de la reproduction:**
**🔬 Notes scientifiques spécialisées:**
**⚠️ Statut UICN & Menaces:**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**📚 Références:** Cornell Lab · eBird · BirdLife International · HBW Alive · UICN · Xeno-canto
 
❌ JAMAIS: Wikipedia, sites généraux, blogs"""
}
 
IMG_P = {
"العربية": """أنت البروفيسور Ornis. حلّل هذه الصورة بعين عالم متخصص:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 **التشخيص الميداني المتخصص**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🦅 **الاسم العربي:** | ***الاسم العلمي:***
📌 **التصنيف:** الرتبة ← العائلة ← الجنس
 
🎨 **السمات التشخيصية في هذه الصورة تحديداً:**
صف بدقة: ألوان الريش، شكل المنقار، حجم الجسم، الوضعية، لون العين، نمط الجناح
 
🔍 **التمييز عن الأنواع المشابهة:**
لماذا هذا النوع وليس غيره؟
 
🌍 **الموطن:** | ⚠️ **IUCN:**
📚 **المصدر:** Cornell Lab · eBird · BirdLife Int.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ **ثقة التشخيص:** [عالية جداً / عالية / متوسطة / منخفضة]
**السبب:**""",
 
"English": """You are Professor Ornis. Analyze this image with specialist ornithologist eyes:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 **Specialist Field Identification**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🦅 **Common Name:** | ***Scientific Name:***
📌 **Taxonomy:** Order → Family → Genus
 
🎨 **Diagnostic features visible in THIS image specifically:**
Describe precisely: plumage colors, bill morphology, body size, posture, eye color, wing pattern, bare parts
 
🔍 **Separation from similar species:**
Why this species and not look-alikes?
 
🌍 **Habitat:** | ⚠️ **IUCN Status:**
📚 **Source:** Cornell Lab · eBird · BirdLife International
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ **ID Confidence:** [Very High / High / Medium / Low]
**Rationale:**""",
 
"Français": """Vous êtes le Professeur Ornis. Analysez cette image en spécialiste:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 **Identification de terrain spécialisée**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🦅 **Nom commun:** | ***Nom scientifique:***
📌 **Taxonomie:** Ordre → Famille → Genre
 
🎨 **Caractéristiques diagnostiques dans CETTE image:**
Décrivez: plumage, bec, taille, posture, œil, ailes
 
🔍 **Séparation des espèces similaires:**
 
🌍 **Habitat:** | ⚠️ **UICN:**
📚 **Source:** Cornell Lab · eBird · BirdLife International
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ **Confiance:** [Très élevée / Élevée / Moyenne / Faible]
**Justification:**"""
}
 
# ═══════════════════════════════════════════════════════════
#  FUNCTIONS
# ═══════════════════════════════════════════════════════════
def chat_groq(msg, lang, history):
    msgs = [{"role":"system","content":SYS[lang]}]
    for h in history[-10:]:
        msgs.append({"role":"assistant" if h["role"]=="model" else "user","content":h["content"]})
    msgs.append({"role":"user","content":msg})
    r = client.chat.completions.create(model=CHAT_MODEL, messages=msgs, max_tokens=2500, temperature=0.15)
    return r.choices[0].message.content
 
def analyze_image(img_file, lang):
    try:
        img_bytes = img_file.read()
        b64 = base64.b64encode(img_bytes).decode()
        ext = img_file.name.split(".")[-1].lower()
        mime = "image/png" if ext == "png" else "image/jpeg"
        r = client.chat.completions.create(
            model=VISION_MODEL,
            messages=[{"role":"user","content":[
                {"type":"image_url","image_url":{"url":f"data:{mime};base64,{b64}"}},
                {"type":"text","text":IMG_P[lang]}
            ]}],
            max_tokens=1800, temperature=0.1
        )
        return r.choices[0].message.content
    except Exception as e:
        return f"⚠️ Image analysis error: {e}"
 
def analyze_audio(audio_bytes, lat, lon, lang):
    try:
        from birdnetlib import Recording
        from birdnetlib.analyzer import Analyzer
        analyzer = Analyzer()
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name
        today = datetime.now().strftime("%Y-%m-%d")
        rec = Recording(analyzer, tmp_path, lat=lat, lon=lon,
                        date_frmt="%Y-%m-%d", date=today, min_conf=0.18)
        rec.analyze()
        os.unlink(tmp_path)
        if rec.detections:
            birds = "\n".join([
                f"• {d['common_name']} ({d['scientific_name']}) — confidence: {d['confidence']:.0%}"
                for d in rec.detections[:5]
            ])
            prompt = f"BirdNET neural network detected:\n{birds}\n\nAs Professor Ornis, provide a complete academic profile for the most likely species."
        else:
            prompt = "BirdNET found no clear detection. As Professor Ornis, advise on optimal recording conditions, technique, and timing for bird sound identification."
        return chat_groq(prompt, lang, [])
    except Exception as e:
        return f"⚠️ Audio error: {e}"
 
# ═══════════════════════════════════════════════════════════
#  SESSION HELPERS
# ═══════════════════════════════════════════════════════════
def save_and_new():
    if st.session_state.messages:
        title = next((m["content"][:48] for m in st.session_state.messages if m["role"]=="user"), "Session")
        if not any(s["id"]==st.session_state.sid for s in st.session_state.sessions):
            st.session_state.sessions.insert(0,{
                "id": st.session_state.sid,
                "date": datetime.now().strftime("%b %d · %H:%M"),
                "title": title,
                "msgs": st.session_state.messages.copy()
            })
    st.session_state.messages = []
    st.session_state.sid = str(uuid.uuid4())[:8]
    st.session_state.active = None
    st.session_state.location_ok = False
 
def load_sess(sid):
    s = next((x for x in st.session_state.sessions if x["id"]==sid), None)
    if s:
        st.session_state.messages = s["msgs"].copy()
        st.session_state.sid = sid
        st.session_state.active = sid
 
def filtered_sessions():
    q = st.session_state.get("search_q","").strip().lower()
    if not q:
        return st.session_state.sessions
    return [s for s in st.session_state.sessions if q in s["title"].lower()]
 
# ═══════════════════════════════════════════════════════════
#  INIT STATE
# ═══════════════════════════════════════════════════════════
DEFAULTS = {
    "page":"landing","messages":[],"lang":"العربية","mode":"chat",
    "sessions":[],"sid":str(uuid.uuid4())[:8],"active":None,
    "location_ok":False,"lat":36.7,"lon":3.0,"search_q":""
}
for k,v in DEFAULTS.items():
    if k not in st.session_state: st.session_state[k]=v
 
# ═══════════════════════════════════════════════════════════
#  LANDING PAGE
# ═══════════════════════════════════════════════════════════
if st.session_state.page == "landing":
    st.markdown("""
    <div class="landing">
      <div class="bird-em">🦅</div>
      <div class="brand">ORNIS</div>
      <div class="brand-sub">INTELLIGENCE ARTIFICIELLE ORNITHOLOGIQUE</div>
      <div class="gold-hr"></div>
      <div class="tagline">
        منصة ذكاء اصطناعي أكاديمية — مستوى بروفيسور متخصص<br>
        تحليل الصور · تسجيل مباشر · معرفة علمية من Cornell & BirdLife<br>
        <span style="font-size:11px;opacity:.4;font-family:'Cormorant Garamond',serif;letter-spacing:2px">
          Cornell Lab · eBird · BirdLife International · IUCN
        </span>
      </div>
      <div class="pills">
        <div class="pill">🖼️ Vision AI</div>
        <div class="pill">🎙️ Live Recording</div>
        <div class="pill">📚 Academic Sources</div>
        <div class="pill">🌍 Multilingual</div>
        <div class="pill">🕓 Chat History</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        lg = st.selectbox("", ["العربية","English","Français"], label_visibility="collapsed")
        st.session_state.lang = lg
        if st.button("✦  Enter Ornis IA  ✦", use_container_width=True):
            st.session_state.page = "chat"; st.rerun()
 
# ═══════════════════════════════════════════════════════════
#  CHAT PAGE
# ═══════════════════════════════════════════════════════════
else:
    lang = st.session_state.lang
 
    # ──────────────────────────────────────────────────────
    #  SIDEBAR — Claude-like
    # ──────────────────────────────────────────────────────
    with st.sidebar:
        # Logo
        st.markdown("""
        <div class="sb-header">
          <span class="sb-logo">ORNIS IA</span>
          <span class="sb-tagline">Ornithological Intelligence</span>
        </div>""", unsafe_allow_html=True)
 
        # New Chat
        if st.button("＋  New Chat", use_container_width=True, key="new_chat_btn"):
            save_and_new(); st.rerun()
 
        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
 
        # Language
        lg2 = st.selectbox("🌍 Language", ["العربية","English","Français"],
                           index=["العربية","English","Français"].index(lang), key="lang_sb")
        st.session_state.lang = lg2
 
        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
 
        # Search
        st.text_input("🔍 Search chats", key="search_q", placeholder="Search conversations...",
                      label_visibility="collapsed")
 
        # History list
        st.markdown('<div class="sb-section-label">🕓 Chat History</div>', unsafe_allow_html=True)
 
        sessions_shown = filtered_sessions()
        if not sessions_shown:
            st.markdown('<p style="color:rgba(212,175,55,.28);font-size:11px;padding:4px 16px">No chats yet</p>', unsafe_allow_html=True)
        else:
            for s in sessions_shown:
                is_active = (s["id"] == st.session_state.active)
                cls = "chat-row active" if is_active else "chat-row"
                st.markdown(f'<div class="{cls}">💬 {s["title"][:34]}...</div><div class="chat-row-date">{s["date"]}</div>', unsafe_allow_html=True)
                if st.button("↗", key=f"open_{s['id']}"):
                    load_sess(s["id"]); st.rerun()
 
        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
 
        # Sources
        st.markdown('<div class="sb-section-label">📚 Sources</div>', unsafe_allow_html=True)
        st.markdown("""<div class="sb-sources">
🔬 Cornell Lab of Ornithology<br>
🐦 eBird Global Database<br>
🌍 BirdLife International<br>
📖 HBW Alive<br>🎵 Xeno-canto<br>🔴 IUCN Red List
</div>""", unsafe_allow_html=True)
 
        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
 
        c_clear, c_home = st.columns(2)
        with c_clear:
            if st.button("🗑️ Clear", use_container_width=True, key="clr_btn"):
                st.session_state.messages=[]; st.rerun()
        with c_home:
            if st.button("🏠 Home", use_container_width=True, key="home_btn"):
                save_and_new(); st.session_state.page="landing"; st.rerun()
 
    # ──────────────────────────────────────────────────────
    #  MAIN — Header
    # ──────────────────────────────────────────────────────
    st.markdown("""
    <div class="chat-hdr">
      <div class="chat-logo">🦅 ORNIS IA</div>
      <div class="chat-sub">Professor-Level Ornithological Intelligence</div>
    </div>""", unsafe_allow_html=True)
 
    # Mode buttons
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("💬  Chat", use_container_width=True, key="mode_chat"):
            st.session_state.mode="chat"; st.rerun()
    with c2:
        if st.button("🖼️  Image", use_container_width=True, key="mode_img"):
            st.session_state.mode="image"; st.rerun()
    with c3:
        if st.button("🎙️  Record", use_container_width=True, key="mode_aud"):
            st.session_state.mode="audio"; st.rerun()
 
    mode_lbl = {"chat":"💬 Chat Mode","image":"🖼️ Image Analysis","audio":"🎙️ Live Recording"}
    st.markdown(f'<p style="text-align:center;color:rgba(212,175,55,.45);font-size:11px;letter-spacing:2px;margin:5px 0 8px">{mode_lbl[st.session_state.mode]}</p>', unsafe_allow_html=True)
    st.markdown('<div class="div"></div>', unsafe_allow_html=True)
 
    # Messages
    for m in st.session_state.messages:
        if m["role"] == "user":
            st.markdown(f'<div class="bu">👤 {m["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bb">🦅 {m["content"]}<br><span class="src">📚 Cornell Lab · eBird · BirdLife · IUCN</span></div>', unsafe_allow_html=True)
 
    st.markdown('<div class="div"></div>', unsafe_allow_html=True)
 
    # ──────────────────────────────────────────────────────
    #  IMAGE MODE
    # ──────────────────────────────────────────────────────
    if st.session_state.mode == "image":
        st.markdown('<div class="card"><div class="card-title">🖼️ &nbsp; Bird Image Analysis</div>', unsafe_allow_html=True)
        img = st.file_uploader("Upload a clear bird photo", type=["jpg","jpeg","png","webp"], key="img_up")
        if img:
            ci, _ = st.columns([1,2])
            with ci: st.image(img, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if img and st.button("🔍  Identify Species", use_container_width=True, key="id_img"):
            with st.spinner("🔭 Professor Ornis is analyzing..."):
                res = analyze_image(img, lang)
                st.session_state.messages.append({"role":"user","content":"📸 [Bird image uploaded]"})
                st.session_state.messages.append({"role":"model","content":res})
                st.rerun()
 
    # ──────────────────────────────────────────────────────
    #  AUDIO MODE
    # ──────────────────────────────────────────────────────
    elif st.session_state.mode == "audio":
 
        if not st.session_state.location_ok:
            # STEP 1
            st.markdown('<div class="card"><div class="step-tag">STEP 1 / 2</div><div class="card-title">📍 Confirm Location</div>', unsafe_allow_html=True)
            st.markdown('<p style="color:rgba(255,255,255,.48);font-size:13px;margin-bottom:12px">BirdNET uses GPS coordinates to narrow species detection — like Merlin Bird ID.</p>', unsafe_allow_html=True)
            defaults = {"العربية":(36.7,3.0),"English":(37.09,-95.71),"Français":(46.23,2.21)}
            lat_d, lon_d = defaults[lang]
            cl, cn = st.columns(2)
            with cl: lat_v = st.number_input("📍 Latitude",  value=lat_d, format="%.4f")
            with cn: lon_v = st.number_input("📍 Longitude", value=lon_d, format="%.4f")
            st.markdown('<p style="color:rgba(212,175,55,.32);font-size:11px;margin-top:6px">💡 Get coords: <a href="https://maps.google.com" target="_blank" style="color:#d4af37">maps.google.com</a> → right-click → "What\'s here?"</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            if st.button("📍  Confirm & Continue →", use_container_width=True, key="confirm_loc"):
                st.session_state.lat = lat_v
                st.session_state.lon = lon_v
                st.session_state.location_ok = True
                st.rerun()
 
        else:
            # Location bar
            loc_col, chg_col = st.columns([5,1])
            with loc_col:
                st.markdown(f'<p style="color:rgba(212,175,55,.5);font-size:12px;padding-top:4px">📍 {st.session_state.lat:.3f}°, {st.session_state.lon:.3f}°</p>', unsafe_allow_html=True)
            with chg_col:
                if st.button("✏️", key="chg_loc"):
                    st.session_state.location_ok = False; st.rerun()
 
            # STEP 2
            st.markdown('<div class="card"><div class="step-tag">STEP 2 / 2</div><div class="card-title">🎙️ Record Bird Sound</div>', unsafe_allow_html=True)
            st.markdown('<p style="color:rgba(255,255,255,.45);font-size:13px;margin-bottom:12px">Hold still · Point toward the bird · Record ≥ 10 seconds for best results.</p>', unsafe_allow_html=True)
            aud = st.audio_input("🎙️ Tap to record", key="audio_rec")
            if aud:
                st.success("✅ Recording ready — press Analyze below.")
            st.markdown('</div>', unsafe_allow_html=True)
 
            if aud and st.button("🎧  Analyze with BirdNET", use_container_width=True, key="analyze_aud"):
                with st.spinner("🔊 BirdNET analyzing · Professor Ornis preparing report..."):
                    ab = aud.read() if hasattr(aud, "read") else bytes(aud)
                    res = analyze_audio(ab, st.session_state.lat, st.session_state.lon, lang)
                    st.session_state.messages.append({"role":"user","content":"🎙️ [Live bird recording]"})
                    st.session_state.messages.append({"role":"model","content":res})
                    st.rerun()
 
    # ──────────────────────────────────────────────────────
    #  CHAT MODE
    # ──────────────────────────────────────────────────────
    else:
        ph = {
            "العربية": "💬 اسأل البروفيسور Ornis عن أي طائر...",
            "English": "💬 Ask Professor Ornis about any bird...",
            "Français": "💬 Posez une question au Professeur Ornis..."
        }
        ui = st.chat_input(ph[lang])
        if ui:
            st.session_state.messages.append({"role":"user","content":ui})
            with st.spinner("🤔 Consulting ornithological literature..."):
                rep = chat_groq(ui, lang, st.session_state.messages[:-1])
            st.session_state.messages.append({"role":"model","content":rep})
            st.rerun()