import streamlit as st
from groq import Groq
import base64, tempfile, os, uuid
from datetime import datetime
 
st.set_page_config(page_title="Ornis IA", page_icon="🦅", layout="wide", initial_sidebar_state="collapsed")
 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Cormorant+Garamond:wght@300;400;600;700&family=Tajawal:wght@300;400;700&display=swap');
*{box-sizing:border-box;margin:0;padding:0;}
.stApp{background:#04080f;font-family:'Tajawal',serif;}
.space-bg{position:fixed;inset:0;z-index:0;pointer-events:none;
background:radial-gradient(ellipse at 15% 40%,rgba(40,10,80,.6) 0%,transparent 55%),
radial-gradient(ellipse at 85% 15%,rgba(10,30,80,.5) 0%,transparent 55%),
radial-gradient(ellipse at 50% 90%,rgba(60,15,10,.3) 0%,transparent 50%),#04080f;}
.stars-a{position:fixed;inset:0;z-index:0;pointer-events:none;
background-image:radial-gradient(1.5px 1.5px at 8% 12%,#fff 0%,transparent 100%),
radial-gradient(1px 1px at 22% 5%,rgba(255,255,255,.8) 0%,transparent 100%),
radial-gradient(2px 2px at 37% 22%,#fff 0%,transparent 100%),
radial-gradient(1px 1px at 53% 8%,rgba(255,220,150,.9) 0%,transparent 100%),
radial-gradient(1.5px 1.5px at 68% 18%,#fff 0%,transparent 100%),
radial-gradient(2px 2px at 91% 30%,#fff 0%,transparent 100%),
radial-gradient(1px 1px at 14% 45%,rgba(255,255,255,.6) 0%,transparent 100%),
radial-gradient(1.5px 1.5px at 28% 55%,#fff 0%,transparent 100%),
radial-gradient(2px 2px at 59% 62%,#fff 0%,transparent 100%),
radial-gradient(1px 1px at 74% 50%,rgba(200,210,255,.8) 0%,transparent 100%),
radial-gradient(2px 2px at 20% 80%,#fff 0%,transparent 100%),
radial-gradient(1px 1px at 65% 85%,rgba(180,200,255,.7) 0%,transparent 100%),
radial-gradient(2px 2px at 79% 78%,#fff 0%,transparent 100%),
radial-gradient(1px 1px at 94% 68%,rgba(255,255,255,.5) 0%,transparent 100%);
animation:twinkle 5s ease-in-out infinite alternate;}
.stars-b{position:fixed;inset:0;z-index:0;pointer-events:none;
background-image:radial-gradient(1px 1px at 11% 28%,rgba(255,255,255,.5) 0%,transparent 100%),
radial-gradient(1.5px 1.5px at 26% 15%,#fff 0%,transparent 100%),
radial-gradient(1px 1px at 41% 35%,rgba(255,230,160,.6) 0%,transparent 100%),
radial-gradient(2px 2px at 57% 42%,rgba(255,255,255,.8) 0%,transparent 100%),
radial-gradient(1.5px 1.5px at 87% 58%,#fff 0%,transparent 100%),
radial-gradient(2px 2px at 18% 70%,#fff 0%,transparent 100%),
radial-gradient(1.5px 1.5px at 48% 92%,#fff 0%,transparent 100%),
radial-gradient(2px 2px at 77% 88%,rgba(180,200,255,.6) 0%,transparent 100%);
animation:twinkle 7s ease-in-out infinite alternate-reverse;}
@keyframes twinkle{0%{opacity:.5}50%{opacity:1}100%{opacity:.6}}
 
/* LANDING */
.landing-wrap{position:relative;z-index:10;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:90vh;padding:60px 20px 40px;text-align:center;}
.bird-icon{font-size:90px;line-height:1;animation:float 5s ease-in-out infinite,glow-bird 3s ease-in-out infinite alternate;margin-bottom:30px;}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-18px)}}
@keyframes glow-bird{0%{filter:drop-shadow(0 0 15px rgba(212,175,55,.5))}100%{filter:drop-shadow(0 0 45px rgba(255,215,0,.9)) drop-shadow(0 0 70px rgba(212,175,55,.4))}}
.brand-title{font-family:'Playfair Display',serif;font-size:clamp(56px,10vw,110px);font-weight:900;letter-spacing:12px;line-height:1;
background:linear-gradient(180deg,#fffbe6 0%,#ffd700 15%,#d4af37 35%,#8b6914 50%,#d4af37 65%,#ffd700 80%,#c8960c 100%);
-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
filter:drop-shadow(0 2px 30px rgba(212,175,55,.6));animation:title-in 1.8s cubic-bezier(.23,1.01,.32,1) forwards;opacity:0;}
@keyframes title-in{0%{opacity:0;transform:scale(.6) translateY(40px)}70%{opacity:1;transform:scale(1.04) translateY(-6px)}100%{opacity:1;transform:scale(1) translateY(0)}}
.brand-ia{font-family:'Cormorant Garamond',serif;font-size:clamp(11px,2vw,16px);font-weight:300;letter-spacing:12px;color:rgba(212,175,55,.7);margin-top:6px;animation:fade-up 1s ease-out 1.5s forwards;opacity:0;text-transform:uppercase;}
.gold-line{width:280px;height:1px;background:linear-gradient(90deg,transparent,#d4af37,#ffd700,#d4af37,transparent);margin:24px auto;animation:fade-up 1s ease-out 2s forwards;opacity:0;}
.tagline{font-family:'Tajawal',sans-serif;color:rgba(255,255,255,.65);font-size:clamp(14px,2vw,18px);line-height:1.8;max-width:560px;animation:fade-up 1s ease-out 2.2s forwards;opacity:0;}
@keyframes fade-up{0%{opacity:0;transform:translateY(20px)}100%{opacity:1;transform:translateY(0)}}
.features-row{display:flex;gap:12px;flex-wrap:wrap;justify-content:center;margin:30px 0;animation:fade-up 1s ease-out 2.6s forwards;opacity:0;}
.feat-pill{background:rgba(212,175,55,.08);border:1px solid rgba(212,175,55,.35);border-radius:40px;padding:9px 22px;color:#d4af37;font-family:'Tajawal',sans-serif;font-size:13px;}
 
/* CHAT */
.chat-top{position:relative;z-index:10;text-align:center;padding:20px 0 8px;border-bottom:1px solid rgba(212,175,55,.15);margin-bottom:14px;}
.chat-logo{font-family:'Playfair Display',serif;font-size:clamp(26px,5vw,44px);font-weight:900;letter-spacing:8px;
background:linear-gradient(180deg,#ffd700 0%,#d4af37 50%,#8b6914 100%);
-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;filter:drop-shadow(0 0 12px rgba(212,175,55,.5));}
.chat-sub{font-family:'Cormorant Garamond',serif;color:rgba(212,175,55,.5);letter-spacing:5px;font-size:11px;text-transform:uppercase;margin-top:4px;}
 
.bubble-user{background:linear-gradient(135deg,rgba(212,175,55,.15),rgba(212,175,55,.07));border:1px solid rgba(212,175,55,.35);border-radius:18px 18px 4px 18px;padding:14px 20px;margin:8px 0;color:#fde68a;font-family:'Tajawal',sans-serif;font-size:15px;position:relative;z-index:10;}
.bubble-bot{background:rgba(8,14,35,.88);border:1px solid rgba(212,175,55,.18);border-radius:18px 18px 18px 4px;padding:18px 22px;margin:8px 0;color:#e8e6e0;font-family:'Tajawal',sans-serif;font-size:15px;line-height:1.85;position:relative;z-index:10;backdrop-filter:blur(12px);}
.src-badge{display:inline-flex;align-items:center;gap:6px;margin-top:10px;background:rgba(212,175,55,.08);border:1px solid rgba(212,175,55,.25);border-radius:20px;padding:4px 14px;font-size:11px;color:#d4af37;letter-spacing:.5px;}
 
.upload-card{position:relative;z-index:10;background:rgba(8,14,35,.75);border:1px solid rgba(212,175,55,.25);border-radius:14px;padding:24px;margin-bottom:18px;backdrop-filter:blur(10px);}
.upload-card-title{font-family:'Playfair Display',serif;color:#d4af37;font-size:18px;letter-spacing:3px;margin-bottom:16px;}
 
.step-badge{display:inline-block;background:rgba(212,175,55,.15);border:1px solid rgba(212,175,55,.4);border-radius:20px;padding:4px 16px;color:#d4af37;font-size:12px;letter-spacing:2px;margin-bottom:10px;}
 
.hist-item{background:rgba(212,175,55,.06);border:1px solid rgba(212,175,55,.2);border-radius:10px;padding:10px 14px;margin-bottom:8px;cursor:pointer;color:#c8a96e;font-size:12px;font-family:'Tajawal',sans-serif;transition:all .2s;}
.hist-item:hover{background:rgba(212,175,55,.12);border-color:rgba(212,175,55,.4);}
.hist-date{color:rgba(212,175,55,.4);font-size:10px;margin-top:3px;}
 
/* Streamlit overrides */
.stButton > button{background:linear-gradient(135deg,#6b4f00,#d4af37,#ffd700,#d4af37)!important;color:#0a0600!important;border:none!important;border-radius:40px!important;padding:12px 40px!important;font-family:'Playfair Display',serif!important;font-weight:700!important;font-size:14px!important;letter-spacing:2px!important;box-shadow:0 0 25px rgba(212,175,55,.3)!important;transition:all .3s!important;}
.stButton > button:hover{transform:scale(1.05)!important;box-shadow:0 0 40px rgba(212,175,55,.6)!important;}
[data-testid="stFileUploader"]{background:rgba(212,175,55,.04)!important;border:1.5px dashed rgba(212,175,55,.4)!important;border-radius:12px!important;padding:6px!important;}
[data-testid="stFileUploader"] label{color:#d4af37!important;}
[data-testid="stFileUploadDropzone"]{background:transparent!important;border:none!important;}
[data-testid="stFileUploadDropzone"] p{color:#a0896a!important;}
[data-testid="stFileUploadDropzone"] svg{fill:#d4af37!important;}
[data-testid="stSidebar"]{background:rgba(4,8,15,.97)!important;border-right:1px solid rgba(212,175,55,.15)!important;}
label,.stRadio label,.stSelectbox label{color:#d4af37!important;}
.stChatInput textarea{background:rgba(10,16,40,.9)!important;border:1px solid rgba(212,175,55,.3)!important;color:#fde68a!important;border-radius:12px!important;}
.stNumberInput input{background:rgba(10,16,40,.9)!important;border:1px solid rgba(212,175,55,.3)!important;color:#fde68a!important;border-radius:8px!important;}
div[data-testid="stAudioInput"]{background:rgba(212,175,55,.04)!important;border:1.5px dashed rgba(212,175,55,.5)!important;border-radius:12px!important;}
.divider{height:1px;background:linear-gradient(90deg,transparent,#d4af37,transparent);margin:14px 0;position:relative;z-index:10;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding-top:0!important;max-width:900px;}
section[data-testid="stMain"]>div{position:relative;z-index:10;}
</style>
<div class="space-bg"></div><div class="stars-a"></div><div class="stars-b"></div>
""", unsafe_allow_html=True)
 
# ── CLIENTS ──────────────────────────────────────────────────
groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
CHAT_MODEL   = "llama-3.3-70b-versatile"
VISION_MODEL = "llama-3.2-11b-vision-preview"
 
# ── PROMPTS ───────────────────────────────────────────────────
SYS = {
"العربية":"""أنت Ornis IA — ذكاء اصطناعي أورنيثولوجي أكاديمي متخصص.
قواعد صارمة:
1. أجب بالعربية الفصحى دائماً
2. اذكر الاسم العلمي اللاتيني لكل طائر
3. هيكل كل إجابة:
━━━━━━━━━━━━━━━━━━━━━━
🦅 [الاسم العربي] | [Scientific Name]
━━━━━━━━━━━━━━━━━━━━━━
📌 التصنيف: الرتبة ← العائلة ← الجنس ← النوع
🌍 الانتشار الجغرافي: ...
🏔️ البيئة والموطن: ...
🎨 الوصف المورفولوجي: ...
🔊 الصوت: ...
🍃 الغذاء والسلوك: ...
🥚 التكاثر: ...
⚠️ الحالة (IUCN): ...
━━━━━━━━━━━━━━━━━━━━━━
📚 المصادر: Cornell Lab · eBird · BirdLife International · IUCN
4. ❌ محظور: Wikipedia أو مصادر غير علمية""",
 
"English":"""You are Ornis IA — academic-level ornithological AI.
Rules:
1. Always answer in English
2. Always include Latin scientific name
3. Structure every answer:
━━━━━━━━━━━━━━━━━━━━━━
🦅 [Common Name] | [Scientific Name]
━━━━━━━━━━━━━━━━━━━━━━
📌 Taxonomy: Order → Family → Genus → Species
🌍 Geographic Range: ...
🏔️ Habitat & Ecology: ...
🎨 Morphological Description: ...
🔊 Vocalizations: ...
🍃 Diet & Behavior: ...
🥚 Reproduction: ...
⚠️ IUCN Status: ...
━━━━━━━━━━━━━━━━━━━━━━
📚 Sources: Cornell Lab · eBird · BirdLife International · IUCN
4. ❌ NEVER use Wikipedia or non-scientific sources""",
 
"Français":"""Vous êtes Ornis IA — expert IA en ornithologie académique.
Règles:
1. Répondez toujours en français
2. Toujours le nom scientifique latin
3. Structure obligatoire:
━━━━━━━━━━━━━━━━━━━━━━
🦅 [Nom commun] | [Nom scientifique]
━━━━━━━━━━━━━━━━━━━━━━
📌 Taxonomie: Ordre → Famille → Genre → Espèce
🌍 Répartition: ...
🏔️ Habitat & Écologie: ...
🎨 Morphologie: ...
🔊 Vocalisations: ...
🍃 Alimentation & Comportement: ...
🥚 Reproduction: ...
⚠️ Statut UICN: ...
━━━━━━━━━━━━━━━━━━━━━━
📚 Sources: Cornell Lab · eBird · BirdLife International · UICN
4. ❌ JAMAIS Wikipedia ou sources non-scientifiques"""
}
 
IMG_P = {
"العربية":"""حلّل هذه الصورة وحدد الطائر بدقة علمية تامة:
━━━━━━━━━━━━━━━━━━━━━━
🔍 نتيجة التعرف
━━━━━━━━━━━━━━━━━━━━━━
🦅 الاسم العربي: | الاسم العلمي:
📌 التصنيف: الرتبة ← العائلة ← الجنس
🎨 المميزات التشخيصية في الصورة:
🌍 الموطن الطبيعي:
⚠️ حالة الحفاظ (IUCN):
📚 المصدر: Cornell Lab / eBird / BirdLife International
━━━━━━━━━━━━━━━━━━━━━━
⚠️ مستوى الثقة: [عالٍ/متوسط/منخفض] + السبب""",
"English":"""Analyze this image. Identify the bird with full scientific precision:
━━━━━━━━━━━━━━━━━━━━━━
🔍 Identification Result
━━━━━━━━━━━━━━━━━━━━━━
🦅 Common Name: | Scientific Name:
📌 Taxonomy: Order → Family → Genus
🎨 Diagnostic features visible in image:
🌍 Natural habitat:
⚠️ IUCN status:
📚 Source: Cornell Lab / eBird / BirdLife International
━━━━━━━━━━━━━━━━━━━━━━
⚠️ Confidence: [High/Medium/Low] + reason""",
"Français":"""Analysez cette image et identifiez l'oiseau:
━━━━━━━━━━━━━━━━━━━━━━
🔍 Résultat d'identification
━━━━━━━━━━━━━━━━━━━━━━
🦅 Nom commun: | Nom scientifique:
📌 Taxonomie: Ordre → Famille → Genre
🎨 Caractéristiques diagnostiques:
🌍 Habitat naturel:
⚠️ Statut UICN:
📚 Source: Cornell Lab / eBird / BirdLife International
━━━━━━━━━━━━━━━━━━━━━━
⚠️ Niveau de confiance: [Élevé/Moyen/Faible] + raison"""
}
 
# ── FUNCTIONS ────────────────────────────────────────────────
def chat_groq(msg, lang, history):
    msgs = [{"role":"system","content":SYS[lang]}]
    for h in history[-8:]:
        msgs.append({"role":"assistant" if h["role"]=="model" else "user","content":h["content"]})
    msgs.append({"role":"user","content":msg})
    r = groq_client.chat.completions.create(model=CHAT_MODEL, messages=msgs, max_tokens=2000, temperature=0.2)
    return r.choices[0].message.content
 
def analyze_image(img_file, lang):
    try:
        img_bytes = img_file.read()
        b64 = base64.b64encode(img_bytes).decode()
        ext = img_file.name.split(".")[-1].lower()
        mime = "image/png" if ext=="png" else "image/jpeg"
        r = groq_client.chat.completions.create(
            model=VISION_MODEL,
            messages=[{"role":"user","content":[
                {"type":"image_url","image_url":{"url":f"data:{mime};base64,{b64}"}},
                {"type":"text","text":IMG_P[lang]}
            ]}],
            max_tokens=1500, temperature=0.2
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
        rec = Recording(analyzer, tmp_path, lat=lat, lon=lon, date_frmt="%Y-%m-%d", date=today, min_conf=0.20)
        rec.analyze()
        os.unlink(tmp_path)
        if rec.detections:
            birds = "\n".join([f"• {d['common_name']} ({d['scientific_name']}) — {d['confidence']:.0%}" for d in rec.detections[:5]])
            prompt = f"BirdNET detected:\n{birds}\n\nProvide full academic profile."
        else:
            prompt = "BirdNET found no clear bird. Advise user on better recording quality."
        return chat_groq(prompt, lang, [])
    except Exception as e:
        return f"⚠️ Audio error: {e}"
 
def save_session():
    if st.session_state.messages:
        first = next((m["content"] for m in st.session_state.messages if m["role"]=="user"), "Session")
        title = (first[:45]+"...") if len(first)>45 else first
        # avoid duplicate save
        ids = [s["id"] for s in st.session_state.all_sessions]
        if st.session_state.session_id not in ids:
            st.session_state.all_sessions.insert(0, {
                "id": st.session_state.session_id,
                "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "title": title,
                "messages": st.session_state.messages.copy()
            })
 
def new_session():
    save_session()
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())[:8]
    st.session_state.location_confirmed = False
 
# ── SESSION STATE ────────────────────────────────────────────
defs = {
    "page":"landing","messages":[],"lang":"العربية","mode":"chat",
    "all_sessions":[],"session_id":str(uuid.uuid4())[:8],
    "location_confirmed":False,"lat":36.7,"lon":3.0,"viewing_hist":None
}
for k,v in defs.items():
    if k not in st.session_state: st.session_state[k]=v
 
# ════════════════════════════════════════════════════════════
#  LANDING PAGE
# ════════════════════════════════════════════════════════════
if st.session_state.page == "landing":
    st.markdown("""
    <div class="landing-wrap">
      <div class="bird-icon">🦅</div>
      <div class="brand-title">ORNIS</div>
      <div class="brand-ia">INTELLIGENCE ARTIFICIELLE ORNITHOLOGIQUE</div>
      <div class="gold-line"></div>
      <div class="tagline">
        منصة ذكاء اصطناعي أكاديمية متخصصة في علم الطيور<br>
        تحليل الصور · تسجيل الأصوات المباشر · معرفة علمية موثّقة<br>
        <span style="font-size:13px;opacity:.5;font-family:'Cormorant Garamond',serif;letter-spacing:2px">
          Powered by Cornell Lab · eBird · BirdLife International
        </span>
      </div>
      <div class="features-row">
        <div class="feat-pill">🖼️ تحليل الصور</div>
        <div class="feat-pill">🎙️ تسجيل مباشر</div>
        <div class="feat-pill">📚 مصادر أكاديمية</div>
        <div class="feat-pill">🌍 متعدد اللغات</div>
        <div class="feat-pill">🕓 سجل المحادثات</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    c1,c2,c3 = st.columns([1,2,1])
    with c2:
        lang = st.selectbox("", ["العربية","English","Français"], label_visibility="collapsed")
        st.session_state.lang = lang
        if st.button("✦  Enter Ornis IA  ✦", use_container_width=True):
            st.session_state.page = "chat"
            st.rerun()
 
# ════════════════════════════════════════════════════════════
#  HISTORY PAGE
# ════════════════════════════════════════════════════════════
elif st.session_state.page == "history":
    st.markdown("""
    <div class="chat-top">
      <div class="chat-logo">🕓 HISTORY</div>
      <div class="chat-sub">Past Conversations</div>
    </div>
    """, unsafe_allow_html=True)
 
    cb1,cb2 = st.columns([1,4])
    with cb1:
        if st.button("← Back"):
            st.session_state.viewing_hist = None
            st.session_state.page = "chat"
            st.rerun()
 
    if not st.session_state.all_sessions:
        st.markdown('<p style="color:rgba(212,175,55,.5);text-align:center;margin-top:40px">No history yet — start a conversation first.</p>', unsafe_allow_html=True)
    else:
        if st.session_state.viewing_hist is None:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            for sess in st.session_state.all_sessions:
                col_t, col_b = st.columns([5,1])
                with col_t:
                    st.markdown(f'<div class="hist-item">💬 {sess["title"]}<div class="hist-date">🕓 {sess["date"]} · {len(sess["messages"])} messages</div></div>', unsafe_allow_html=True)
                with col_b:
                    if st.button("View", key=f"view_{sess['id']}"):
                        st.session_state.viewing_hist = sess["id"]
                        st.rerun()
        else:
            sess = next((s for s in st.session_state.all_sessions if s["id"]==st.session_state.viewing_hist), None)
            if sess:
                st.markdown(f'<p style="color:#d4af37;font-size:13px">🕓 {sess["date"]}</p>', unsafe_allow_html=True)
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                for m in sess["messages"]:
                    if m["role"]=="user":
                        st.markdown(f'<div class="bubble-user">👤 {m["content"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="bubble-bot">🦅 {m["content"]}<br><span class="src-badge">📚 Cornell Lab · eBird · BirdLife · IUCN</span></div>', unsafe_allow_html=True)
            if st.button("← All Sessions"):
                st.session_state.viewing_hist = None
                st.rerun()
 
# ════════════════════════════════════════════════════════════
#  CHAT PAGE
# ════════════════════════════════════════════════════════════
else:
    lang = st.session_state.lang
 
    # ── SIDEBAR ────────────────────────────────────────────
    with st.sidebar:
        st.markdown('<p style="font-family:Playfair Display,serif;font-size:20px;color:#d4af37;letter-spacing:4px;text-align:center">ORNIS IA</p>', unsafe_allow_html=True)
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
 
        lang = st.selectbox("🌍 Language", ["العربية","English","Français"],
                            index=["العربية","English","Français"].index(st.session_state.lang))
        st.session_state.lang = lang
 
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p style="color:#d4af37;font-size:12px;letter-spacing:1px">📚 SCIENTIFIC SOURCES</p>', unsafe_allow_html=True)
        st.markdown("""<p style="color:#888;font-size:11px;line-height:2.2">
🔬 Cornell Lab of Ornithology<br>🐦 eBird Global Database<br>
🌍 BirdLife International<br>📖 HBW Alive<br>
🎵 Xeno-canto<br>🔴 IUCN Red List</p>""", unsafe_allow_html=True)
 
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p style="color:#d4af37;font-size:12px;letter-spacing:1px">🕓 RECENT SESSIONS</p>', unsafe_allow_html=True)
 
        if st.session_state.all_sessions:
            for s in st.session_state.all_sessions[:5]:
                st.markdown(f'<div class="hist-item" style="font-size:11px">💬 {s["title"][:30]}...<div class="hist-date">{s["date"]}</div></div>', unsafe_allow_html=True)
            if st.button("📂 View All History"):
                save_session()
                st.session_state.page = "history"
                st.rerun()
        else:
            st.markdown('<p style="color:rgba(212,175,55,.3);font-size:11px">No history yet</p>', unsafe_allow_html=True)
 
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        if st.button("➕ New Chat"):
            new_session()
            st.rerun()
        if st.button("🗑️ Clear Current"):
            st.session_state.messages = []
            st.rerun()
        if st.button("🏠 Home"):
            save_session()
            st.session_state.page = "landing"
            st.rerun()
 
    # ── HEADER ─────────────────────────────────────────────
    st.markdown("""
    <div class="chat-top">
      <div class="chat-logo">🦅 ORNIS IA</div>
      <div class="chat-sub">Ornithological Artificial Intelligence</div>
    </div>""", unsafe_allow_html=True)
 
    # ── MODE BUTTONS ────────────────────────────────────────
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("💬  Chat", use_container_width=True, key="m_chat"):
            st.session_state.mode="chat"; st.rerun()
    with c2:
        if st.button("🖼️  Image Analysis", use_container_width=True, key="m_img"):
            st.session_state.mode="image"; st.rerun()
    with c3:
        if st.button("🎙️  Record Audio", use_container_width=True, key="m_aud"):
            st.session_state.mode="audio"; st.rerun()
 
    labels = {"chat":"💬 Chat Mode","image":"🖼️ Image Analysis Mode","audio":"🎙️ Live Audio Recording Mode"}
    st.markdown(f'<p style="text-align:center;color:rgba(212,175,55,.55);font-size:12px;letter-spacing:2px;margin:6px 0 12px">{labels[st.session_state.mode]}</p>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
 
    # ── MESSAGES ────────────────────────────────────────────
    for m in st.session_state.messages:
        if m["role"]=="user":
            st.markdown(f'<div class="bubble-user">👤 {m["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bubble-bot">🦅 {m["content"]}<br><span class="src-badge">📚 Cornell Lab · eBird · BirdLife · IUCN</span></div>', unsafe_allow_html=True)
 
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
 
    # ════════════════════════════════════════════════
    #  IMAGE MODE
    # ════════════════════════════════════════════════
    if st.session_state.mode == "image":
        st.markdown('<div class="upload-card"><div class="upload-card-title">🖼️ &nbsp; Bird Image Analysis</div>', unsafe_allow_html=True)
        img = st.file_uploader("Upload a clear bird photo", type=["jpg","jpeg","png","webp"], key="img_up")
        if img:
            col_i,_ = st.columns([1,2])
            with col_i:
                st.image(img, caption="📸 Uploaded", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if img and st.button("🔍  Identify Species from Image", use_container_width=True):
            with st.spinner("🔭 Analyzing with Llama Vision AI..."):
                res = analyze_image(img, lang)
                st.session_state.messages.append({"role":"user","content":"📸 [Bird image uploaded]"})
                st.session_state.messages.append({"role":"model","content":res})
                st.rerun()
 
    # ════════════════════════════════════════════════
    #  AUDIO MODE  —  Like Merlin: Location → Record
    # ════════════════════════════════════════════════
    elif st.session_state.mode == "audio":
 
        if not st.session_state.location_confirmed:
            # ── STEP 1: LOCATION ──────────────────────
            st.markdown('<div class="upload-card">', unsafe_allow_html=True)
            st.markdown('<div class="step-badge">STEP 1 OF 2</div>', unsafe_allow_html=True)
            st.markdown('<div class="upload-card-title">📍 &nbsp; Confirm Your Location</div>', unsafe_allow_html=True)
            st.markdown('<p style="color:rgba(255,255,255,.55);font-size:13px;margin-bottom:16px">BirdNET uses your coordinates to improve species identification accuracy — just like Merlin.</p>', unsafe_allow_html=True)
 
            defaults_loc = {"العربية":(36.7,3.0),"English":(37.09,-95.71),"Français":(46.23,2.21)}
            lat_d, lon_d = defaults_loc[lang]
 
            col_lat, col_lon = st.columns(2)
            with col_lat:
                lat = st.number_input("📍 Latitude", value=lat_d, format="%.4f", key="lat_inp")
            with col_lon:
                lon = st.number_input("📍 Longitude", value=lon_d, format="%.4f", key="lon_inp")
 
            st.markdown('<p style="color:rgba(212,175,55,.4);font-size:11px;margin-top:6px">💡 Find your coordinates at <a href="https://maps.google.com" target="_blank" style="color:#d4af37">maps.google.com</a> → right-click → "What\'s here?"</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
 
            if st.button("📍  Confirm Location & Continue →", use_container_width=True):
                st.session_state.lat = lat
                st.session_state.lon = lon
                st.session_state.location_confirmed = True
                st.rerun()
 
        else:
            # ── STEP 2: RECORD ────────────────────────
            st.markdown(f'<p style="color:rgba(212,175,55,.6);font-size:12px;text-align:center">📍 Location confirmed: {st.session_state.lat:.2f}°, {st.session_state.lon:.2f}° &nbsp;|&nbsp; <span style="cursor:pointer;text-decoration:underline" onclick="">Change</span></p>', unsafe_allow_html=True)
 
            cloc1, cloc2 = st.columns([4,1])
            with cloc2:
                if st.button("📍 Change", key="change_loc"):
                    st.session_state.location_confirmed = False
                    st.rerun()
 
            st.markdown('<div class="upload-card">', unsafe_allow_html=True)
            st.markdown('<div class="step-badge">STEP 2 OF 2</div>', unsafe_allow_html=True)
            st.markdown('<div class="upload-card-title">🎙️ &nbsp; Record Bird Sound</div>', unsafe_allow_html=True)
            st.markdown('<p style="color:rgba(255,255,255,.55);font-size:13px;margin-bottom:14px">Hold the record button, point your device toward the bird, and stay still for at least 10 seconds.</p>', unsafe_allow_html=True)
 
            audio_val = st.audio_input("🎙️ Press to record bird sound")
 
            if audio_val:
                st.success("✅ Recording captured! Press Identify to analyze.")
 
            st.markdown('</div>', unsafe_allow_html=True)
 
            if audio_val and st.button("🎧  Identify Species from Recording", use_container_width=True):
                with st.spinner("🔊 Running BirdNET neural analysis..."):
                    if hasattr(audio_val, 'read'):
                        ab = audio_val.read()
                    else:
                        ab = audio_val
                    res = analyze_audio(ab, st.session_state.lat, st.session_state.lon, lang)
                    st.session_state.messages.append({"role":"user","content":"🎙️ [Live bird recording captured]"})
                    st.session_state.messages.append({"role":"model","content":res})
                    st.rerun()
 
    # ════════════════════════════════════════════════
    #  CHAT MODE
    # ════════════════════════════════════════════════
    else:
        ph = {"العربية":"💬 اكتب سؤالك الأكاديمي عن الطيور...",
              "English":"💬 Ask your ornithological question...",
              "Français":"💬 Posez votre question ornithologique..."}
        user_input = st.chat_input(ph[lang])
        if user_input:
            st.session_state.messages.append({"role":"user","content":user_input})
            with st.spinner("🤔 Consulting databases..."):
                reply = chat_groq(user_input, lang, st.session_state.messages[:-1])
            st.session_state.messages.append({"role":"model","content":reply})
            st.rerun()