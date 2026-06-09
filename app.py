import streamlit as st
from groq import Groq
import base64, tempfile, os, uuid, re
from datetime import datetime
import streamlit.components.v1 as components

# ═══════════════════════════════════════════════════════════════
#  MARKDOWN → HTML CONVERTER
# ═══════════════════════════════════════════════════════════════
def md_to_html(text):
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*',     r'<i>\1</i>', text)
    text = text.replace('\n', '<br>')
    return text

# ═══════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Ornis IA",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════
#  CSS
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Cormorant+Garamond:wght@300;400;600&family=Tajawal:wght@300;400;700&display=swap');

html, body, .stApp { background: #04080f !important; }
.stApp::before {
    content:''; position:fixed; inset:0; z-index:0; pointer-events:none;
    background: radial-gradient(ellipse at 20% 50%, rgba(40,10,80,.5) 0%, transparent 55%),
                radial-gradient(ellipse at 80% 20%, rgba(10,30,80,.4) 0%, transparent 55%);
}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background:#0f0f0f !important;
    border-right:1px solid rgba(255,255,255,.08) !important;
    min-width:260px !important; max-width:260px !important;
}
section[data-testid="stSidebar"] > div { padding:0 !important; }
button[data-testid="collapsedControl"] { display:none !important; }

.sb-appname {
    font-family:'Playfair Display',serif; font-size:16px; font-weight:900;
    letter-spacing:3px; color:#d4af37; padding:18px 16px 6px; display:block;
}
.stSidebar .stButton > button {
    background:transparent !important; color:rgba(255,255,255,.85) !important;
    border:1px solid rgba(255,255,255,.12) !important; border-radius:8px !important;
    padding:8px 14px !important; font-family:'Tajawal',sans-serif !important;
    font-size:13px !important; font-weight:400 !important; letter-spacing:0 !important;
    box-shadow:none !important; text-align:left !important; width:100% !important;
    transition:background .15s !important;
}
.stSidebar .stButton > button:hover {
    background:rgba(255,255,255,.06) !important;
    transform:none !important; box-shadow:none !important;
}
.sb-section {
    font-size:11px; font-weight:500; color:rgba(255,255,255,.35);
    letter-spacing:1px; text-transform:uppercase; padding:14px 16px 4px;
    font-family:'Tajawal',sans-serif;
}
.stSidebar .stTextInput input {
    background:rgba(255,255,255,.06) !important;
    border:1px solid rgba(255,255,255,.1) !important;
    border-radius:8px !important; color:rgba(255,255,255,.8) !important;
    font-size:13px !important; padding:8px 12px !important;
}
.stSidebar .stTextInput input::placeholder { color:rgba(255,255,255,.3) !important; }
.stSidebar .stTextInput input:focus { border-color:rgba(212,175,55,.4) !important; box-shadow:none !important; }
.stSidebar .stSelectbox > div > div {
    background:rgba(255,255,255,.06) !important;
    border:1px solid rgba(255,255,255,.1) !important;
    border-radius:8px !important; color:rgba(255,255,255,.8) !important;
}
.stSidebar label { color:rgba(255,255,255,.45) !important; font-size:11px !important; }
.sb-div { height:1px; background:rgba(255,255,255,.07); margin:8px 0; }

/* ── LANDING ── */
.land {
    position:relative; z-index:10; display:flex; flex-direction:column;
    align-items:center; justify-content:center;
    min-height:88vh; padding:50px 24px; text-align:center;
}
.bird-em {
    font-size:80px; margin-bottom:20px;
    animation:fl 5s ease-in-out infinite, gl 3s ease-in-out infinite alternate;
}
@keyframes fl { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-15px)} }
@keyframes gl {
    0%   { filter:drop-shadow(0 0 14px rgba(212,175,55,.5)); }
    100% { filter:drop-shadow(0 0 40px rgba(255,215,0,.9)); }
}
.brand {
    font-family:'Playfair Display',serif; font-size:clamp(50px,9vw,96px);
    font-weight:900; letter-spacing:12px;
    background:linear-gradient(180deg,#fffbe6 0%,#ffd700 15%,#d4af37 35%,#8b6914 50%,#d4af37 65%,#ffd700 80%,#c8960c 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
    filter:drop-shadow(0 2px 26px rgba(212,175,55,.5));
    animation:bin 1.8s cubic-bezier(.23,1.01,.32,1) both;
}
@keyframes bin {
    0%  { opacity:0; transform:scale(.65) translateY(38px); }
    70% { opacity:1; transform:scale(1.04) translateY(-4px); }
    100%{ opacity:1; transform:scale(1) translateY(0); }
}
.brand-sub {
    font-family:'Cormorant Garamond',serif; letter-spacing:10px;
    font-size:clamp(10px,1.4vw,13px); color:rgba(212,175,55,.58); margin-top:3px;
    animation:fi 1s ease-out 1.5s both;
}
.gold-hr { width:240px; height:1px; background:linear-gradient(90deg,transparent,#d4af37,transparent); margin:18px auto; animation:fi 1s ease-out 2s both; }
.tagline { color:rgba(255,255,255,.6); font-size:clamp(13px,1.7vw,16px); line-height:1.85; max-width:520px; animation:fi 1s ease-out 2.2s both; }
@keyframes fi { 0%{opacity:0;transform:translateY(14px)} 100%{opacity:1;transform:translateY(0)} }
.pills { display:flex; gap:9px; flex-wrap:wrap; justify-content:center; margin:22px 0; animation:fi 1s ease-out 2.5s both; }
.pl { background:rgba(212,175,55,.07); border:1px solid rgba(212,175,55,.28); border-radius:40px; padding:7px 18px; color:#d4af37; font-size:12px; }

/* ── MAIN CHAT ── */
.block-container { padding:0 !important; max-width:800px; }
section[data-testid="stMain"] > div { position:relative; z-index:10; }
.chdr {
    text-align:center; padding:18px 0 6px;
    border-bottom:1px solid rgba(212,175,55,.1); margin-bottom:12px;
    position:relative; z-index:10;
}
.clogo {
    font-family:'Playfair Display',serif; font-size:clamp(20px,3.5vw,36px);
    font-weight:900; letter-spacing:7px;
    background:linear-gradient(180deg,#ffd700,#d4af37,#8b6914);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}
.csub { font-family:'Cormorant Garamond',serif; color:rgba(212,175,55,.38); letter-spacing:4px; font-size:9px; }

.bu {
    background:linear-gradient(135deg,rgba(212,175,55,.12),rgba(212,175,55,.05));
    border:1px solid rgba(212,175,55,.26); border-radius:16px 16px 4px 16px;
    padding:13px 17px; margin:7px 0; color:#fde68a;
    font-family:'Tajawal',sans-serif; font-size:15px; position:relative; z-index:10;
}
.bb {
    background:rgba(5,10,26,.93); border:1px solid rgba(212,175,55,.12);
    border-radius:16px 16px 16px 4px; padding:17px 20px; margin:7px 0;
    color:#e3e0d8; font-family:'Tajawal',sans-serif; font-size:15px;
    line-height:1.9; position:relative; z-index:10; backdrop-filter:blur(8px);
}
.src-footer {
    margin-top:10px; padding-top:8px;
    border-top:1px solid rgba(212,175,55,.1);
    font-size:10px; color:rgba(212,175,55,.45);
}
.card {
    position:relative; z-index:10; background:rgba(5,10,26,.88);
    border:1px solid rgba(212,175,55,.16); border-radius:12px;
    padding:18px; margin-bottom:12px; backdrop-filter:blur(7px);
}
.ctitle { font-family:'Playfair Display',serif; color:#d4af37; font-size:16px; letter-spacing:2px; margin-bottom:10px; }
.divider { height:1px; background:linear-gradient(90deg,transparent,rgba(212,175,55,.22),transparent); margin:10px 0; position:relative; z-index:10; }

.stButton > button {
    background:linear-gradient(135deg,#4a3500,#c49b20,#ffd700) !important;
    color:#050200 !important; border:none !important; border-radius:28px !important;
    padding:10px 32px !important; font-family:'Playfair Display',serif !important;
    font-weight:700 !important; font-size:13px !important; letter-spacing:1.5px !important;
    box-shadow:0 0 16px rgba(212,175,55,.2) !important; transition:all .3s !important;
}
.stButton > button:hover { transform:scale(1.04) !important; box-shadow:0 0 28px rgba(212,175,55,.45) !important; }

[data-testid="stFileUploader"] { background:rgba(212,175,55,.03)!important; border:1.5px dashed rgba(212,175,55,.3)!important; border-radius:10px!important; }
[data-testid="stFileUploader"] label { color:#d4af37!important; }
[data-testid="stFileUploadDropzone"] { background:transparent!important; border:none!important; }
[data-testid="stFileUploadDropzone"] p { color:#7a6040!important; }
[data-testid="stFileUploadDropzone"] svg { fill:#d4af37!important; }
div[data-testid="stAudioInput"] { background:rgba(212,175,55,.03)!important; border:1.5px dashed rgba(212,175,55,.38)!important; border-radius:10px!important; }
.stChatInput textarea { background:rgba(5,10,28,.96)!important; border:1px solid rgba(212,175,55,.24)!important; color:#fde68a!important; border-radius:12px!important; }
.stExpander { border:1px solid rgba(212,175,55,.18)!important; border-radius:10px!important; background:rgba(5,10,26,.7)!important; }
#MainMenu, footer, header { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  CLIENTS & MODELS
# ═══════════════════════════════════════════════════════════════
client       = Groq(api_key=st.secrets["GROQ_API_KEY"])
CHAT_MODEL   = "compound-beta"
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

# ═══════════════════════════════════════════════════════════════
#  SYSTEM PROMPTS
# ═══════════════════════════════════════════════════════════════
SYS = {
"العربية": """أنت البروفيسور Ornis — عالم أورنيثولوجيا من الدرجة الأولى عالمياً.
حاصل على الدكتوراه من Cornell University، عضو في الهيئة التحريرية لـ The Auk وIbis وJournal of Ornithology.
ساهمت في تأليف أكثر من 200 ورقة علمية محكّمة ونشرت فصولاً في Handbook of the Birds of the World.
خبرتك الميدانية تمتد لأكثر من 30 عاماً في 6 قارات.

═══════════════════════════════════════
قواعد الإجابة الصارمة:
═══════════════════════════════════════
1. تجيب دائماً كأنك تكتب ورقة علمية محكّمة أو تحاضر في مؤتمر دولي
2. كل معلومة تذكرها مدعومة فوراً بمصدرها بين قوسين
3. استخدم المصطلحات العلمية الدقيقة مع شرحها
4. ابدأ دائماً بالنقطة الأكثر إثارة علمياً في الموضوع
5. اذكر دائماً الاسم العلمي اللاتيني الكامل لكل نوع
6. إذا لم تعرف معلومة بدقة: قل ذلك بوضوح بدلاً من اختراعها

═══════════════════════════════════════
هيكل الإجابة الإلزامي عن أي نوع طائر:
═══════════════════════════════════════
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🦅 [الاسم العربي الدقيق] | [Genus species, Author, Year]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 التصنيف الفيلوجيني الكامل:
المملكة: Animalia | الشعبة: Chordata | الصف: Aves
الرتبة | العائلة | الجنس | النوع
الاشتقاق اللاتيني: [معنى الكلمات في الاسم العلمي]
(المصدر: Clements Checklist v2023 ; Cornell Lab of Ornithology, 2024)

🌍 الانتشار الجغرافي ومسارات الهجرة:
[وصف دقيق للمدى الجغرافي، مسارات الهجرة بالأرقام، التوزيع الموسمي]
(المصدر: eBird Global Database, 2024 ; BirdLife International, 2024)

🏔️ البيئة والموطن الإيكولوجي:
[النوع الدقيق من الموطن، نطاق الارتفاع، المناخ المفضل، العلاقات التكافلية]
(المصدر: HBW Alive ; BirdLife International, 2024)

🎨 الوصف المورفولوجي والتشخيصي:
[القياسات الدقيقة: الطول، الوزن، باع الجناح، الريش بالتفصيل، الفوارق بين الجنسين والأعمار، السمات الفارقة عن الأنواع المشابهة]
(المصدر: Handbook of the Birds of the World — del Hoyo et al., 2024)

🔊 الصوت والتواصل:
[التوصيف الصوتي الدقيق، أنواع النداءات، الوظيفة البيولوجية، الموسمية]
(المصدر: Xeno-canto Foundation, 2024 ; Macaulay Library, Cornell)

🍃 الإيكولوجيا الغذائية وسلوكيات الصيد:
[الغذاء الدقيق، تقنيات البحث عن الطعام، الموقع في السلسلة الغذائية]
(المصدر: Journal of Ornithology ; The Auk)

🥚 البيولوجيا التكاثرية:
[موسم التكاثر، طقوس التزاوج، العش، عدد البيض، مدة الحضانة، الرعاية الأبوية]
(المصدر: HBW Alive ; Ornithology — Frank Gill, 2020)

🔬 ملاحظات علمية متخصصة:
[أبحاث حديثة، تكيفات تطورية، حقائق لا يعرفها إلا المتخصصون]
(المصدر: The Auk / Ornithology (AOS) ; Ibis (BOU) ; PubMed)

⚠️ الحالة الحفاظية والتهديدات:
[تصنيف IUCN الدقيق مع السنة، اتجاه الأعداد، التهديدات، جهود الحماية]
(المصدر: IUCN Red List, 2024 ; BirdLife International, 2024)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 المراجع الكاملة: [قائمة APA]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

للأسئلة العامة: أجب بعمق أكاديمي مع هيكل منطقي ومصادر.
لا تستخدم: Wikipedia أو مصادر غير علمية.
🚫 إذا كان السؤال خارج علم الطيور تماماً: قل فقط:
'🦅 Ornis IA مخصص حصراً لعلم الطيور. أرجو طرح سؤال يتعلق بالطيور.'""",

"English": """You are Professor Ornis — a globally recognized authority in ornithology.
PhD from Cornell University. Editorial board member of The Auk, Ibis, and Journal of Ornithology.
Over 200 peer-reviewed publications. Chapters in Handbook of the Birds of the World.
30+ years of field research across 6 continents.

═══════════════════════════════════════
NON-NEGOTIABLE RESPONSE RULES:
═══════════════════════════════════════
1. Write as if authoring a peer-reviewed paper or lecturing at an international ornithology conference
2. Every single claim must be immediately followed by its source in parentheses
3. Use precise scientific terminology with brief explanations for non-specialists
4. Always lead with the most scientifically remarkable aspect of the topic
5. Always include the full Latin binomial with author and year
6. If unsure about a fact: say so explicitly rather than fabricating

═══════════════════════════════════════
MANDATORY SPECIES STRUCTURE:
═══════════════════════════════════════
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🦅 [Common Name] | [Genus species, Author, Year]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 Complete Phylogenetic Classification:
Kingdom: Animalia | Phylum: Chordata | Class: Aves
Order | Family | Genus | Species
Etymology: [meaning of the scientific name]
(Source: Clements Checklist v2023 ; Cornell Lab of Ornithology, 2024)

🌍 Geographic Range & Migration:
[Precise range, migration routes with distances, seasonal distribution]
(Source: eBird Global Database, 2024 ; BirdLife International, 2024)

🏔️ Ecological Habitat & Niche:
[Specific habitat, altitude range, climate, symbiotic relationships]
(Source: HBW Alive ; BirdLife International, 2024)

🎨 Morphological & Diagnostic Description:
[Precise measurements: length, mass, wingspan; plumage detail; sexual dimorphism; age variation; diagnostic vs similar species]
(Source: Handbook of the Birds of the World — del Hoyo et al., 2024)

🔊 Vocalizations & Communication:
[Acoustic characterization, call types, biological function, seasonality]
(Source: Xeno-canto Foundation, 2024 ; Macaulay Library, Cornell)

🍃 Foraging Ecology & Behavior:
[Precise prey/food, hunting techniques, trophic position, ecological role]
(Source: Journal of Ornithology ; The Auk)

🥚 Reproductive Biology:
[Breeding season, courtship, nest, clutch size, incubation, parental care]
(Source: HBW Alive ; Ornithology — Frank Gill, 2020)

🔬 Specialist Scientific Notes:
[Recent research, evolutionary adaptations, facts unknown to non-specialists]
(Source: The Auk/Ornithology (AOS) ; Ibis (BOU) ; PubMed)

⚠️ Conservation Status & Threats:
[Precise IUCN category with year, population trend, threats, conservation efforts]
(Source: IUCN Red List, 2024 ; BirdLife International, 2024)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 Full References: [APA format]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For general ornithology questions: answer with academic depth and sources.
Never use: Wikipedia or non-scientific sources.
🚫 If question is completely outside ornithology: respond only with:
'🦅 Ornis IA is exclusively dedicated to ornithology. Please ask a bird-related question.'""",

"Français": """Vous êtes le Professeur Ornis — autorité mondiale en ornithologie.
Docteur de Cornell University. Membre éditorial de The Auk, Ibis et Journal of Ornithology.
Plus de 200 publications scientifiques. Chapitres dans le HBW. 30 ans de terrain sur 6 continents.

═══════════════════════════════════════
RÈGLES DE RÉPONSE ABSOLUES:
═══════════════════════════════════════
1. Rédigez comme pour un article peer-reviewed ou une conférence internationale
2. Chaque affirmation immédiatement suivie de sa source entre parenthèses
3. Terminologie scientifique précise avec brèves explications
4. Commencez par l'aspect scientifiquement le plus remarquable
5. Binôme latin complet avec auteur et année toujours inclus
6. Si incertain: dites-le honnêtement plutôt que fabriquer

═══════════════════════════════════════
STRUCTURE OBLIGATOIRE (espèce):
═══════════════════════════════════════
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🦅 [Nom commun] | [Genre espèce, Auteur, Année]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 Classification phylogénétique complète:
Règne: Animalia | Embranchement: Chordata | Classe: Aves
Ordre | Famille | Genre | Espèce + Étymologie
(Source: Clements Checklist v2023 ; Cornell Lab, 2024)

🌍 Répartition & Migration:
[Aire précise, routes migratoires avec distances, distribution saisonnière]
(Source: eBird, 2024 ; BirdLife International, 2024)

🏔️ Habitat & Niche écologique:
[Type d'habitat, altitude, climat, relations symbiotiques]
(Source: HBW Alive ; BirdLife International, 2024)

🎨 Description morphologique & diagnostique:
[Mesures précises, plumage, dimorphisme, critères diagnostiques vs espèces similaires]
(Source: HBW — del Hoyo et al., 2024)

🔊 Vocalisations & Communication:
[Caractérisation acoustique, types d'appels, fonction biologique]
(Source: Xeno-canto, 2024 ; Macaulay Library)

🍃 Écologie alimentaire & Comportement:
[Proies/aliments précis, techniques, position trophique]
(Source: Journal of Ornithology ; The Auk)

🥚 Biologie reproductive:
[Saison, rituel, nid, ponte, incubation, soins parentaux]
(Source: HBW Alive ; Ornithology — Frank Gill, 2020)

🔬 Notes scientifiques spécialisées:
[Recherches récentes, adaptations évolutives, faits réservés aux spécialistes]
(Source: The Auk ; Ibis ; PubMed)

⚠️ Statut de conservation & Menaces:
[Catégorie UICN précise avec année, tendance, menaces, conservation]
(Source: UICN, 2024 ; BirdLife International, 2024)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 Références complètes: [format APA]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Questions générales en ornithologie: profondeur académique avec sources.
Jamais: Wikipedia ou sources non scientifiques.
🚫 Si question hors ornithologie: répondez uniquement:
'🦅 Ornis IA est exclusivement dédié à l'ornithologie. Veuillez poser une question sur les oiseaux.'"""
}

# ═══════════════════════════════════════════════════════════════
#  IMAGE PROMPTS
# ═══════════════════════════════════════════════════════════════
IMG_P = {
"العربية": """أنت البروفيسور Ornis. حلّل هذه الصورة بعين عالم متخصص.
بعد كل معلومة اكتب مصدرها فوراً بين قوسين.
━━━━━━━━━━━━━━━━━━━━━━━━
🔍 التشخيص الميداني المتخصص
━━━━━━━━━━━━━━━━━━━━━━━━
🦅 الاسم العربي: | الاسم العلمي: [Genus species, Author, Year]
📌 التصنيف: الرتبة | العائلة | الجنس (المصدر: Clements Checklist v2023)
🎨 السمات التشخيصية في هذه الصورة تحديداً:
[صف بدقة ما تراه: الريش، المنقار، الحجم، الوضعية، العين، الجناح]
(المصدر: HBW Alive ; del Hoyo et al., 2024)
🔍 التمييز عن الأنواع المشابهة: (المصدر: The Auk ; Ibis)
🌍 الموطن الطبيعي: (المصدر: eBird, 2024 ; BirdLife International, 2024)
⚠️ الحالة الحفاظية (IUCN): (المصدر: IUCN Red List, 2024)
━━━━━━━━━━━━━━━━━━━━━━━━
📚 المراجع: [قائمة APA]
⚠️ ثقة التشخيص: [عالية جداً/عالية/متوسطة/منخفضة] — السبب:""",

"English": """You are Professor Ornis. Analyze this image with a specialist ornithologist's eye.
After every fact, write its source immediately in parentheses.
━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Specialist Field Identification
━━━━━━━━━━━━━━━━━━━━━━━━
🦅 Common Name: | Scientific Name: [Genus species, Author, Year]
📌 Taxonomy: Order | Family | Genus (Source: Clements Checklist v2023)
🎨 Diagnostic features visible in THIS image:
[Describe precisely: plumage, bill, size, posture, eye, wing pattern]
(Source: HBW Alive ; del Hoyo et al., 2024)
🔍 Separation from similar species: (Source: The Auk ; Ibis)
🌍 Natural habitat: (Source: eBird, 2024 ; BirdLife International, 2024)
⚠️ IUCN Conservation Status: (Source: IUCN Red List, 2024)
━━━━━━━━━━━━━━━━━━━━━━━━
📚 References: [APA list]
⚠️ ID Confidence: [Very High/High/Medium/Low] — Rationale:""",

"Français": """Vous êtes le Professeur Ornis. Analysez cette image en spécialiste.
Après chaque fait, écrivez sa source immédiatement entre parenthèses.
━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Identification de terrain spécialisée
━━━━━━━━━━━━━━━━━━━━━━━━
🦅 Nom commun: | Nom scientifique: [Genre espèce, Auteur, Année]
📌 Taxonomie: Ordre | Famille | Genre (Source: Clements Checklist v2023)
🎨 Caractéristiques diagnostiques dans CETTE image:
[Plumage, bec, taille, posture, oeil, ailes]
(Source: HBW Alive ; del Hoyo et al., 2024)
🔍 Séparation espèces similaires: (Source: The Auk ; Ibis)
🌍 Habitat naturel: (Source: eBird, 2024 ; BirdLife International, 2024)
⚠️ Statut UICN: (Source: UICN, 2024)
━━━━━━━━━━━━━━━━━━━━━━━━
📚 Références: [liste APA]
⚠️ Confiance: [Très élevée/Élevée/Moyenne/Faible] — Justification:"""
}

# ═══════════════════════════════════════════════════════════════
#  SESSION STATE INIT
# ═══════════════════════════════════════════════════════════════
defaults = {
    "all_sessions": [],
    "cur_sid":      str(uuid.uuid4())[:8],
    "messages":     [],
    "lang":         "العربية",
    "page":         "landing",
    "show_img":     False,
    "speak_it":     False,
    "search_q":     ""
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ═══════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════
def save_current():
    if not st.session_state.messages:
        return
    title = next(
        (m["content"][:52] for m in st.session_state.messages if m["role"] == "user"),
        "Conversation"
    )
    sid = st.session_state.cur_sid
    for s in st.session_state.all_sessions:
        if s["id"] == sid:
            s["title"] = title
            s["date"]  = datetime.now().strftime("%b %d · %H:%M")
            s["msgs"]  = st.session_state.messages.copy()
            return
    st.session_state.all_sessions.insert(0, {
        "id":    sid,
        "title": title,
        "date":  datetime.now().strftime("%b %d · %H:%M"),
        "msgs":  st.session_state.messages.copy()
    })

def new_chat():
    save_current()
    st.session_state.messages = []
    st.session_state.cur_sid  = str(uuid.uuid4())[:8]
    st.session_state.show_img = False

def open_session(sid):
    save_current()
    s = next((x for x in st.session_state.all_sessions if x["id"] == sid), None)
    if s:
        st.session_state.messages = s["msgs"].copy()
        st.session_state.cur_sid  = sid

def delete_session(sid):
    st.session_state.all_sessions = [
        s for s in st.session_state.all_sessions if s["id"] != sid
    ]
    if sid == st.session_state.cur_sid:
        st.session_state.messages = []
        st.session_state.cur_sid  = str(uuid.uuid4())[:8]

# ═══════════════════════════════════════════════════════════════
#  AI FUNCTIONS
# ═══════════════════════════════════════════════════════════════
def chat_groq(msg, lang):
    msgs = [{"role": "system", "content": SYS[lang]}]
    for h in st.session_state.messages[-6:]:
        msgs.append({
            "role": "assistant" if h["role"] == "model" else "user",
            "content": h["content"]
        })
    msgs.append({"role": "user", "content": msg})
    try:
        r = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=msgs,
            max_tokens=3000,
            temperature=0.05
        )
        response_text = r.choices[0].message.content or ""
        # Add web sources if compound-beta returns them
        if hasattr(r, 'sources') and r.sources:
            sources_text = "<br><br><b>🌐 Web Sources:</b><br>"
            for s in r.sources[:3]:
                title = getattr(s, 'title', '')
                url   = getattr(s, 'url',   '')
                if title and url:
                    sources_text += f"• <a href='{url}' target='_blank'>{title}</a><br>"
            response_text += sources_text
        return response_text
    except Exception as e:
        return f"⚠️ Error: {e}"

def analyze_image(img_file, lang):
    try:
        img_bytes = img_file.read()
        b64  = base64.b64encode(img_bytes).decode()
        mime = "image/png" if img_file.name.lower().endswith("png") else "image/jpeg"
        r = client.chat.completions.create(
            model=VISION_MODEL,
            messages=[{"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
                {"type": "text",      "text": IMG_P[lang]}
            ]}],
            max_tokens=1800,
            temperature=0.1
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
                model="whisper-large-v3",
                file=("audio.wav", f)
            )
        os.unlink(tmp_path)
        return result.text
    except Exception:
        return ""

def speak(text, lang):
    vl    = {"العربية": "ar", "English": "en-US", "Français": "fr-FR"}.get(lang, "en-US")
    clean = text.replace('"', ' ').replace("'", " ").replace("\n", " ")[:600]
    components.html(f"""<script>
const u = new SpeechSynthesisUtterance("{clean}");
u.lang = "{vl}"; u.rate = 0.9;
window.speechSynthesis.cancel();
window.speechSynthesis.speak(u);
</script>""", height=0)

# ═══════════════════════════════════════════════════════════════
#  LANDING PAGE
# ═══════════════════════════════════════════════════════════════
if st.session_state.page == "landing":
    st.markdown("""<style>
    section[data-testid="stSidebar"]{ display:none !important; }
    </style>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="land">
      <div class="bird-em">🦅</div>
      <div class="brand">ORNIS</div>
      <div class="brand-sub">INTELLIGENCE ARTIFICIELLE ORNITHOLOGIQUE</div>
      <div class="gold-hr"></div>
      <div class="tagline">
        منصة ذكاء اصطناعي أكاديمية — مستوى بروفيسور متخصص<br>
        كل معلومة بمصدرها المباشر · تحليل الصور · تاريخ المحادثات<br>
        <span style="font-size:11px;opacity:.38;font-family:'Cormorant Garamond',serif;letter-spacing:2px">
          Cornell Lab · eBird · BirdLife · HBW · IUCN · The Auk · Ibis
        </span>
      </div>
      <div class="pills">
        <div class="pl">🖼️ Bird Photo ID</div>
        <div class="pl">🎤 Voice Questions</div>
        <div class="pl">🔊 Voice Answers</div>
        <div class="pl">📍 Inline Citations</div>
        <div class="pl">🕓 Chat History</div>
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
        st.markdown('<span class="sb-appname">🦅 ORNIS IA</span>', unsafe_allow_html=True)

        if st.button("＋  New chat", key="new_btn", use_container_width=True):
            new_chat()
            st.rerun()

        st.markdown('<div class="sb-div"></div>', unsafe_allow_html=True)

        st.text_input("", key="search_q",
                      placeholder="🔍  Search conversations",
                      label_visibility="collapsed")

        lg2 = st.selectbox(
            "Language", ["العربية", "English", "Français"],
            index=["العربية", "English", "Français"].index(lang),
            key="lang_sb"
        )
        st.session_state.lang = lg2

        st.markdown('<div class="sb-div"></div>', unsafe_allow_html=True)

        q        = st.session_state.search_q.strip().lower()
        filtered = [s for s in st.session_state.all_sessions
                    if not q or q in s["title"].lower()]

        if filtered:
            st.markdown('<div class="sb-section">Chats</div>', unsafe_allow_html=True)
            for s in filtered:
                is_active = s["id"] == st.session_state.cur_sid
                col_t, col_d = st.columns([5, 1])
                with col_t:
                    label = ("▶ " if is_active else "") + s["title"][:34]
                    style = "color:#fff;font-weight:600;" if is_active else ""
                    st.markdown(
                        f'<div style="padding:7px 4px 1px;font-size:12px;'
                        f'font-family:Tajawal,sans-serif;color:rgba(255,255,255,.7);'
                        f'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;{style}">'
                        f'{label}</div>'
                        f'<div style="font-size:10px;color:rgba(255,255,255,.28);'
                        f'padding:0 4px 6px;">{s["date"]}</div>',
                        unsafe_allow_html=True
                    )
                    if st.button("Open", key=f"op_{s['id']}", help=s["title"]):
                        open_session(s["id"])
                        st.rerun()
                with col_d:
                    if st.button("✕", key=f"dl_{s['id']}"):
                        delete_session(s["id"])
                        st.rerun()
        else:
            st.markdown(
                '<div class="sb-section">Chats</div>'
                '<p style="color:rgba(255,255,255,.2);font-size:12px;'
                'padding:6px 4px;font-family:Tajawal,sans-serif;">No conversations yet</p>',
                unsafe_allow_html=True
            )

        st.markdown('<div class="sb-div"></div>', unsafe_allow_html=True)
        st.markdown("""<div style="padding:4px;font-size:10px;color:rgba(255,255,255,.25);line-height:2">
<b style="color:rgba(212,175,55,.4);letter-spacing:1px;font-size:9px">📚 SCIENTIFIC SOURCES</b><br>
Cornell Lab · eBird · BirdLife<br>Avibase · Macaulay · HBW<br>
IUCN · Xeno-canto · SORA · BHL<br>The Auk · Ibis · J.Ornithology<br>
Condor · Emu · PubMed · Gill 2020
</div>""", unsafe_allow_html=True)

        st.markdown('<div class="sb-div"></div>', unsafe_allow_html=True)
        sc1, sc2 = st.columns(2)
        with sc1:
            if st.button("🗑 Clear", use_container_width=True, key="clr"):
                st.session_state.messages = []
                st.rerun()
        with sc2:
            if st.button("🏠 Home", use_container_width=True, key="hm"):
                save_current()
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
            st.markdown(
                f'<div class="bu">👤 {m["content"]}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="bb">🦅 {md_to_html(m["content"])}'
                f'<br><span class="src-footer">📚 Cornell Lab · eBird · BirdLife · IUCN · The Auk · Ibis · HBW</span></div>',
                unsafe_allow_html=True
            )

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
        st.markdown('<div class="card"><div class="ctitle">🖼️  Bird Photo Identification</div>',
                    unsafe_allow_html=True)
        img = st.file_uploader("Upload a clear bird photo",
                               type=["jpg", "jpeg", "png", "webp"],
                               key="img_up")
        if img:
            ci, _ = st.columns([1, 2])
            with ci:
                st.image(img, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if img and st.button("🔍  Identify Species", use_container_width=True, key="id_img"):
            with st.spinner("🔭 Professor Ornis analyzing..."):
                res = analyze_image(img, lang)
                st.session_state.messages.append({"role": "user",  "content": "📸 [Bird photo submitted]"})
                st.session_state.messages.append({"role": "model", "content": res})
                st.session_state.show_img = False
                save_current()
                st.rerun()

    # ── VOICE ───────────────────────────────────────────────
    with st.expander("🎤  Record question (voice)", expanded=False):
        aud = st.audio_input("🎤 Tap to record", key="voice_in")
        if aud and st.button("📝  Transcribe & Send",
                             use_container_width=True, key="trans_btn"):
            with st.spinner("🎙️ Transcribing..."):
                ab   = aud.read() if hasattr(aud, "read") else bytes(aud)
                text = transcribe(ab)
            if text:
                st.session_state.messages.append({"role": "user", "content": f"🎤 {text}"})
                with st.spinner("🤔 Professor Ornis thinking..."):
                    rep = chat_groq(text, lang)
                st.session_state.messages.append({"role": "model", "content": rep})
                save_current()
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
            "العربية": "💬 اسأل البروفيسور Ornis — كل معلومة بمصدرها...",
            "English":  "💬 Ask Professor Ornis — every fact cited inline...",
            "Français": "💬 Posez votre question — chaque fait cité en ligne..."
        }
        user_input = st.chat_input(ph[lang])
    with b3:
        if st.button("🔊", key="tts", help="Read last answer aloud"):
            st.session_state.speak_it = True
            st.rerun()

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("🤔 Consulting ornithological literature..."):
            rep = chat_groq(user_input, lang)
        st.session_state.messages.append({"role": "model", "content": rep})
        save_current()
        st.rerun()