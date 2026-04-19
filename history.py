import json, os
from datetime import datetime

HISTORY_FILE = "ornis_history.json"

def load_all():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE,"r",encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_session(sid, title, messages):
    all_sessions = load_all()
    # update if exists, else insert
    for s in all_sessions:
        if s["id"] == sid:
            s["title"]    = title
            s["messages"] = messages
            s["date"]     = datetime.now().strftime("%b %d · %H:%M")
            break
    else:
        all_sessions.insert(0, {
            "id":       sid,
            "title":    title,
            "date":     datetime.now().strftime("%b %d · %H:%M"),
            "messages": messages
        })
    with open(HISTORY_FILE,"w",encoding="utf-8") as f:
        json.dump(all_sessions, f, ensure_ascii=False, indent=2)

def delete_session(sid):
    all_sessions = [s for s in load_all() if s["id"] != sid]
    with open(HISTORY_FILE,"w",encoding="utf-8") as f:
        json.dump(all_sessions, f, ensure_ascii=False, indent=2)

def get_session(sid):
    return next((s for s in load_all() if s["id"]==sid), None)