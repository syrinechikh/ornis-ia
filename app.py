import streamlit as st
from groq import Groq
import base64, tempfile, os, uuid
from datetime import datetime
 
st.set_page_config(page_title="Ornis IA", page_icon="🦅", layout="wide", initial_sidebar_state="expanded")
 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Cormorant+Garamond:wght@300;400;600;700&family=Tajawal:wght@300;400;700&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
html,body,.stApp{background:#04080f!important;font-family:'Tajawal',sans-serif;}
 
/* SPACE */
.space-bg{position:fixed;inset:0;z-index:0;pointer-events:none;
  background:radial-gradient(ellipse at 20% 50%,rgba(40,10,80,.5) 0%,transparent 55%),
  radial-gradient(ellipse at 80% 20%,rgba(10,30,80,.4) 0%,transparent 55%),#04080f;}
.stars{position:fixed;inset:0;z-index:0;pointer-events:none;
  background-image:
    radial-gradient(1.5px 1.5px at 8% 12%,#fff 0%,transparent 100%),
    radial-gradient(1px 1px at 22% 5%,rgba(255,255,255,.8) 0%,transparent 100%),
    radial-gradient(2px 2px at 37% 22%,#fff 0%,transparent 100%),
    radial-gradient(1px 1px at 53% 8%,rgba(255,220,150,.9) 0%,transparent 100%),
    radial-gradient(1.5px 1.5px at 68% 18%,#fff 0%,transparent 100%),
    radial-gradient(2px 2px at 91% 30%,#fff 0%,transparent 100%),
    radial-gradient(1px 1px at 14% 45%,rgba(255,255,255,.6) 0%,transparent 100%),
    radial-gradient(2px 2px at 59% 62%,#fff 0%,transparent 100%),
    radial-gradient(1px 1px at 74% 50%,rgba(200,210,255,.8) 0%,transparent 100%),
    radial-gradient(2px 2px at 20% 80%,#fff 0%,transparent 100%),
    radial-gradient(1px 1px at 65% 85%,rgba(180,200,255,.7) 0%,transparent 100%),
    radial-gradient(1px 1px at 94% 68%,rgba(255,255,255,.5) 0%,transparent 100%),
    radial-gradient(1.5px 1.5px at 45% 35%,rgba(255,240,180,.7) 0%,transparent 100%),
    radial-gradient(1px 1px at 82% 55%,rgba(255,255,255,.6) 0%,transparent 100%);
  animation:twinkle 5s ease-in-out infinite alternate;}
@keyframes twinkle{0%{opacity:.5}50%{opacity:1}100%{opacity:.6}}
 
/* ═══ SIDEBAR ═══ */
[data-testid="stSidebar"]{background:rgba(6,10,20,.98)!important;border-right:1px solid rgba(212,175,55,.12)!important;min-width:260px!important;}
[data-testid="stSidebar"] .block-container{padding:0!important;}
 
.sb-logo{font-family:'Playfair Display',serif;font-size:22px;font-weight:900;letter-spacing:5px;
  background:linear-gradient(135deg,#ffd700,#d4af37,#8b6914);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  padding:20px 16px 4px;display:block;}
.sb-sub{font-size:10px;color:rgba(212,175,55,.4);letter-spacing:3px;padding:0 16px 16px;display:block;font-family:'Cormorant Garamond',serif;}
.sb-divider{height:1px;background:linear-gradient(90deg,transparent,rgba(212,175,55,.2),transparent);margin:6px 0;}
.sb-section{padding:8px 16px 4px;font-size:10px;color:rgba(212,175,55,.5);letter-spacing:2px;text-transform:uppercase;}
 
.sb-new-btn{display:flex;align-items:center;gap:8px;padding:8px 14px;margin:6px 10px;
  background:rgba(212,175,55,.08);border:1px solid rgba(212,175,55,.25);border-radius:8px;
  color:#d4af37;font-size:13px;cursor:pointer;transition:all .2s;}
.sb-new-btn:hover{background:rgba(212,175,55,.16);border-color:rgba(212,175,55,.45);}
 
.chat-item{display:flex;align-items:center;gap:8px;padding:9px 14px;margin:2px 8px;
  border-radius:8px;cursor:pointer;color:#b8a07a;font-size:12px;
  transition:all .2s;border:1px solid transparent;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.chat-item:hover{background:rgba(212,175,55,.08);border-color:rgba(212,175,55,.15);color:#d4af37;}
.chat-item.active{background:rgba(212,175,55,.12);border-color:rgba(212,175,55,.3);color:#ffd700;}
.chat-date{font-size:10px;color:rgba(212,175,55,.3);padding:0 14px 2px;margin-top:4px;}
 
/* ═══ LANDING ═══ */
.landing-wrap{position:relative;z-index:10;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:88vh;padding:40px 20px;text-align:center;}
.bird-icon{font-size:80px;line-height:1;animation:float 5s ease-in-out infinite,glow-bird 3s ease-in-out infinite alternate;margin-bottom:24px;}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-16px)}}
@keyframes glow-bird{0%{filter:drop-shadow(0 0 15px rgba(212,175,55,.5))}100%{filter:drop-shadow(0 0 45px rgba(255,215,0,.9))}}
.brand-title{font-family:'Playfair Display',serif;font-size:clamp(50px,9vw,100px);font-weight:900;letter-spacing:12px;
  background:linear-gradient(180deg,#fffbe6 0%,#ffd700 15%,#d4af37 35%,#8b6914 50%,#d4af37 65%,#ffd700 80%,#c8960c 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  filter:drop-shadow(0 2px 30px rgba(212,175,55,.5));animation:title-in 1.8s cubic-bezier(.23,1.01,.32,1) forwards;opacity:0;}
@keyframes title-in{0%{opacity:0;transform:scale(.65) translateY(40px)}70%{opacity:1;transform:scale(1.04) translateY(-5px)}100%{opacity:1;transform:scale(1) translateY(0)}}
.brand-ia{font-family:'Cormorant Garamond',serif;font-size:clamp(11px,1.5vw,15px);letter-spacing:12px;color:rgba(212,175,55,.65);margin-top:4px;animation:fup 1s ease-out 1.5s forwards;opacity:0;}
.gold-line{width:260px;height:1px;background:linear-gradient(90deg,transparent,#d4af37,transparent);margin:20px auto;animation:fup 1s ease-out 2s forwards;opacity:0;}
.tagline{color:rgba(255,255,255,.6);font-size:clamp(13px,1.8vw,17px);line-height:1.8;max-width:540px;animation:fup 1s ease-out 2.2s forwards;opacity:0;}
@keyframes fup{0%{opacity:0;transform:translateY(18px)}100%{opacity:1;transform:translateY(0)}}
.feat-row{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin:26px 0;animation:fup 1s ease-out 2.5s forwards;opacity:0;}
.feat-pill{background:rgba(212,175,55,.07);border:1px solid rgba(212,175,55,.3);border-radius:40px;padding:8px 20px;color:#d4af37;font-size:13px;}
 
/* ═══ CHAT AREA ═══ */
.chat-top{position:relative;z-index:10;text-align:center;padding:18px 0 6px;border-bottom:1px solid rgba(212,175,55,.12);margin-bottom:12px;}
.chat-logo{font-family:'Playfair Display',serif;font-size:clamp(24px,4vw,40px);font-weight:900;letter-spacing:7px;
  background:linear-gradient(180deg,#ffd700 0%,#d4af37 50%,#8b6914 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.chat-sub{font-family:'Cormorant Garamond',serif;color:rgba(212,175,55,.45);letter-spacing:4px;font-size:10px;text-transform:uppercase;}
 
.bubble-user{background:linear-gradient(135deg,rgba(212,175,55,.13),rgba(212,175,55,.06));
  border:1px solid rgba(212,175,55,.3);border-radius:16px 16px 4px 16px;
  padding:14px 18px;margin:8px 0;color:#fde68a;font-size:15px;position:relative;z-index:10;}
.bubble-bot{background:rgba(7,12,30,.9);border:1px solid rgba(212,175,55,.15);
  border-radius:16px 16px 16px 4px;padding:18px 22px;margin:8px 0;
  color:#e5e2da;font-size:15px;line-height:1.9;position:relative;z-index:10;backdrop-filter:blur(10px);}
.src-badge{display:inline-flex;align-items:center;gap:5px;margin-top:10px;
  background:rgba(212,175,55,.07);border:1px solid rgba(212,175,55,.2);
  border-radius:20px;padding:4px 14px;font-size:11px;color:#b8943a;letter-spacing:.5px;}
 
.upload-card{position:relative;z-index:10;background:rgba(7,12,30,.8);
  border:1px solid rgba(212,175,55,.2);border-radius:14px;padding:22px;margin-bottom:16px;backdrop-filter:blur(8px);}
.upload-title{font-family:'Playfair Display',serif;color:#d4af37;font-size:17px;letter-spacing:3px;margin-bottom:14px;}
.step-pill{display:inline-block;background:rgba(212,175,55,.12);border:1px solid rgba(212,175,55,.3);
  border-radius:20px;padding:3px 14px;color:#d4af37;font-size:11px;letter-spacing:2px;margin-bottom:10px;}
 
/* MODE TABS */
.mode-tabs{display:flex;gap:8px;margin-bottom:14px;position:relative;z-index:10;}
.mode-tab{flex:1;padding:10px;text-align:center;border:1px solid rgba(212,175,55,.2);border-radius:10px;
  color:rgba(212,175,55,.6);font-size:13px;background:rgba(212,175,55,.04);cursor:pointer;transition:all .2s;}
.mode-tab.on{background:rgba(212,175,55,.14);border-color:rgba(212,175,55,.5);color:#ffd700;font-weight:700;}
 
/* Streamlit */
.stButton>button{background:linear-gradient(135deg,#6b4f00,#d4af37,#ffd700)!important;color:#060300!important;
  border:none!important;border-radius:30px!important;padding:11px 36px!important;
  font-family:'Playfair Display',serif!important;font-weight:700!important;font-size:14px!important;
  letter-spacing:2px!important;box-shadow:0 0 20px rgba(212,175,55,.25)!important;transition:all .3s!important;}
.stButton>button:hover{transform:scale(1.04)!important;box-shadow:0 0 35px rgba(212,175,55,.55)!important;}
[data-testid="stFileUploader"]{background:rgba(212,175,55,.03)!important;border:1.5px dashed rgba(212,175,55,.35)!important;border-radius:10px!important;padding:4px!important;}
[data-testid="stFileUploader"] label{color:#d4af37!important;}
[data-testid="stFileUploadDropzone"]{background:transparent!important;border:none!important;}
[data-testid="stFileUploadDropzone"] p{color:#a0896a!important;}
[data-testid="stFileUploadDropzone"] svg{fill:#d4af37!important;}
div[data-testid="stAudioInput"]{background:rgba(212,175,55,.04)!important;border:1.5px dashed rgba(212,175,55,.45)!important;border-radius:10px!important;}
label,.stRadio label,.stSelectbox label{color:#d4af37!important;}
.stChatInput textarea{background:rgba(8,14,36,.95)!important;border:1px solid rgba(212,175,55,.28)!important;color:#fde68a!important;border-radius:12px!important;}
.stNumberInput input{background:rgba(8,14,36,.9)!important;border:1px solid rgba(212,175,55,.28)!important;color:#fde68a!important;border-radius:8px!important;}
.divider{height:1px;background:linear-gradient(90deg,transparent,rgba(212,175,55,.3),transparent);margin:12px 0;position:relative;z-index:10;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding-top:0!important;max-width:860px;}
section[data-testid="stMain"]>div{position:relative;z-index:10;}
</style>
<div class="space-bg"></div><div class="stars"></div>
""", unsafe_allow_html=True)
 
# ── CLIENT ───────────────────────────────────────────────────
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
CHAT_MODEL   = "llama-3.3-70b-versatile"
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"  # current Groq vision model
 
# ── PROFESSOR-LEVEL PROMPTS ──────────────────────────────────
SYS = {
"العربية": """أنت البروفيسور Ornis — عالم أورنيثولوجيا (علم الطيور) من الدرجة الأولى، حاصل على الدكتوراه من Cornell University، ومساهم في Handbook of the Birds of the World وBirdLife International. خبرتك تمتد لأكثر من 30 عاماً في الميدان.
 
أسلوبك في الإجابة:
- تتحدث بلغة علمية دقيقة لكنها مفهومة، كما يفعل David Attenborough لو كان متخصصاً أكاديمياً
- تبدأ دائماً بالنقطة الأكثر أهمية وإثارة للاهتمام
- تربط المعلومات ببعضها وتبني السياق العلمي
- تذكر التفاصيل الدقيقة التي لا يعرفها إلا المختصون
- تستشهد بأبحاث ودراسات ميدانية حقيقية
 
هيكل إجابتك الإلزامي:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🦅 [الاسم العربي الدقيق] | *[Genus species]*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**📌 التصنيف الفيلوجيني:**
الشعبة: Chordata | الرتبة: ... | العائلة: ... | الجنس: ... | النوع: ...
[اذكر الاشتقاق اللاتيني للاسم العلمي وما يعنيه]
 
**🌍 الانتشار الجغرافي والهجرة:**
[خريطة وصفية دقيقة، مسارات الهجرة إن وُجدت، التوزيع الموسمي]
 
**🏔️ البيئة والموطن الايكولوجي:**
[النوع الدقيق من الموطن، الارتفاع، المناخ، العلاقات التكافلية]
 
**🎨 الوصف المورفولوجي والتشخيصي:**
[القياسات، الوزن، الألوان بدقة، الفوارق بين الذكر والأنثى والطيور الصغيرة، والسمات التشخيصية الفارقة عن الأنواع المشابهة]
 
**🔊 الصوت والتواصل:**
[وصف الأصوات، دورها البيئي، الموسمية، مقارنة بالأنواع القريبة]
 
**🍃 الغذاء وسلوكيات الصيد:**
[الفريسة أو الغذاء بالتفصيل، تقنيات الصيد أو الأكل، السلسلة الغذائية]
 
**🥚 التكاثر وعلم الأعشاش:**
[موسم التكاثر، بناء العش، عدد البيض، مدة الحضانة، الرعاية الأبوية]
 
**🔬 ملاحظات علمية متخصصة:**
[أبحاث حديثة، تكيفات تطورية مثيرة، حقائق غير معروفة للعامة]
 
**⚠️ الحالة الحفاظية والتهديدات:**
[تصنيف IUCN الدقيق، اتجاه الأعداد، التهديدات الرئيسية، جهود الحماية]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**📚 المراجع العلمية:**
• Cornell Lab of Ornithology — allaboutbirds.org
• eBird Global Database — ebird.org
• BirdLife International — birdlife.org/datazone
• HBW Alive — hbw.com
• IUCN Red List — iucnredlist.org
• Xeno-canto — xeno-canto.org [للأصوات]
 
❌ لا تستخدم أبداً: Wikipedia، مواقع عامة، مدونات، أو مصادر غير محكّمة""",
 
"English": """You are Professor Ornis — a world-renowned ornithologist with a PhD from Cornell University, a contributor to the Handbook of the Birds of the World, and a field researcher with 30+ years of expertise across 6 continents.
 
Your response style:
- Write with the precision of a scientific paper and the clarity of David Attenborough
- Lead with the most fascinating, intellectually engaging aspect
- Connect information to build deep ecological understanding
- Include details only field specialists would know
- Reference real research and fieldwork
 
Mandatory response structure:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🦅 [Precise Common Name] | *[Genus species]*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**📌 Phylogenetic Classification:**
Phylum: Chordata | Order: ... | Family: ... | Genus: ... | Species: ...
[Include etymology of the scientific name]
 
**🌍 Geographic Distribution & Migration:**
[Precise range, migration routes if applicable, seasonal distribution]
 
**🏔️ Habitat & Ecological Niche:**
[Specific habitat type, altitude, climate, symbiotic relationships]
 
**🎨 Morphological & Diagnostic Description:**
[Measurements, mass, precise plumage, sexual dimorphism, juvenile plumage, distinguishing features from similar species]
 
**🔊 Vocalizations & Communication:**
[Detailed sound description, ecological role, seasonality]
 
**🍃 Foraging & Diet:**
[Precise prey/food items, hunting techniques, trophic position]
 
**🥚 Breeding & Nest Biology:**
[Breeding season, nest construction, clutch size, incubation period, parental care]
 
**🔬 Specialist Scientific Notes:**
[Recent research, evolutionary adaptations, facts unknown to non-specialists]
 
**⚠️ Conservation Status & Threats:**
[Precise IUCN category, population trend, threats, conservation efforts]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**📚 Scientific References:**
• Cornell Lab / AllAboutBirds — allaboutbirds.org
• eBird — ebird.org
• BirdLife International — birdlife.org/datazone
• HBW Alive — hbw.com
• IUCN Red List — iucnredlist.org
• Xeno-canto — xeno-canto.org [vocalizations]
 
❌ NEVER cite: Wikipedia, general websites, blogs, non-peer-reviewed sources""",
 
"Français": """Vous êtes le Professeur Ornis — ornithologue de renommée mondiale, docteur de l'Université Cornell, contributeur au Handbook of the Birds of the World, chercheur de terrain avec plus de 30 ans d'expérience sur 6 continents.
 
Style de réponse:
- Précision scientifique avec la clarté de David Attenborough
- Commencez par l'aspect le plus fascinant
- Construisez une compréhension écologique profonde
- Incluez des détails que seuls les spécialistes connaissent
 
Structure obligatoire:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🦅 [Nom commun précis] | *[Genre espèce]*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**📌 Classification phylogénétique:**
Phylum: Chordata | Ordre: ... | Famille: ... | Genre: ... | Espèce: ...
[Étymologie du nom scientifique]
 
**🌍 Distribution & Migration:**
[Aire de répartition précise, routes migratoires, distribution saisonnière]
 
**🏔️ Habitat & Niche écologique:**
[Type d'habitat, altitude, climat, relations symbiotiques]
 
**🎨 Description morphologique & diagnostique:**
[Mesures, masse, plumage précis, dimorphisme sexuel, espèces similaires]
 
**🔊 Vocalisations & Communication:**
[Description sonore, rôle écologique, saisonnalité]
 
**🍃 Alimentation & Techniques de chasse:**
[Proies/aliments précis, techniques, position trophique]
 
**🥚 Reproduction & Biologie des nids:**
[Saison de reproduction, construction du nid, taille de la couvée, incubation]
 
**🔬 Notes scientifiques spécialisées:**
[Recherches récentes, adaptations évolutives]
 
**⚠️ Statut de conservation & Menaces:**
[Catégorie UICN précise, tendance, menaces, efforts de conservation]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**📚 Références scientifiques:**
• Cornell Lab — allaboutbirds.org
• eBird — ebird.org
• BirdLife International — birdlife.org/datazone
• HBW Alive — hbw.com
• Liste rouge UICN — iucnredlist.org
• Xeno-canto — xeno-canto.org [vocalisations]
 
❌ JAMAIS: Wikipedia, sites généraux, blogs"""
}
 
IMG_P = {
"العربية": """أنت البروفيسور Ornis. حلّل هذه الصورة بعين عالم طيور متخصص وقدّم تشخيصاً علمياً شاملاً:
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 التشخيص المرئي الميداني
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🦅 **الاسم العربي:** | ***الاسم العلمي:***
📌 **التصنيف:** الرتبة ← العائلة ← الجنس ← النوع
 
🎨 **السمات التشخيصية المرئية في هذه الصورة تحديداً:**
[صف بدقة ما تراه: ألوان الريش، شكل المنقار، حجم الجسم، وضعية الجسم، لون العين، إلخ]
 
🔍 **التمييز عن الأنواع المشابهة:**
[لماذا هذا النوع وليس غيره؟ ما السمات الفارقة؟]
 
🌍 **الموطن الطبيعي والانتشار:**
⚠️ **حالة الحفاظ (IUCN):**
📚 **المصادر:** Cornell Lab · eBird · BirdLife International
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ **مستوى الثقة في التشخيص:** [عالٍ جداً/عالٍ/متوسط/منخفض]
**السبب:** [لماذا هذا المستوى من الثقة؟]""",
 
"English": """You are Professor Ornis. Analyze this image with the eye of a specialist ornithologist and provide a complete scientific diagnosis:
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Field Identification Assessment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🦅 **Common Name:** | ***Scientific Name:***
📌 **Classification:** Order → Family → Genus → Species
 
🎨 **Diagnostic features visible in THIS image specifically:**
[Describe precisely what you see: plumage colors, bill shape, body size, posture, eye color, wing pattern, etc.]
 
🔍 **Separation from similar species:**
[Why this species and not others? What are the distinguishing marks?]
 
🌍 **Natural Habitat & Range:**
⚠️ **IUCN Conservation Status:**
📚 **Sources:** Cornell Lab · eBird · BirdLife International
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ **Identification Confidence:** [Very High/High/Medium/Low]
**Rationale:** [Why this confidence level?]""",
 
"Français": """Vous êtes le Professeur Ornis. Analysez cette image avec l'œil d'un ornithologue spécialiste:
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 Diagnostic d'identification de terrain
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🦅 **Nom commun:** | ***Nom scientifique:***
📌 **Classification:** Ordre → Famille → Genre → Espèce
 
🎨 **Caractéristiques diagnostiques visibles dans CETTE image:**
[Décrivez précisément: couleurs du plumage, forme du bec, taille, posture, etc.]
 
🔍 **Séparation des espèces similaires:**
[Pourquoi cette espèce? Quels sont les critères distinctifs?]
 
🌍 **Habitat naturel & Répartition:**
⚠️ **Statut UICN:**
📚 **Sources:** Cornell Lab · eBird · BirdLife International
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ **Niveau de confiance:** [Très élevé/Élevé/Moyen/Faible]
**Justification:** [Pourquoi ce niveau?]"""
}
 
# ── CORE FUNCTIONS ───────────────────────────────────────────
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
        mime = "image/png" if ext=="png" else "image/jpeg"
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
            tmp.write(audio_bytes); tmp_path = tmp.name
        today = datetime.now().strftime("%Y-%m-%d")
        rec = Recording(analyzer, tmp_path, lat=lat, lon=lon, date_frmt="%Y-%m-%d", date=today, min_conf=0.20)
        rec.analyze()
        os.unlink(tmp_path)
        if rec.detections:
            birds = "\n".join([f"• {d['common_name']} ({d['scientific_name']}) — confidence: {d['confidence']:.0%}" for d in rec.detections[:5]])
            prompt = f"BirdNET neural network analysis detected the following species from the audio recording:\n{birds}\n\nAs Professor Ornis, provide a complete academic profile for the most likely species."
        else:
            prompt = "BirdNET found no clear detection. As Professor Ornis, advise on optimal recording technique and conditions for bird sound identification."
        return chat_groq(prompt, lang, [])
    except Exception as e:
        return f"⚠️ Audio error: {e}"
 
# ── SESSION HELPERS ──────────────────────────────────────────
def new_session():
    # save current if non-empty
    if st.session_state.messages:
        title = next((m["content"][:50] for m in st.session_state.messages if m["role"]=="user"), "Session")
        exists = any(s["id"]==st.session_state.sid for s in st.session_state.sessions)
        if not exists:
            st.session_state.sessions.insert(0,{
                "id":st.session_state.sid,
                "date":datetime.now().strftime("%b %d, %H:%M"),
                "title":title,
                "messages":st.session_state.messages.copy()
            })
    st.session_state.messages = []
    st.session_state.sid = str(uuid.uuid4())[:8]
    st.session_state.active_session = None
 
def load_session(sid):
    s = next((x for x in st.session_state.sessions if x["id"]==sid), None)
    if s:
        st.session_state.messages = s["messages"].copy()
        st.session_state.sid = sid
        st.session_state.active_session = sid
 
# ── STATE INIT ───────────────────────────────────────────────
for k,v in {"page":"landing","messages":[],"lang":"العربية","mode":"chat",
            "sessions":[],"sid":str(uuid.uuid4())[:8],"active_session":None,
            "location_ok":False,"lat":36.7,"lon":3.0}.items():
    if k not in st.session_state: st.session_state[k]=v
 
# ════════════════════════════════════════════════════════════
#  LANDING
# ════════════════════════════════════════════════════════════
if st.session_state.page == "landing":
    st.markdown("""
    <div class="landing-wrap">
      <div class="bird-icon">🦅</div>
      <div class="brand-title">ORNIS</div>
      <div class="brand-ia">INTELLIGENCE ARTIFICIELLE ORNITHOLOGIQUE</div>
      <div class="gold-line"></div>
      <div class="tagline">
        منصة ذكاء اصطناعي أكاديمية — مستوى بروفيسور متخصص<br>
        تحليل الصور · تسجيل مباشر · معرفة علمية من Cornell & BirdLife<br>
        <span style="font-size:12px;opacity:.45;font-family:'Cormorant Garamond',serif;letter-spacing:2px">
          Scientific Partner of Cornell Lab · eBird · BirdLife International
        </span>
      </div>
      <div class="feat-row">
        <div class="feat-pill">🖼️ Vision AI</div>
        <div class="feat-pill">🎙️ Live Recording</div>
        <div class="feat-pill">📚 Academic Sources</div>
        <div class="feat-pill">🌍 Multilingual</div>
        <div class="feat-pill">🕓 Chat History</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    c1,c2,c3 = st.columns([1,2,1])
    with c2:
        lg = st.selectbox("", ["العربية","English","Français"], label_visibility="collapsed")
        st.session_state.lang = lg
        if st.button("✦  Enter Ornis IA  ✦", use_container_width=True):
            st.session_state.page="chat"; st.rerun()
 
# ════════════════════════════════════════════════════════════
#  CHAT PAGE
# ════════════════════════════════════════════════════════════
else:
    lang = st.session_state.lang
 
    # ── SIDEBAR ─────────────────────────────────────────────
    with st.sidebar:
        st.markdown('<span class="sb-logo">ORNIS IA</span><span class="sb-sub">ORNITHOLOGICAL AI</span>', unsafe_allow_html=True)
        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
 
        if st.button("✦  New Chat", use_container_width=True, key="new_chat"):
            new_session(); st.rerun()
 
        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
 
        lg2 = st.selectbox("🌍 Language", ["العربية","English","Français"],
                           index=["العربية","English","Français"].index(lang), key="lang_sel")
        st.session_state.lang = lg2
 
        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sb-section">🕓 CHAT HISTORY</div>', unsafe_allow_html=True)
 
        if not st.session_state.sessions:
            st.markdown('<p style="color:rgba(212,175,55,.3);font-size:11px;padding:4px 16px">No history yet</p>', unsafe_allow_html=True)
        else:
            for s in st.session_state.sessions:
                is_active = s["id"] == st.session_state.active_session
                cls = "chat-item active" if is_active else "chat-item"
                st.markdown(f'<div class="{cls}">💬 {s["title"][:32]}...</div><div class="chat-date">🕓 {s["date"]}</div>', unsafe_allow_html=True)
                if st.button("Open", key=f"op_{s['id']}"):
                    load_session(s["id"]); st.rerun()
 
        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sb-section">📚 SOURCES</div>', unsafe_allow_html=True)
        st.markdown("""<p style="color:#666;font-size:10px;padding:4px 16px;line-height:2.2">
🔬 Cornell Lab of Ornithology<br>🐦 eBird Global Database<br>
🌍 BirdLife International<br>📖 HBW Alive<br>
🎵 Xeno-canto<br>🔴 IUCN Red List</p>""", unsafe_allow_html=True)
 
        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
        if st.button("🗑️ Clear Chat", key="clr"):
            st.session_state.messages=[]; st.rerun()
        if st.button("🏠 Home", key="home"):
            new_session(); st.session_state.page="landing"; st.rerun()
 
    # ── HEADER ──────────────────────────────────────────────
    st.markdown("""
    <div class="chat-top">
      <div class="chat-logo">🦅 ORNIS IA</div>
      <div class="chat-sub">Professor-Level Ornithological Intelligence</div>
    </div>""", unsafe_allow_html=True)
 
    # ── MODE BUTTONS ────────────────────────────────────────
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("💬  Chat", use_container_width=True, key="m1"):
            st.session_state.mode="chat"; st.rerun()
    with c2:
        if st.button("🖼️  Image", use_container_width=True, key="m2"):
            st.session_state.mode="image"; st.rerun()
    with c3:
        if st.button("🎙️  Record", use_container_width=True, key="m3"):
            st.session_state.mode="audio"; st.rerun()
 
    lbl={"chat":"💬 Chat Mode","image":"🖼️ Image Analysis Mode","audio":"🎙️ Live Recording Mode"}
    st.markdown(f'<p style="text-align:center;color:rgba(212,175,55,.5);font-size:11px;letter-spacing:2px;margin:5px 0 10px">{lbl[st.session_state.mode]}</p>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
 
    # ── MESSAGES ────────────────────────────────────────────
    for m in st.session_state.messages:
        if m["role"]=="user":
            st.markdown(f'<div class="bubble-user">👤 {m["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bubble-bot">🦅 {m["content"]}<br><span class="src-badge">📚 Cornell Lab · eBird · BirdLife Int. · IUCN</span></div>', unsafe_allow_html=True)
 
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
 
    # ── IMAGE ───────────────────────────────────────────────
    if st.session_state.mode=="image":
        st.markdown('<div class="upload-card"><div class="upload-title">🖼️ &nbsp; Bird Image Analysis</div>', unsafe_allow_html=True)
        img = st.file_uploader("Upload a clear bird photo", type=["jpg","jpeg","png","webp"], key="iu")
        if img:
            col_i,_ = st.columns([1,2])
            with col_i: st.image(img, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if img and st.button("🔍  Identify Species", use_container_width=True, key="id_img"):
            with st.spinner("🔭 Professor Ornis is analyzing the image..."):
                res = analyze_image(img, lang)
                st.session_state.messages.append({"role":"user","content":"📸 [Bird image uploaded for identification]"})
                st.session_state.messages.append({"role":"model","content":res})
                st.rerun()
 
    # ── AUDIO ───────────────────────────────────────────────
    elif st.session_state.mode=="audio":
        if not st.session_state.location_ok:
            st.markdown('<div class="upload-card"><div class="step-pill">STEP 1 / 2</div><div class="upload-title">📍 Confirm Your Location</div>', unsafe_allow_html=True)
            st.markdown('<p style="color:rgba(255,255,255,.5);font-size:13px;margin-bottom:14px">BirdNET uses your GPS coordinates to improve accuracy — like Merlin.</p>', unsafe_allow_html=True)
            d={"العربية":(36.7,3.0),"English":(37.09,-95.71),"Français":(46.23,2.21)}
            ld,lnd=d[lang]
            cl,cn=st.columns(2)
            with cl: la=st.number_input("📍 Latitude", value=ld, format="%.4f")
            with cn: lo=st.number_input("📍 Longitude", value=lnd, format="%.4f")
            st.markdown('<p style="color:rgba(212,175,55,.35);font-size:11px;margin-top:6px">💡 Find at <a href="https://maps.google.com" target="_blank" style="color:#d4af37">maps.google.com</a> → right-click → "What\'s here?"</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            if st.button("📍  Confirm Location →", use_container_width=True):
                st.session_state.lat=la; st.session_state.lon=lo; st.session_state.location_ok=True; st.rerun()
        else:
            r1,r2=st.columns([5,1])
            with r1: st.markdown(f'<p style="color:rgba(212,175,55,.55);font-size:12px">📍 {st.session_state.lat:.3f}°, {st.session_state.lon:.3f}°</p>', unsafe_allow_html=True)
            with r2:
                if st.button("📍", key="chgloc"): st.session_state.location_ok=False; st.rerun()
 
            st.markdown('<div class="upload-card"><div class="step-pill">STEP 2 / 2</div><div class="upload-title">🎙️ Record Bird Sound</div>', unsafe_allow_html=True)
            st.markdown('<p style="color:rgba(255,255,255,.5);font-size:13px;margin-bottom:12px">Hold still, point toward the bird, record for at least 10 seconds.</p>', unsafe_allow_html=True)
            aud = st.audio_input("🎙️ Press to record")
            if aud: st.success("✅ Recording captured!")
            st.markdown('</div>', unsafe_allow_html=True)
            if aud and st.button("🎧  Analyze with BirdNET", use_container_width=True):
                with st.spinner("🔊 BirdNET analyzing — Professor Ornis preparing report..."):
                    ab = aud.read() if hasattr(aud,'read') else aud
                    res = analyze_audio(ab, st.session_state.lat, st.session_state.lon, lang)
                    st.session_state.messages.append({"role":"user","content":"🎙️ [Live bird recording]"})
                    st.session_state.messages.append({"role":"model","content":res})
                    st.rerun()
 
    # ── CHAT ────────────────────────────────────────────────
    else:
        ph={"العربية":"💬 اسأل البروفيسور Ornis عن أي طائر...","English":"💬 Ask Professor Ornis about any bird...","Français":"💬 Posez une question au Professeur Ornis..."}
        ui = st.chat_input(ph[lang])
        if ui:
            st.session_state.messages.append({"role":"user","content":ui})
            with st.spinner("🤔 Consulting ornithological literature..."):
                rep = chat_groq(ui, lang, st.session_state.messages[:-1])
            st.session_state.messages.append({"role":"model","content":rep})
            st.rerun()