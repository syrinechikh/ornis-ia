import streamlit as st
from groq import Groq
import base64, tempfile, os, uuid
from datetime import datetime
import streamlit.components.v1 as components
from history import load_all, save_session, delete_session, get_session
 
st.set_page_config(page_title="Ornis IA", page_icon="🦅", layout="wide", initial_sidebar_state="expanded")
 
# ═══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Cormorant+Garamond:wght@300;400;600&family=Tajawal:wght@300;400;700&display=swap');
html,body,.stApp{background:#04080f!important;}
.stApp::before{content:'';position:fixed;inset:0;z-index:0;pointer-events:none;
  background:radial-gradient(ellipse at 20% 50%,rgba(40,10,80,.5) 0%,transparent 55%),
  radial-gradient(ellipse at 80% 20%,rgba(10,30,80,.4) 0%,transparent 55%);}
 
/* ── SIDEBAR ── */
[data-testid="stSidebar"]{background:#060c1c!important;border-right:1px solid rgba(212,175,55,.12)!important;}
[data-testid="stSidebar"]>div{padding:0!important;}
.sb-wrap{padding:18px 14px 10px;}
.sb-logo{font-family:'Playfair Display',serif;font-size:19px;font-weight:900;letter-spacing:5px;
  background:linear-gradient(135deg,#ffd700,#d4af37,#8b6914);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;display:block;}
.sb-sub{font-size:9px;color:rgba(212,175,55,.35);letter-spacing:3px;font-family:'Cormorant Garamond',serif;}
.sb-div{height:1px;background:rgba(212,175,55,.1);margin:8px 0;}
.sb-lbl{font-size:9px;color:rgba(212,175,55,.38);letter-spacing:2px;text-transform:uppercase;padding:6px 4px 3px;}
.ch-row{padding:9px 10px;border-radius:7px;margin:2px 0;
  color:#9a8060;font-size:12px;border:1px solid transparent;transition:all .18s;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-family:'Tajawal',sans-serif;}
.ch-row:hover{background:rgba(212,175,55,.07);color:#d4af37;border-color:rgba(212,175,55,.15);}
.ch-row.on{background:rgba(212,175,55,.11);color:#ffd700;border-color:rgba(212,175,55,.26);}
.ch-date{font-size:9px;color:rgba(212,175,55,.22);padding:0 10px;margin-bottom:4px;}
 
/* ── LANDING ── */
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
.bsub{font-family:'Cormorant Garamond',serif;letter-spacing:10px;font-size:clamp(10px,1.4vw,13px);
  color:rgba(212,175,55,.58);margin-top:3px;animation:fi 1s ease-out 1.5s both;}
.ghr{width:240px;height:1px;background:linear-gradient(90deg,transparent,#d4af37,transparent);margin:18px auto;animation:fi 1s ease-out 2s both;}
.tgl{color:rgba(255,255,255,.6);font-size:clamp(13px,1.7vw,16px);line-height:1.85;max-width:520px;animation:fi 1s ease-out 2.2s both;}
@keyframes fi{0%{opacity:0;transform:translateY(14px)}100%{opacity:1;transform:translateY(0)}}
.pills{display:flex;gap:9px;flex-wrap:wrap;justify-content:center;margin:22px 0;animation:fi 1s ease-out 2.5s both;}
.pl{background:rgba(212,175,55,.07);border:1px solid rgba(212,175,55,.28);border-radius:40px;padding:7px 18px;color:#d4af37;font-size:12px;}
 
/* ── CHAT ── */
.chdr{text-align:center;padding:16px 0 5px;border-bottom:1px solid rgba(212,175,55,.1);margin-bottom:10px;position:relative;z-index:10;}
.clogo{font-family:'Playfair Display',serif;font-size:clamp(20px,3.5vw,36px);font-weight:900;letter-spacing:7px;
  background:linear-gradient(180deg,#ffd700,#d4af37,#8b6914);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.csub{font-family:'Cormorant Garamond',serif;color:rgba(212,175,55,.38);letter-spacing:4px;font-size:9px;}
.bu{background:linear-gradient(135deg,rgba(212,175,55,.12),rgba(212,175,55,.05));
  border:1px solid rgba(212,175,55,.26);border-radius:16px 16px 4px 16px;
  padding:13px 17px;margin:7px 0;color:#fde68a;font-family:'Tajawal',sans-serif;font-size:15px;position:relative;z-index:10;}
.bb{background:rgba(5,10,26,.93);border:1px solid rgba(212,175,55,.12);
  border-radius:16px 16px 16px 4px;padding:17px 20px;margin:7px 0;
  color:#e3e0d8;font-family:'Tajawal',sans-serif;font-size:15px;line-height:1.9;position:relative;z-index:10;backdrop-filter:blur(8px);}
.src-b{display:inline-flex;align-items:center;gap:4px;margin-top:9px;
  background:rgba(212,175,55,.06);border:1px solid rgba(212,175,55,.16);
  border-radius:20px;padding:3px 13px;font-size:10px;color:#9a7030;}
.card{position:relative;z-index:10;background:rgba(5,10,26,.88);
  border:1px solid rgba(212,175,55,.16);border-radius:12px;padding:18px;margin-bottom:12px;backdrop-filter:blur(7px);}
.ctitle{font-family:'Playfair Display',serif;color:#d4af37;font-size:16px;letter-spacing:2px;margin-bottom:10px;}
.div{height:1px;background:linear-gradient(90deg,transparent,rgba(212,175,55,.22),transparent);margin:10px 0;position:relative;z-index:10;}
 
/* ── BUTTONS ── */
.stButton>button{background:linear-gradient(135deg,#4a3500,#c49b20,#ffd700)!important;
  color:#050200!important;border:none!important;border-radius:28px!important;
  padding:10px 32px!important;font-family:'Playfair Display',serif!important;
  font-weight:700!important;font-size:13px!important;letter-spacing:1.5px!important;
  box-shadow:0 0 16px rgba(212,175,55,.2)!important;transition:all .3s!important;}
.stButton>button:hover{transform:scale(1.04)!important;box-shadow:0 0 28px rgba(212,175,55,.45)!important;}
 
/* ── UPLOADS ── */
[data-testid="stFileUploader"]{background:rgba(212,175,55,.03)!important;border:1.5px dashed rgba(212,175,55,.3)!important;border-radius:10px!important;}
[data-testid="stFileUploader"] label{color:#d4af37!important;}
[data-testid="stFileUploadDropzone"]{background:transparent!important;border:none!important;}
[data-testid="stFileUploadDropzone"] p{color:#7a6040!important;}
[data-testid="stFileUploadDropzone"] svg{fill:#d4af37!important;}
div[data-testid="stAudioInput"]{background:rgba(212,175,55,.03)!important;border:1.5px dashed rgba(212,175,55,.38)!important;border-radius:10px!important;}
.stChatInput textarea{background:rgba(5,10,28,.96)!important;border:1px solid rgba(212,175,55,.24)!important;color:#fde68a!important;border-radius:12px!important;}
.stTextInput input{background:rgba(5,10,28,.9)!important;border:1px solid rgba(212,175,55,.22)!important;color:#fde68a!important;border-radius:7px!important;}
label,.stRadio label,.stSelectbox label{color:#d4af37!important;}
.stExpander{border:1px solid rgba(212,175,55,.18)!important;border-radius:10px!important;background:rgba(5,10,26,.7)!important;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding:0!important;max-width:820px;}
section[data-testid="stMain"]>div{position:relative;z-index:10;}
</style>
""", unsafe_allow_html=True)
 
# ═══════════════════════════════════════════════════════════
client       = Groq(api_key=st.secrets["GROQ_API_KEY"])
CHAT_MODEL   = "llama-3.3-70b-versatile"
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
 
SYS = {
"العربية": """أنت البروفيسور Ornis — عالم أورنيثولوجيا من الدرجة الأولى، دكتوراه من Cornell University، مساهم في Handbook of the Birds of the World وBirdLife International، خبرة ميدانية 30+ عاماً في 6 قارات.

أسلوبك: علمي دقيق وعميق كالأستاذ الجامعي المتخصص. عمق الإجابة يتناسب مع السؤال.

للأسئلة عن نوع طائر، استخدم هذا الهيكل:
━━━━━━━━━━━━━━━━━━━━━━━━
🦅 **[الاسم العربي]** | *[Genus species]*
━━━━━━━━━━━━━━━━━━━━━━━━
**📌 التصنيف:** الرتبة | العائلة | الجنس | النوع
**🌍 الانتشار والهجرة:** ...
**🏔️ البيئة الإيكولوجية:** ...
**🎨 المورفولوجيا والتشخيص:** ...
**🔊 الأصوات:** ...
**🍃 الغذاء والسلوك:** ...
**🥚 التكاثر:** ...
**🔬 ملاحظات متخصصة:** ...
**⚠️ IUCN:** ...
━━━━━━━━━━━━━━━━━━━━━━━━
**📚 المراجع العلمية المعتمدة (استخدم الأنسب لكل معلومة):**

▸ قواعد بيانات أولية:
  • Cornell Lab of Ornithology — allaboutbirds.org
  • eBird Global Database — ebird.org
  • BirdLife International — birdlife.org/datazone
  • Avibase (Lepage, D.) — avibase.bsc-eoc.org
  • Macaulay Library (صوت وصورة) — macaulaylibrary.org
  • Birds of the World (Cornell/BirdLife) — birdsoftheworld.org
  • IUCN Red List — iucnredlist.org
  • Xeno-canto (تسجيلات صوتية) — xeno-canto.org
  • Biodiversity Heritage Library — biodiversitylibrary.org
  • SORA — Searchable Ornithological Research Archive — sora.unm.edu

▸ مجلات علمية محكّمة (اذكر الدراسة الأنسب):
  • The Auk / Ornithology (AOS) — academic.oup.com/ornithology
  • Ibis (BOU) — onlinelibrary.wiley.com/journal/1474919x
  • Journal of Ornithology (DO-G) — link.springer.com/journal/10336
  • The Condor: Ornithological Applications — academic.oup.com/condor
  • Emu – Austral Ornithology — tandfonline.com/journals/temu20
  • Current Ornithology (D.M. Power, ed.)
  • PubMed / NCBI — pubmed.ncbi.nlm.nih.gov

▸ مراجع أكاديمية شاملة:
  • Handbook of the Birds of the World (HBW Alive) — hbw.com
  • Ornithology — Frank Gill (4th ed., 2020)
  • ResearchGate — researchgate.net (للأبحاث)
  • Google Scholar — scholar.google.com

❌ محظور تماماً: Wikipedia، مواقع عامة، مدونات، مصادر غير محكّمة
⚠️ إذا لم تكن متأكداً من مصدر معين، صرّح بذلك بصدق.""",

"English": """You are Professor Ornis — world-class ornithologist, PhD Cornell University, HBW & BirdLife contributor, 30+ years field research across 6 continents.

Style: scientific depth matching the question's complexity. Write like a passionate academic expert.

For species questions use this structure:
━━━━━━━━━━━━━━━━━━━━━━━━
🦅 **[Common Name]** | *[Genus species]*
━━━━━━━━━━━━━━━━━━━━━━━━
**📌 Taxonomy | 🌍 Distribution & Migration | 🏔️ Ecology | 🎨 Morphology | 🔊 Vocalizations | 🍃 Diet & Behavior | 🥚 Breeding | 🔬 Specialist Notes | ⚠️ IUCN**
━━━━━━━━━━━━━━━━━━━━━━━━
**📚 Scientific References — cite the most appropriate per fact:**

▸ Primary Databases:
  • Cornell Lab / AllAboutBirds — allaboutbirds.org
  • eBird Global Database — ebird.org
  • BirdLife International — birdlife.org/datazone
  • Avibase (Lepage, D.) — avibase.bsc-eoc.org
  • Macaulay Library (audio/video) — macaulaylibrary.org
  • Birds of the World (Cornell/BirdLife) — birdsoftheworld.org
  • IUCN Red List — iucnredlist.org
  • Xeno-canto (recordings) — xeno-canto.org
  • Biodiversity Heritage Library — biodiversitylibrary.org
  • SORA – Searchable Ornithological Research Archive — sora.unm.edu

▸ Peer-Reviewed Journals (cite specific studies when relevant):
  • The Auk / Ornithology (AOS) — academic.oup.com/ornithology
  • Ibis (BOU) — onlinelibrary.wiley.com/journal/1474919x
  • Journal of Ornithology (DO-G) — link.springer.com/journal/10336
  • The Condor: Ornithological Applications — academic.oup.com/condor
  • Emu – Austral Ornithology — tandfonline.com/journals/temu20
  • Current Ornithology (Ed. D.M. Power)
  • PubMed / NCBI — pubmed.ncbi.nlm.nih.gov

▸ Reference Works:
  • Handbook of the Birds of the World (HBW Alive) — hbw.com
  • Ornithology — Frank Gill (4th ed., 2020)
  • ResearchGate — researchgate.net
  • Google Scholar — scholar.google.com

❌ NEVER cite: Wikipedia, general websites, blogs, non-peer-reviewed sources
⚠️ If uncertain about a specific source, say so honestly.""",

"Français": """Vous êtes le Professeur Ornis — ornithologue mondial, docteur Cornell, contributeur HBW & BirdLife, 30+ ans de terrain sur 6 continents.

Style: profondeur scientifique adaptée à la question. Rigueur académique et passion communicative.

Pour les espèces:
━━━━━━━━━━━━━━━━━━━━━━━━
🦅 **[Nom commun]** | *[Genre espèce]*
━━━━━━━━━━━━━━━━━━━━━━━━
**📌 Taxonomie · 🌍 Répartition · 🏔️ Habitat · 🎨 Morphologie · 🔊 Vocalisations · 🍃 Alimentation · 🥚 Reproduction · 🔬 Notes spécialisées · ⚠️ UICN**
━━━━━━━━━━━━━━━━━━━━━━━━
**📚 Références scientifiques — citez la plus appropriée par information:**

▸ Bases de données primaires:
  • Cornell Lab / AllAboutBirds — allaboutbirds.org
  • eBird — ebird.org
  • BirdLife International — birdlife.org/datazone
  • Avibase (Lepage, D.) — avibase.bsc-eoc.org
  • Macaulay Library (audio/vidéo) — macaulaylibrary.org
  • Birds of the World — birdsoftheworld.org
  • Liste rouge UICN — iucnredlist.org
  • Xeno-canto (enregistrements) — xeno-canto.org
  • Biodiversity Heritage Library — biodiversitylibrary.org
  • SORA – Searchable Ornithological Research Archive — sora.unm.edu

▸ Revues scientifiques à comité de lecture:
  • The Auk / Ornithology (AOS)
  • Ibis (BOU)
  • Journal of Ornithology (DO-G)
  • The Condor: Ornithological Applications
  • Emu – Austral Ornithology
  • Current Ornithology (Ed. D.M. Power)
  • PubMed / NCBI — pubmed.ncbi.nlm.nih.gov

▸ Ouvrages de référence:
  • HBW Alive — hbw.com
  • Ornithology — Frank Gill (4e éd., 2020)
  • ResearchGate — researchgate.net
  • Google Scholar — scholar.google.com

❌ JAMAIS: Wikipedia, sites généraux, blogs
⚠️ En cas d'incertitude sur une source, signalez-le honnêtement."""
}
 
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
        mime = "image/png" if img_file.name.lower().endswith("png") else "image/jpeg"
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
        return f"⚠️ Image error: {e}"
 
def transcribe(audio_bytes):
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio_bytes); tmp_path = tmp.name
        with open(tmp_path,"rb") as f:
            result = client.audio.transcriptions.create(
                model="whisper-large-v3", file=("audio.wav", f)
            )
        os.unlink(tmp_path)
        return result.text
    except Exception as e:
        return ""
 
def speak(text, lang):
    vl = {"العربية":"ar","English":"en-US","Français":"fr-FR"}.get(lang,"en-US")
    clean = text.replace('"',' ').replace("'"," ").replace("\n"," ")[:600]
    components.html(f"""<script>
const u=new SpeechSynthesisUtterance("{clean}");
u.lang="{vl}";u.rate=0.9;
window.speechSynthesis.cancel();
window.speechSynthesis.speak(u);
</script>""", height=0)
 
# ═══════════════════════════════════════════════════════════
#  SESSION INIT
# ═══════════════════════════════════════════════════════════
if "sid"      not in st.session_state: st.session_state.sid      = str(uuid.uuid4())[:8]
if "messages" not in st.session_state: st.session_state.messages = []
if "lang"     not in st.session_state: st.session_state.lang     = "العربية"
if "page"     not in st.session_state: st.session_state.page     = "landing"
if "show_img" not in st.session_state: st.session_state.show_img = False
if "speak_it" not in st.session_state: st.session_state.speak_it = False
if "search_q" not in st.session_state: st.session_state.search_q = ""
 
def commit():
    """Save current session to disk."""
    if st.session_state.messages:
        title = next((m["content"][:55] for m in st.session_state.messages if m["role"]=="user"), "Chat")
        save_session(st.session_state.sid, title, st.session_state.messages)
 
def new_chat():
    commit()
    st.session_state.messages = []
    st.session_state.sid      = str(uuid.uuid4())[:8]
    st.session_state.show_img = False
 
# ═══════════════════════════════════════════════════════════
#  LANDING
# ═══════════════════════════════════════════════════════════
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
        <div class="pl">🖼️ Bird Photo ID</div>
        <div class="pl">🎤 Voice Questions</div>
        <div class="pl">🔊 Voice Answers</div>
        <div class="pl">📚 Academic Sources</div>
        <div class="pl">🕓 Persistent History</div>
      </div>
    </div>""", unsafe_allow_html=True)
    c1,c2,c3 = st.columns([1,2,1])
    with c2:
        lg = st.selectbox("", ["العربية","English","Français"], label_visibility="collapsed")
        st.session_state.lang = lg
        if st.button("✦  Enter Ornis IA  ✦", use_container_width=True):
            st.session_state.page="chat"; st.rerun()
 
# ═══════════════════════════════════════════════════════════
#  CHAT PAGE
# ═══════════════════════════════════════════════════════════
else:
    lang = st.session_state.lang
 
    # ── SIDEBAR ─────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""<div class="sb-wrap">
          <span class="sb-logo">ORNIS IA</span>
          <span class="sb-sub">Ornithological Intelligence</span>
        </div>""", unsafe_allow_html=True)
 
        if st.button("＋  New Chat", use_container_width=True, key="new_btn"):
            new_chat(); st.rerun()
 
        st.markdown('<div class="sb-div"></div>', unsafe_allow_html=True)
 
        lg2 = st.selectbox("🌍 Language", ["العربية","English","Français"],
                           index=["العربية","English","Français"].index(lang), key="lang_sb")
        st.session_state.lang = lg2
 
        st.markdown('<div class="sb-div"></div>', unsafe_allow_html=True)
 
        # ── SEARCH ──
        st.text_input("", key="search_q", placeholder="🔍  Search conversations...",
                      label_visibility="collapsed")
        q = st.session_state.search_q.strip().lower()
 
        # ── HISTORY LIST (from disk) ──
        st.markdown('<div class="sb-lbl">🕓 Chat History</div>', unsafe_allow_html=True)
        all_sess = load_all()
        filtered = [s for s in all_sess if (not q or q in s["title"].lower())]
 
        if not filtered:
            st.markdown('<p style="color:rgba(212,175,55,.25);font-size:11px;padding:3px 10px">No history yet</p>', unsafe_allow_html=True)
 
        for s in filtered:
            is_on = s["id"] == st.session_state.sid
            cls   = "ch-row on" if is_on else "ch-row"
            st.markdown(f'<div class="{cls}">💬 {s["title"][:38]}</div>'
                        f'<div class="ch-date">{s["date"]}</div>', unsafe_allow_html=True)
 
            oc1, oc2 = st.columns([3,1])
            with oc1:
                if st.button("↗ Open", key=f"open_{s['id']}"):
                    commit()
                    loaded = get_session(s["id"])
                    if loaded:
                        st.session_state.messages = loaded["messages"]
                        st.session_state.sid      = s["id"]
                    st.rerun()
            with oc2:
                if st.button("🗑", key=f"del_{s['id']}"):
                    delete_session(s["id"])
                    if s["id"] == st.session_state.sid:
                        st.session_state.messages = []
                        st.session_state.sid      = str(uuid.uuid4())[:8]
                    st.rerun()
 
        st.markdown('<div class="sb-div"></div>', unsafe_allow_html=True)
        st.markdown("""<div style="padding:3px 8px;font-size:10px;color:#4a3f30;line-height:2.1">
📚 <b style="color:rgba(212,175,55,.4)">Sources</b><br>
🔬 Cornell Lab · 🐦 eBird<br>🌍 BirdLife Int.<br>📖 HBW · 🔴 IUCN · 🎵 Xeno-canto</div>""",
unsafe_allow_html=True)
 
        st.markdown('<div class="sb-div"></div>', unsafe_allow_html=True)
        sc1,sc2 = st.columns(2)
        with sc1:
            if st.button("🗑️ Clear", use_container_width=True, key="clr"):
                st.session_state.messages=[]; st.rerun()
        with sc2:
            if st.button("🏠 Home", use_container_width=True, key="hm"):
                commit(); st.session_state.page="landing"; st.rerun()
 
    # ── HEADER ──────────────────────────────────────────────
    st.markdown("""
    <div class="chdr">
      <div class="clogo">🦅 ORNIS IA</div>
      <div class="csub">Professor-Level Ornithological Intelligence</div>
    </div>""", unsafe_allow_html=True)
 
    # ── MESSAGES ────────────────────────────────────────────
    for m in st.session_state.messages:
        if m["role"]=="user":
            st.markdown(f'<div class="bu">👤 {m["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bb">🦅 {m["content"]}<br>'
                        f'<span class="src-b">📚 Cornell Lab · eBird · BirdLife · IUCN</span></div>',
                        unsafe_allow_html=True)
 
    # TTS trigger
    if st.session_state.speak_it:
        last = next((m["content"] for m in reversed(st.session_state.messages) if m["role"]=="model"), None)
        if last: speak(last, lang)
        st.session_state.speak_it = False
 
    st.markdown('<div class="div"></div>', unsafe_allow_html=True)
 
    # ── IMAGE PANEL ─────────────────────────────────────────
    if st.session_state.show_img:
        st.markdown('<div class="card"><div class="ctitle">🖼️  Bird Photo Identification</div>', unsafe_allow_html=True)
        img = st.file_uploader("Upload bird photo", type=["jpg","jpeg","png","webp"], key="img_up")
        if img:
            ci,_ = st.columns([1,2])
            with ci: st.image(img, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if img and st.button("🔍  Identify Species", use_container_width=True, key="id_img"):
            with st.spinner("🔭 Professor Ornis analyzing..."):
                res = analyze_image(img, lang)
                st.session_state.messages.append({"role":"user","content":"📸 [Bird photo submitted]"})
                st.session_state.messages.append({"role":"model","content":res})
                st.session_state.show_img = False
                commit()
                st.rerun()
 
    # ── VOICE INPUT ─────────────────────────────────────────
    with st.expander("🎤  Record question (voice)", expanded=False):
        aud = st.audio_input("🎤 Tap to record", key="voice_in")
        if aud and st.button("📝  Transcribe & Send", use_container_width=True, key="trans_btn"):
            with st.spinner("🎙️ Transcribing..."):
                ab   = aud.read() if hasattr(aud,"read") else bytes(aud)
                text = transcribe(ab)
            if text:
                st.session_state.messages.append({"role":"user","content":f"🎤 {text}"})
                with st.spinner("🤔 Professor Ornis thinking..."):
                    rep = chat_groq(text, lang, st.session_state.messages[:-1])
                st.session_state.messages.append({"role":"model","content":rep})
                commit()
                st.rerun()
            else:
                st.warning("Could not transcribe — please try again.")
 
    # ── BOTTOM BAR: ➕  chat_input  🔊 ─────────────────────
    b1, b2, b3 = st.columns([1, 10, 1])
    with b1:
        if st.button("➕", key="plus", help="Attach photo"):
            st.session_state.show_img = not st.session_state.show_img
            st.rerun()
    with b2:
        ph = {"العربية":"💬 اسأل البروفيسور Ornis...",
              "English":"💬 Ask Professor Ornis...",
              "Français":"💬 Posez votre question..."}
        user_input = st.chat_input(ph[lang])
    with b3:
        if st.button("🔊", key="tts", help="Read last answer"):
            st.session_state.speak_it = True
            st.rerun()
 
    if user_input:
        st.session_state.messages.append({"role":"user","content":user_input})
        with st.spinner("🤔 Consulting ornithological literature..."):
            rep = chat_groq(user_input, lang, st.session_state.messages[:-1])
        st.session_state.messages.append({"role":"model","content":rep})
        commit()   # ← save to disk immediately
        st.rerun()