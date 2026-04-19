import streamlit as st
from groq import Groq
import base64, tempfile, os, uuid, json
from datetime import datetime
import streamlit.components.v1 as components
 
st.set_page_config(page_title="Ornis IA", page_icon="🦅", layout="wide", initial_sidebar_state="expanded")
 
# ═══════════════════════════════════════════════════════════════
#  CSS
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Cormorant+Garamond:wght@300;400;600&family=Tajawal:wght@300;400;700&display=swap');
 
html,body,.stApp{background:#04080f!important;}
 
/* SPACE */
.stApp::before{content:'';position:fixed;inset:0;z-index:0;pointer-events:none;
  background:radial-gradient(ellipse at 20% 50%,rgba(40,10,80,.5) 0%,transparent 55%),
  radial-gradient(ellipse at 80% 20%,rgba(10,30,80,.4) 0%,transparent 55%);}
 
.star{position:fixed;border-radius:50%;background:#fff;pointer-events:none;z-index:0;
  animation:tw 4s ease-in-out infinite alternate;}
@keyframes tw{0%{opacity:.2}50%{opacity:.9}100%{opacity:.3}}
 
/* SIDEBAR */
[data-testid="stSidebar"]{background:#060c1c!important;border-right:1px solid rgba(212,175,55,.12)!important;}
[data-testid="stSidebar"]>div{padding:0!important;}
 
.sb-logo{font-family:'Playfair Display',serif;font-size:19px;font-weight:900;letter-spacing:5px;
  background:linear-gradient(135deg,#ffd700,#d4af37,#8b6914);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.sb-sub{font-size:9px;color:rgba(212,175,55,.35);letter-spacing:3px;font-family:'Cormorant Garamond',serif;}
.sb-div{height:1px;background:rgba(212,175,55,.1);margin:8px 0;}
.sb-lbl{font-size:9px;color:rgba(212,175,55,.38);letter-spacing:2px;text-transform:uppercase;padding:8px 4px 3px;}
 
.ch-row{padding:8px 10px;border-radius:7px;margin:2px 0;cursor:pointer;
  color:#9a8060;font-size:12px;border:1px solid transparent;transition:all .18s;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-family:'Tajawal',sans-serif;}
.ch-row:hover{background:rgba(212,175,55,.07);color:#d4af37;border-color:rgba(212,175,55,.15);}
.ch-row.on{background:rgba(212,175,55,.11);color:#ffd700;border-color:rgba(212,175,55,.26);}
.ch-date{font-size:9px;color:rgba(212,175,55,.25);padding:0 10px;margin-bottom:3px;}
 
/* MAIN */
.block-container{padding:0!important;max-width:820px;}
section[data-testid="stMain"]>div{position:relative;z-index:10;}
 
/* LANDING */
.land{position:relative;z-index:10;display:flex;flex-direction:column;align-items:center;
  justify-content:center;min-height:88vh;padding:50px 24px;text-align:center;}
.b-em{font-size:80px;animation:fl 5s ease-in-out infinite,gl 3s ease-in-out infinite alternate;margin-bottom:20px;}
@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-15px)}}
@keyframes gl{0%{filter:drop-shadow(0 0 14px rgba(212,175,55,.5))}100%{filter:drop-shadow(0 0 40px rgba(255,215,0,.9))}}
.brand{font-family:'Playfair Display',serif;font-size:clamp(50px,9vw,96px);font-weight:900;letter-spacing:12px;
  background:linear-gradient(180deg,#fffbe6 0%,#ffd700 15%,#d4af37 35%,#8b6914 50%,#d4af37 65%,#ffd700 80%,#c8960c 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  filter:drop-shadow(0 2px 26px rgba(212,175,55,.5));animation:bin 1.8s cubic-bezier(.23,1.01,.32,1) both;}
@keyframes bin{0%{opacity:0;transform:scale(.65) translateY(38px)}70%{opacity:1;transform:scale(1.04) translateY(-4px)}100%{opacity:1;transform:scale(1) translateY(0)}}
.bsub{font-family:'Cormorant Garamond',serif;letter-spacing:10px;font-size:clamp(10px,1.5vw,13px);
  color:rgba(212,175,55,.58);margin-top:3px;animation:fi 1s ease-out 1.5s both;}
.ghr{width:240px;height:1px;background:linear-gradient(90deg,transparent,#d4af37,transparent);margin:18px auto;animation:fi 1s ease-out 2s both;}
.tgl{color:rgba(255,255,255,.6);font-size:clamp(13px,1.7vw,16px);line-height:1.85;max-width:520px;animation:fi 1s ease-out 2.2s both;}
@keyframes fi{0%{opacity:0;transform:translateY(14px)}100%{opacity:1;transform:translateY(0)}}
.pills{display:flex;gap:9px;flex-wrap:wrap;justify-content:center;margin:22px 0;animation:fi 1s ease-out 2.5s both;}
.pl{background:rgba(212,175,55,.07);border:1px solid rgba(212,175,55,.28);border-radius:40px;padding:7px 18px;color:#d4af37;font-size:12px;}
 
/* CHAT HDR */
.chdr{text-align:center;padding:16px 0 5px;border-bottom:1px solid rgba(212,175,55,.1);margin-bottom:10px;position:relative;z-index:10;}
.clogo{font-family:'Playfair Display',serif;font-size:clamp(20px,3.5vw,36px);font-weight:900;letter-spacing:7px;
  background:linear-gradient(180deg,#ffd700,#d4af37,#8b6914);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.csub{font-family:'Cormorant Garamond',serif;color:rgba(212,175,55,.38);letter-spacing:4px;font-size:9px;}
 
/* BUBBLES */
.bu{background:linear-gradient(135deg,rgba(212,175,55,.12),rgba(212,175,55,.05));
  border:1px solid rgba(212,175,55,.26);border-radius:16px 16px 4px 16px;
  padding:13px 17px;margin:7px 0;color:#fde68a;font-family:'Tajawal',sans-serif;font-size:15px;
  position:relative;z-index:10;}
.bb{background:rgba(5,10,26,.93);border:1px solid rgba(212,175,55,.12);
  border-radius:16px 16px 16px 4px;padding:17px 20px;margin:7px 0;
  color:#e3e0d8;font-family:'Tajawal',sans-serif;font-size:15px;line-height:1.9;
  position:relative;z-index:10;backdrop-filter:blur(8px);}
.src{display:inline-flex;align-items:center;gap:4px;margin-top:9px;
  background:rgba(212,175,55,.06);border:1px solid rgba(212,175,55,.16);
  border-radius:20px;padding:3px 13px;font-size:10px;color:#9a7030;}
 
/* CARD */
.card{position:relative;z-index:10;background:rgba(5,10,26,.88);
  border:1px solid rgba(212,175,55,.16);border-radius:12px;padding:18px;
  margin-bottom:12px;backdrop-filter:blur(7px);}
.ctitle{font-family:'Playfair Display',serif;color:#d4af37;font-size:16px;letter-spacing:2px;margin-bottom:10px;}
 
.div{height:1px;background:linear-gradient(90deg,transparent,rgba(212,175,55,.22),transparent);margin:10px 0;position:relative;z-index:10;}
 
/* INPUT BAR */
.input-bar{position:relative;z-index:10;display:flex;align-items:center;gap:8px;
  padding:10px;background:rgba(5,10,26,.9);border:1px solid rgba(212,175,55,.18);
  border-radius:14px;margin-top:6px;}
 
/* STREAMLIT */
.stButton>button{background:linear-gradient(135deg,#4a3500,#c49b20,#ffd700)!important;
  color:#050200!important;border:none!important;border-radius:28px!important;
  padding:10px 32px!important;font-family:'Playfair Display',serif!important;
  font-weight:700!important;font-size:13px!important;letter-spacing:1.5px!important;
  box-shadow:0 0 16px rgba(212,175,55,.2)!important;transition:all .3s!important;}
.stButton>button:hover{transform:scale(1.04)!important;box-shadow:0 0 28px rgba(212,175,55,.45)!important;}
 
[data-testid="stFileUploader"]{background:rgba(212,175,55,.03)!important;
  border:1.5px dashed rgba(212,175,55,.3)!important;border-radius:10px!important;}
[data-testid="stFileUploader"] label{color:#d4af37!important;}
[data-testid="stFileUploadDropzone"]{background:transparent!important;border:none!important;}
[data-testid="stFileUploadDropzone"] p{color:#7a6040!important;}
[data-testid="stFileUploadDropzone"] svg{fill:#d4af37!important;}
 
div[data-testid="stAudioInput"]{background:rgba(212,175,55,.03)!important;
  border:1.5px dashed rgba(212,175,55,.38)!important;border-radius:10px!important;}
 
.stChatInput textarea{background:rgba(5,10,28,.96)!important;
  border:1px solid rgba(212,175,55,.24)!important;color:#fde68a!important;border-radius:12px!important;}
.stTextInput input{background:rgba(5,10,28,.9)!important;
  border:1px solid rgba(212,175,55,.22)!important;color:#fde68a!important;border-radius:7px!important;}
label,.stRadio label,.stSelectbox label{color:#d4af37!important;}
#MainMenu,footer,header{visibility:hidden;}
</style>
 
<!-- Stars -->
<script>
const s=[{t:'8%',l:'12%',sz:'2px',d:'0s'},{t:'5%',l:'62%',sz:'1.5px',d:'.5s'},{t:'22%',l:'80%',sz:'1px',d:'1s'},
{t:'40%',l:'5%',sz:'1.5px',d:'.3s'},{t:'35%',l:'70%',sz:'2px',d:'.7s'},{t:'55%',l:'28%',sz:'1px',d:'1.2s'},
{t:'70%',l:'50%',sz:'1.5px',d:'.9s'},{t:'80%',l:'15%',sz:'2px',d:'.4s'},{t:'85%',l:'75%',sz:'1px',d:'1.5s'},
{t:'14%',l:'45%',sz:'1px',d:'.6s'},{t:'60%',l:'90%',sz:'1.5px',d:'1.1s'},{t:'92%',l:'38%',sz:'2px',d:'.8s'}];
document.addEventListener('DOMContentLoaded',()=>{s.forEach(x=>{const e=document.createElement('div');
e.className='star';e.style.cssText=`top:${x.t};left:${x.l};width:${x.sz};height:${x.sz};animation-delay:${x.d}`;
document.body.appendChild(e);});});
</script>
""", unsafe_allow_html=True)
 
# ═══════════════════════════════════════════════════════════════
#  CLIENT
# ═══════════════════════════════════════════════════════════════
client       = Groq(api_key=st.secrets["GROQ_API_KEY"])
CHAT_MODEL   = "llama-3.3-70b-versatile"
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
 
# ═══════════════════════════════════════════════════════════════
#  PROFESSOR PROMPTS
# ═══════════════════════════════════════════════════════════════
SYS = {
"العربية": """أنت البروفيسور Ornis — عالم أورنيثولوجيا (علم الطيور) من الدرجة الأولى.
حاصل على الدكتوراه من Cornell University. مساهم في Handbook of the Birds of the World وBirdLife International. خبرة ميدانية تجاوزت 30 عاماً في 6 قارات.
 
**قواعد الأسلوب الأكاديمي:**
- تجيب بعقل العالم المتخصص وقلب المعلّم الشغوف
- كل سؤال له إجابة بمستوى عمقه: سؤال بسيط = إجابة وافية واضحة / سؤال عميق = تحليل أكاديمي معمّق
- ابدأ دائماً بأكثر نقطة علمية إثارة واهتماماً
- اذكر الاسم العلمي اللاتيني عند ذكر أي نوع
- اربط المعلومات ببعضها وابنِ السياق البيولوجي والبيئي
- اذكر تفاصيل لا يعرفها إلا المتخصصون
 
**هيكل الإجابة عند السؤال عن نوع طائر:**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🦅 **[الاسم العربي]** | *[Genus species]*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**📌 التصنيف:** الرتبة | العائلة | الجنس | النوع
**🌍 الانتشار والهجرة:** ...
**🏔️ البيئة الإيكولوجية:** ...
**🎨 المورفولوجيا:** ...
**🔊 الأصوات:** ...
**🍃 الغذاء والسلوك:** ...
**🥚 التكاثر:** ...
**🔬 ملاحظات متخصصة:** ...
**⚠️ IUCN:** ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**📚 المراجع:** Cornell Lab · eBird · BirdLife · HBW · IUCN · Xeno-canto
 
**للأسئلة العامة:** أجب بشكل منظم وعلمي دون استخدام الهيكل الكامل إذا لم يكن ضرورياً.
❌ لا تستخدم Wikipedia أو مصادر غير علمية.""",
 
"English": """You are Professor Ornis — a world-class ornithologist.
PhD from Cornell University. Contributor to HBW and BirdLife International. 30+ years of field research across 6 continents.
 
**Academic Style Rules:**
- Answer with a specialist's mind and passionate teacher's voice
- Depth matches the question: simple question = clear answer / deep question = full academic analysis
- Always start with the most scientifically fascinating point
- Always include Latin scientific names
- Include specialist-level details unknown to non-experts
 
**Species Answer Structure:**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🦅 **[Common Name]** | *[Genus species]*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**📌 Taxonomy:** Order | Family | Genus | Species
**🌍 Distribution & Migration:** ...
**🏔️ Ecological Habitat:** ...
**🎨 Morphology:** ...
**🔊 Vocalizations:** ...
**🍃 Diet & Behavior:** ...
**🥚 Breeding Biology:** ...
**🔬 Specialist Notes:** ...
**⚠️ IUCN Status:** ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**📚 References:** Cornell Lab · eBird · BirdLife · HBW · IUCN · Xeno-canto
 
**For general questions:** Answer in a structured, scientific way without the full template if not needed.
❌ NEVER cite Wikipedia or non-scientific sources.""",
 
"Français": """Vous êtes le Professeur Ornis — ornithologue de classe mondiale.
Docteur de Cornell University. Contributeur au HBW et BirdLife International. 30+ ans de terrain sur 6 continents.
 
**Style académique:**
- Répondez avec la rigueur d'un spécialiste et la passion d'un enseignant
- Profondeur adaptée à la question
- Nom scientifique latin toujours inclus
- Détails que seuls les spécialistes connaissent
 
**Structure pour une espèce:**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🦅 **[Nom commun]** | *[Genre espèce]*
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**📌 Taxonomie · 🌍 Répartition · 🏔️ Habitat · 🎨 Morphologie · 🔊 Vocalisations · 🍃 Alimentation · 🥚 Reproduction · 🔬 Notes spécialisées · ⚠️ UICN**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**📚 Références:** Cornell Lab · eBird · BirdLife · HBW · UICN · Xeno-canto
❌ JAMAIS Wikipedia."""
}
 
IMG_P = {
"العربية": """أنت البروفيسور Ornis. شاهد هذه الصورة وقدم تشخيصاً ميدانياً متخصصاً:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 **التشخيص الميداني المتخصص**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🦅 **الاسم العربي:** | ***Genus species***
📌 **التصنيف:** الرتبة | العائلة | الجنس
 
🎨 **السمات التشخيصية في هذه الصورة:**
[صف بدقة: ألوان الريش، شكل المنقار، الحجم، الوضعية، لون العين، نمط الأجنحة]
 
🔍 **التمييز عن الأنواع المشابهة:** [لماذا هذا النوع تحديداً؟]
🌍 **الموطن:** | ⚠️ **IUCN:** | 📚 **المصدر:** Cornell Lab · eBird · BirdLife
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ **ثقة التشخيص:** [عالية جداً/عالية/متوسطة/منخفضة] — **السبب:**""",
 
"English": """You are Professor Ornis. Examine this image with specialist ornithologist eyes:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 **Specialist Field Identification**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🦅 **Common Name:** | ***Genus species***
📌 **Taxonomy:** Order | Family | Genus
 
🎨 **Diagnostic features visible in THIS image:**
[Describe precisely: plumage, bill morphology, size, posture, eye color, wing pattern]
 
🔍 **Separation from similar species:** [Why this species specifically?]
🌍 **Habitat:** | ⚠️ **IUCN:** | 📚 **Source:** Cornell Lab · eBird · BirdLife
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ **ID Confidence:** [Very High/High/Medium/Low] — **Rationale:**""",
 
"Français": """Vous êtes le Professeur Ornis. Examinez cette image en spécialiste:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 **Identification de terrain spécialisée**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🦅 **Nom commun:** | ***Genre espèce***
📌 **Taxonomie:** Ordre | Famille | Genre
🎨 **Caractéristiques diagnostiques:** [Plumage, bec, taille, posture]
🔍 **Séparation espèces similaires:**
🌍 **Habitat:** | ⚠️ **UICN:** | 📚 **Source:** Cornell Lab · eBird · BirdLife
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ **Confiance:** [Très élevée/Élevée/Moyenne/Faible] — **Justification:**"""
}
 
# ═══════════════════════════════════════════════════════════════
#  CORE FUNCTIONS
# ═══════════════════════════════════════════════════════════════
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
 
def transcribe(audio_bytes):
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio_bytes); tmp_path = tmp.name
        with open(tmp_path,"rb") as f:
            result = client.audio.transcriptions.create(
                model="whisper-large-v3", file=("audio.wav",f), language="ar"
            )
        os.unlink(tmp_path)
        return result.text
    except Exception as e:
        return f"[transcription error: {e}]"
 
def tts_js(text, lang):
    """Inject browser TTS"""
    voice_lang = {"العربية":"ar","English":"en-US","Français":"fr-FR"}
    clean = text.replace('"',' ').replace("'", " ").replace("\n"," ")[:500]
    js = f"""
    <script>
    const u = new SpeechSynthesisUtterance("{clean}");
    u.lang = "{voice_lang.get(lang,'en-US')}";
    u.rate = 0.92; u.pitch = 1;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(u);
    </script>"""
    components.html(js, height=0)
 
# ═══════════════════════════════════════════════════════════════
#  SESSION HELPERS
# ═══════════════════════════════════════════════════════════════
def save_and_new():
    if st.session_state.messages:
        title = next((m["content"][:50] for m in st.session_state.messages if m["role"]=="user"), "Chat")
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
    st.session_state.show_img = False
 
def load_sess(sid):
    s = next((x for x in st.session_state.sessions if x["id"]==sid), None)
    if s:
        st.session_state.messages = s["msgs"].copy()
        st.session_state.sid = sid
        st.session_state.active = sid
 
# ═══════════════════════════════════════════════════════════════
#  STATE INIT
# ═══════════════════════════════════════════════════════════════
D = {"page":"landing","messages":[],"lang":"العربية","sessions":[],
     "sid":str(uuid.uuid4())[:8],"active":None,"show_img":False,
     "search_q":"","pending_text":"","speak_last":False}
for k,v in D.items():
    if k not in st.session_state: st.session_state[k]=v
 
# ═══════════════════════════════════════════════════════════════
#  LANDING
# ═══════════════════════════════════════════════════════════════
if st.session_state.page == "landing":
    st.markdown("""
    <div class="land">
      <div class="b-em">🦅</div>
      <div class="brand">ORNIS</div>
      <div class="bsub">INTELLIGENCE ARTIFICIELLE ORNITHOLOGIQUE</div>
      <div class="ghr"></div>
      <div class="tgl">
        منصة ذكاء اصطناعي أكاديمية — مستوى بروفيسور متخصص<br>
        تحليل الصور · أسئلة بالصوت · إجابات علمية موثّقة<br>
        <span style="font-size:11px;opacity:.38;font-family:'Cormorant Garamond',serif;letter-spacing:2px">
          Cornell Lab · eBird · BirdLife International · IUCN
        </span>
      </div>
      <div class="pills">
        <div class="pl">🖼️ Bird ID from Photo</div>
        <div class="pl">🎤 Voice Questions</div>
        <div class="pl">🔊 Voice Answers</div>
        <div class="pl">📚 Academic Sources</div>
        <div class="pl">🕓 Chat History</div>
      </div>
    </div>""", unsafe_allow_html=True)
    c1,c2,c3 = st.columns([1,2,1])
    with c2:
        lg = st.selectbox("", ["العربية","English","Français"], label_visibility="collapsed")
        st.session_state.lang = lg
        if st.button("✦  Enter Ornis IA  ✦", use_container_width=True):
            st.session_state.page="chat"; st.rerun()
 
# ═══════════════════════════════════════════════════════════════
#  CHAT PAGE
# ═══════════════════════════════════════════════════════════════
else:
    lang = st.session_state.lang
 
    # ── SIDEBAR ──────────────────────────────────────────────
    with st.sidebar:
        st.markdown(f"""
        <div style="padding:18px 14px 10px">
          <div class="sb-logo">ORNIS IA</div>
          <div class="sb-sub">Ornithological Intelligence</div>
        </div>""", unsafe_allow_html=True)
 
        if st.button("＋  New Chat", use_container_width=True, key="new_btn"):
            save_and_new(); st.rerun()
 
        st.markdown('<div class="sb-div"></div>', unsafe_allow_html=True)
 
        # Language
        lg2 = st.selectbox("🌍 Language", ["العربية","English","Français"],
                           index=["العربية","English","Français"].index(lang), key="lang_sb")
        st.session_state.lang = lg2
 
        st.markdown('<div class="sb-div"></div>', unsafe_allow_html=True)
 
        # Search
        st.text_input("", key="search_q", placeholder="🔍 Search conversations...", label_visibility="collapsed")
        q = st.session_state.search_q.strip().lower()
 
        # History
        st.markdown('<div class="sb-lbl">🕓 Chat History</div>', unsafe_allow_html=True)
        sess_list = [s for s in st.session_state.sessions if (not q or q in s["title"].lower())]
 
        if not sess_list:
            st.markdown('<p style="color:rgba(212,175,55,.25);font-size:11px;padding:3px 10px">No history yet</p>', unsafe_allow_html=True)
        for s in sess_list:
            is_on = s["id"] == st.session_state.active
            cls = "ch-row on" if is_on else "ch-row"
            st.markdown(f'<div class="{cls}">💬 {s["title"][:36]}...</div><div class="ch-date">{s["date"]}</div>', unsafe_allow_html=True)
            if st.button("Open →", key=f"o_{s['id']}"):
                load_sess(s["id"]); st.rerun()
 
        st.markdown('<div class="sb-div"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sb-lbl">📚 Sources</div>', unsafe_allow_html=True)
        st.markdown("""<div style="padding:3px 10px;font-size:10px;color:#4a3f30;line-height:2.2">
🔬 Cornell Lab · 🐦 eBird<br>🌍 BirdLife International<br>📖 HBW Alive · 🔴 IUCN<br>🎵 Xeno-canto</div>""",
unsafe_allow_html=True)
 
        st.markdown('<div class="sb-div"></div>', unsafe_allow_html=True)
        sc1, sc2 = st.columns(2)
        with sc1:
            if st.button("🗑️ Clear", use_container_width=True, key="clr"):
                st.session_state.messages=[]; st.rerun()
        with sc2:
            if st.button("🏠 Home", use_container_width=True, key="hm"):
                save_and_new(); st.session_state.page="landing"; st.rerun()
 
    # ── HEADER ───────────────────────────────────────────────
    st.markdown("""
    <div class="chdr">
      <div class="clogo">🦅 ORNIS IA</div>
      <div class="csub">Professor-Level Ornithological Intelligence</div>
    </div>""", unsafe_allow_html=True)
 
    # ── MESSAGES ─────────────────────────────────────────────
    for i, m in enumerate(st.session_state.messages):
        if m["role"] == "user":
            st.markdown(f'<div class="bu">👤 {m["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bb">🦅 {m["content"]}<br><span class="src">📚 Cornell Lab · eBird · BirdLife · IUCN</span></div>', unsafe_allow_html=True)
 
    # TTS for last bot message
    if st.session_state.get("speak_last") and st.session_state.messages:
        last_bot = next((m["content"] for m in reversed(st.session_state.messages) if m["role"]=="model"), None)
        if last_bot:
            tts_js(last_bot, lang)
        st.session_state.speak_last = False
 
    st.markdown('<div class="div"></div>', unsafe_allow_html=True)
 
    # ── IMAGE UPLOAD PANEL (toggle) ──────────────────────────
    if st.session_state.show_img:
        st.markdown('<div class="card"><div class="ctitle">🖼️ &nbsp; Bird Photo Analysis</div>', unsafe_allow_html=True)
        img = st.file_uploader("Upload bird photo", type=["jpg","jpeg","png","webp"], key="img_up")
        if img:
            ci,_ = st.columns([1,2])
            with ci: st.image(img, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if img and st.button("🔍  Identify Species", use_container_width=True, key="id_img"):
            with st.spinner("🔭 Professor Ornis analyzing..."):
                res = analyze_image(img, lang)
                st.session_state.messages.append({"role":"user","content":"📸 [Bird photo submitted for identification]"})
                st.session_state.messages.append({"role":"model","content":res})
                st.session_state.show_img = False
                st.rerun()
 
    # ── VOICE INPUT PANEL ────────────────────────────────────
    with st.expander("🎤 Record your question", expanded=False):
        st.markdown('<p style="color:rgba(212,175,55,.5);font-size:12px">Record your question — it will be transcribed automatically.</p>', unsafe_allow_html=True)
        aud = st.audio_input("🎤 Hold to record", key="voice_in")
        if aud and st.button("📝  Transcribe & Send", use_container_width=True, key="transcribe_btn"):
            with st.spinner("🎙️ Transcribing..."):
                ab = aud.read() if hasattr(aud,"read") else bytes(aud)
                text = transcribe(ab)
            if text and not text.startswith("[transcription"):
                st.session_state.messages.append({"role":"user","content":f"🎤 {text}"})
                with st.spinner("🤔 Professor Ornis is thinking..."):
                    rep = chat_groq(text, lang, st.session_state.messages[:-1])
                st.session_state.messages.append({"role":"model","content":rep})
                st.rerun()
            else:
                st.warning("Could not transcribe. Please try again.")
 
    # ── BOTTOM INPUT BAR ─────────────────────────────────────
    bar_c1, bar_c2, bar_c3 = st.columns([1, 10, 1])
 
    with bar_c1:
        # + button to toggle image upload
        if st.button("➕", key="plus_btn", help="Attach bird photo"):
            st.session_state.show_img = not st.session_state.show_img
            st.rerun()
 
    with bar_c2:
        ph = {"العربية":"💬 اسأل البروفيسور Ornis عن أي طائر...",
              "English":"💬 Ask Professor Ornis about any bird...",
              "Français":"💬 Posez une question au Professeur Ornis..."}
        user_input = st.chat_input(ph[lang])
 
    with bar_c3:
        if st.button("🔊", key="tts_btn", help="Read last answer aloud"):
            st.session_state.speak_last = True
            st.rerun()
 
    # Process chat input
    if user_input:
        st.session_state.messages.append({"role":"user","content":user_input})
        with st.spinner("🤔 Consulting ornithological literature..."):
            rep = chat_groq(user_input, lang, st.session_state.messages[:-1])
        st.session_state.messages.append({"role":"model","content":rep})
        st.rerun()