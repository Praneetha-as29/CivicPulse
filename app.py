
import os
import re
import sqlite3
from datetime import datetime
from flask import Flask, request, redirect, url_for, render_template_string

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "civicpulse.db")

app = Flask(__name__)
app.secret_key = os.environ.get("CIVICPULSE_SECRET", "change-this-local-demo-secret")

CATEGORIES = {
    "Road Damage": "GHMC Roads & Engineering",
    "Garbage": "GHMC Sanitation Department",
    "Water Supply": "HMWSSB",
    "Streetlight": "GHMC Electrical Department",
    "Drainage": "GHMC Drainage Department",
    "Public Safety": "Local Civic Safety Authority",
    "Other": "Relevant Municipal Department"
}

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CivicPulse | Civic Intelligence</title>
<style>
:root{--bg:#0b1020;--panel:#131c30;--text:#eef3ff;--muted:#91a0bb;--accent:#60d5c2;--border:#263550;--red:#ffaaaa;--yellow:#ffdc8c}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);font-family:Inter,Segoe UI,Arial,sans-serif}
header{padding:22px 5%;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center}
.brand{font-size:24px;font-weight:800;letter-spacing:-1px}
.brand span{color:var(--accent)}
.tag{font-size:11px;color:var(--accent);border:1px solid #28685e;padding:6px 10px;border-radius:20px}
main{max-width:1250px;margin:32px auto;padding:0 22px}
h1{font-size:32px;margin:0 0 8px}
.subtitle{color:var(--muted);margin-bottom:28px}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin-bottom:25px}
.stat,.panel,.incident{background:var(--panel);border:1px solid var(--border);border-radius:14px;padding:20px}
.stat small,.muted{color:var(--muted)}
.stat strong{display:block;font-size:29px;margin-top:12px}
.layout{display:grid;grid-template-columns:.9fr 1.4fr;gap:20px;align-items:start}
h2{font-size:18px;margin:0 0 18px}
label{display:block;color:#c2cde0;font-size:13px;margin:15px 0 7px}
input,select,textarea{width:100%;padding:12px;background:#0c1527;border:1px solid var(--border);border-radius:8px;color:white;font:inherit}
textarea{min-height:105px;resize:vertical}
button{border:0;border-radius:8px;padding:11px 16px;background:var(--accent);color:#071c1b;font-weight:700;cursor:pointer}
button:hover{filter:brightness(1.08)}
.secondary{background:#273650;color:white}
.danger{background:#542c37;color:var(--red)}
.submit{width:100%;margin-top:18px}
.incident{margin-bottom:13px;padding:17px}
.incident-top{display:flex;justify-content:space-between;gap:12px;align-items:center}
.incident h3{font-size:16px;margin:0 0 7px}
.pill{display:inline-block;padding:5px 9px;border-radius:20px;background:#25344b;color:#cbd8ef;font-size:11px}
.High,.Critical{background:#542c37;color:var(--red)}
.Medium{background:#544627;color:var(--yellow)}
.Low{background:#1e493e;color:#9af0d5}
.reason{color:var(--muted);font-size:13px;line-height:1.5;margin:12px 0}
.actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}
.actions form{display:flex;gap:6px;flex-wrap:wrap}
.actions select{width:auto;max-width:160px;padding:8px}
.actions button{padding:8px 11px;font-size:12px}
.alert{padding:12px;border-radius:8px;background:#26344b;color:#dce8ff;margin-bottom:15px;font-size:13px}
.duplicate{color:var(--yellow);font-size:12px;margin-top:8px}
.empty{text-align:center;color:var(--muted);padding:40px 10px}
footer{text-align:center;color:var(--muted);font-size:12px;padding:30px}
@media(max-width:850px){.layout{grid-template-columns:1fr}.stats{grid-template-columns:repeat(2,1fr)}}
@media(max-width:450px){.stats{grid-template-columns:1fr 1fr}header{padding:18px}.brand{font-size:20px}h1{font-size:26px}}
</style>
</head>
<body>
<header>
<div class="brand">Civic<span>Pulse</span></div>
<div class="tag">AI-ASSISTED CIVIC OPERATIONS</div>
</header>
<main>
<h1>Civic Incident Command Center</h1>
<p class="subtitle">Report. Analyse. Review. Resolve. &nbsp;|&nbsp; Hyderabad prototype</p>

{% for message in messages %}
<div class="alert">{{ message }}</div>
{% endfor %}

<section class="stats">
<div class="stat"><small>Total incidents</small><strong>{{ total }}</strong></div>
<div class="stat"><small>Awaiting approval</small><strong>{{ pending }}</strong></div>
<div class="stat"><small>High / Critical</small><strong>{{ urgent }}</strong></div>
<div class="stat"><small>Resolved</small><strong>{{ resolved }}</strong></div>
</section>

<div class="layout">
<section class="panel">
<h2>Submit a civic complaint</h2>
<form action="/submit" method="POST">
<label>Incident location</label>
<input name="location" placeholder="e.g. Gachibowli Junction, Hyderabad" required maxlength="180">

<label>Issue category</label>
<select name="category" required>
<option value="Road Damage">Road damage / pothole</option>
<option value="Garbage">Garbage / sanitation</option>
<option value="Water Supply">Water supply</option>
<option value="Streetlight">Streetlight</option>
<option value="Drainage">Drainage / sewage</option>
<option value="Public Safety">Public safety</option>
<option value="Other">Other</option>
</select>

<label>Complaint description</label>
<textarea name="description" placeholder="Describe the civic issue and its impact..." required maxlength="1500"></textarea>

<button class="submit" type="submit">Analyse and submit incident →</button>
</form>
<p class="muted" style="font-size:12px;margin-top:15px">Analysis is advisory. Human approval is required before assignment.</p>
</section>

<section>
<h2>Incident register · {{ incidents|length }} records</h2>
{% for item in incidents %}
<article class="incident">
<div class="incident-top">
<div>
<h3>CP-{{ "%04d"|format(item.id) }} · {{ item.category }}</h3>
<span class="muted" style="font-size:12px">{{ item.location }}</span>
</div>
<span class="pill {{ item.severity }}">{{ item.severity }}</span>
</div>

<p class="reason">{{ item.description }}</p>
<div class="muted" style="font-size:12px">Recommended: {{ item.department }}</div>

{% if item.severity_reason %}
<p class="reason"><strong>Severity rationale:</strong> {{ item.severity_reason }}</p>
{% endif %}

{% if item.duplicate_of %}
<div class="duplicate">Possible duplicate of CP-{{ "%04d"|format(item.duplicate_of) }} · Similarity {{ item.duplicate_score }}%</div>
{% endif %}

<p class="muted" style="font-size:12px">Status: {{ item.status }} · {{ item.decision }} · {{ item.created_at }}</p>

{% if item.status == "Pending Approval" %}
<div class="actions">
<form action="/decision/{{ item.id }}" method="POST">
<button name="decision" value="approve">Approve assignment</button>
<button class="danger" name="decision" value="reject">Reject</button>
</form>
</div>
{% elif item.status == "Assigned" %}
<form class="actions" action="/status/{{ item.id }}" method="POST">
<select name="status" required>
<option value="In Progress">In Progress</option>
<option value="Resolved">Resolved</option>
</select>
<button class="secondary" type="submit">Update status</button>
</form>
{% endif %}
</article>
{% else %}
<div class="panel empty">No incidents yet. Submit your first civic complaint to begin.</div>
{% endfor %}
</section>
</div>
</main>
<footer>CivicPulse · Hackathon prototype · Simulated incidents only · Human oversight enabled</footer>
</body>
</html>
"""


def connect_db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    with connect_db() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                severity TEXT NOT NULL,
                department TEXT NOT NULL,
                duplicate_of INTEGER,
                duplicate_score REAL DEFAULT 0,
                status TEXT DEFAULT 'Pending Approval',
                decision TEXT DEFAULT 'Awaiting Review',
                created_at TEXT NOT NULL
            )
        """)

        columns = {
            row["name"]
            for row in con.execute("PRAGMA table_info(incidents)").fetchall()
        }

        if "severity_reason" not in columns:
            con.execute("ALTER TABLE incidents ADD COLUMN severity_reason TEXT DEFAULT ''")


def words(text):
    stop_words = {
        "a", "an", "the", "is", "are", "was", "were", "to",
        "of", "on", "in", "it", "and", "or", "for", "near",
        "has", "have", "been", "this", "that", "its"
    }

    synonyms = {
        "deep": "large",
        "big": "large",
        "huge": "large",
        "multiple": "several",
        "many": "several",
        "appeared": "present",
        "occurring": "present",
        "dangerous": "hazard",
        "collision": "hazard",
        "collisions": "hazard",
        "swerving": "swerve",
        "vehicles": "vehicle",
        "cars": "vehicle",
        "accidents": "accident",
        "injuries": "injury",
        "potholes": "pothole",
        "lights": "light",
        "lamps": "light"
    }

    tokens = re.findall(r"[a-z0-9]+", text.lower())

    return {
        synonyms.get(word, word)
        for word in tokens
        if word not in stop_words
    }


def analyse(location, category, description):
    text = description.lower()
    department = CATEGORIES.get(category, CATEGORIES["Other"])

    critical_phrases = [
        "life threatening",
        "person trapped",
        "people trapped",
        "building collapsing",
        "building collapsed",
        "electrocuted",
        "major fire",
        "uncontrolled fire",
        "multiple people injured"
    ]

    high_phrases = [
        "exposed live wire",
        "live electric wire",
        "electric wire exposed",
        "electric pole fallen",
        "sewage overflow",
        "open manhole",
        "water flooding the road",
        "road collapse",
        "vehicles swerving",
        "vehicle swerving",
        "collision risk",
        "traffic hazard",
        "garbage blocking the road",
        "waste blocking traffic",
        "medical waste",
        "hazardous waste",
        "drinking water contaminated",
        "water supply contaminated",
        "severe water leakage"
    ]

    if any(phrase in text for phrase in critical_phrases):
        return (
            "Critical",
            "The report contains language indicating a possible immediate threat to life. Urgent human assessment is required.",
            department
        )

    if any(phrase in text for phrase in high_phrases):
        return (
            "High",
            "The reported conditions indicate a significant public safety or health risk requiring priority human review.",
            department
        )

    if category == "Road Damage":
        traffic_risk = any(term in text for term in [
            "swerve", "swerving", "accident", "collision",
            "vehicle", "traffic", "injury"
        ])

        serious_damage = any(term in text for term in [
            "large pothole", "deep pothole", "road collapse",
            "major crack", "road caved"
        ])

        if traffic_risk and serious_damage:
            return (
                "High",
                "Road damage combined with reported traffic or vehicle risk indicates a significant collision hazard.",
                department
            )

        if any(term in text for term in [
            "pothole", "crack", "damaged road", "broken road",
            "uneven road", "road damage"
        ]):
            return (
                "Medium",
                "The reported road defect requires maintenance attention. No immediate collision or injury risk is established in the description.",
                department
            )

    elif category == "Garbage":
        if any(term in text for term in [
            "blocking road", "blocked road", "blocking entrance",
            "blocking access", "waste fire", "burning garbage",
            "toxic waste", "hazardous waste", "medical waste"
        ]):
            return (
                "High",
                "The reported waste condition may create a significant public health or access risk and requires priority review.",
                department
            )

        if any(term in text for term in [
            "garbage", "waste", "rubbish", "trash",
            "overflowing bin", "bad smell", "unpleasant smell",
            "stray animals", "accumulating"
        ]):
            return (
                "Medium",
                "The sanitation issue requires municipal cleaning or collection, but an immediate severe hazard is not established.",
                department
            )

    elif category == "Water Supply":
        if any(term in text for term in [
            "contaminated", "dirty drinking water",
            "sewage in drinking water", "waterborne illness"
        ]):
            return (
                "High",
                "Possible drinking water contamination creates a public health concern requiring priority assessment.",
                department
            )

        if any(term in text for term in [
            "no water", "water shortage", "water not coming",
            "low pressure", "water leakage", "pipe leak",
            "irregular supply"
        ]):
            return (
                "Medium",
                "The water supply issue requires utility inspection and maintenance.",
                department
            )

    elif category == "Streetlight":
        if any(term in text for term in [
            "exposed wire", "live wire", "electric shock",
            "sparking", "electric pole fallen"
        ]):
            return (
                "High",
                "The electrical fault may expose people to electric shock or other immediate danger.",
                department
            )

        if any(term in text for term in [
            "streetlight", "street light", "lamp not working",
            "light not working", "dark street", "light broken"
        ]):
            return (
                "Medium",
                "The lighting fault requires electrical maintenance. No direct electrical hazard is established in the description.",
                department
            )

    elif category == "Drainage":
        if any(term in text for term in [
            "sewage overflow", "sewage entering homes",
            "drain flooding road", "open manhole",
            "manhole uncovered", "drain collapse"
        ]):
            return (
                "High",
                "The drainage condition may create a public health or physical safety risk requiring priority review.",
                department
            )

        if any(term in text for term in [
            "blocked drain", "drain blocked", "drainage",
            "waterlogging", "sewage leak", "drain leak"
        ]):
            return (
                "Medium",
                "The drainage issue requires municipal maintenance and inspection.",
                department
            )

    elif category == "Public Safety":
        if any(term in text for term in [
            "immediate danger", "violent incident",
            "person injured", "fire", "accident",
            "unsafe structure", "building damage"
        ]):
            return (
                "High",
                "The reported public safety concern requires priority human assessment.",
                department
            )

        return (
            "Medium",
            "The public safety report requires review by the responsible authority.",
            department
        )

    general_medium = [
        "blocked", "leak", "broken", "damaged",
        "not working", "pothole", "garbage",
        "waste", "water shortage", "waterlogging",
        "drain", "streetlight"
    ]

    if any(term in text for term in general_medium):
        return (
            "Medium",
            "The issue requires civic maintenance or inspection, but the description does not establish an immediate severe safety threat.",
            department
        )

    return (
        "Low",
        "The report currently indicates a routine civic issue. Further details may change its priority.",
        department
    )


def find_duplicate(location, category, description):
    incoming = words(description)
    best_id = None
    best_score = 0
    normalized_location = words(location)

    with connect_db() as con:
        rows = con.execute(
            "SELECT id, location, category, description FROM incidents"
        ).fetchall()

    for row in rows:
        if row["category"] != category:
            continue

        existing_location = words(row["location"])

        if normalized_location != existing_location:
            continue

        existing = words(row["description"])

        if not incoming or not existing:
            continue

        intersection = len(incoming & existing)
        union = len(incoming | existing)

        if not union:
            continue

        jaccard = intersection / union
        overlap = intersection / min(len(incoming), len(existing))
        score = (0.65 * overlap) + (0.35 * jaccard)

        if score > best_score:
            best_score = score
            best_id = row["id"]

    if best_score >= 0.50:
        return best_id, round(best_score * 100, 1)

    return None, round(best_score * 100, 1)


@app.route("/")
def dashboard():
    with connect_db() as con:
        incidents = con.execute(
            "SELECT * FROM incidents ORDER BY id DESC"
        ).fetchall()

        total = con.execute(
            "SELECT COUNT(*) FROM incidents"
        ).fetchone()[0]

        pending = con.execute(
            "SELECT COUNT(*) FROM incidents WHERE status='Pending Approval'"
        ).fetchone()[0]

        urgent = con.execute(
            "SELECT COUNT(*) FROM incidents WHERE severity IN ('High','Critical')"
        ).fetchone()[0]

        resolved = con.execute(
            "SELECT COUNT(*) FROM incidents WHERE status='Resolved'"
        ).fetchone()[0]

    return render_template_string(
        PAGE,
        incidents=incidents,
        total=total,
        pending=pending,
        urgent=urgent,
        resolved=resolved,
        messages=request.args.getlist("message")
    )


@app.route("/submit", methods=["POST"])
def submit():
    location = request.form.get("location", "").strip()
    category = request.form.get("category", "").strip()
    description = request.form.get("description", "").strip()

    if not location or not description or category not in CATEGORIES:
        return redirect(
            url_for("dashboard", message="Please provide valid incident details.")
        )

    severity, reason, department = analyse(
        location, category, description
    )

    duplicate_id, duplicate_score = find_duplicate(
        location, category, description
    )

    created_at = datetime.now().strftime("%d %b %Y, %I:%M %p")

    with connect_db() as con:
        con.execute("""
            INSERT INTO incidents (
                location, category, description, severity, department,
                duplicate_of, duplicate_score, status, decision,
                created_at, severity_reason
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, 'Pending Approval',
                    'Awaiting Review', ?, ?)
        """, (
            location,
            category,
            description,
            severity,
            department,
            duplicate_id,
            duplicate_score,
            created_at,
            reason
        ))

    message = "Incident analysed and submitted for human approval."

    if duplicate_id:
        message += f" Possible duplicate of CP-{duplicate_id:04d} detected."

    return redirect(url_for("dashboard", message=message))


@app.route("/decision/<int:incident_id>", methods=["POST"])
def decision(incident_id):
    choice = request.form.get("decision")

    if choice not in ["approve", "reject"]:
        return redirect(
            url_for("dashboard", message="Invalid approval decision.")
        )

    if choice == "approve":
        status = "Assigned"
        decision_text = "Human Approved"
    else:
        status = "Rejected"
        decision_text = "Human Rejected"

    with connect_db() as con:
        cursor = con.execute("""
            UPDATE incidents
            SET status=?, decision=?
            WHERE id=? AND status='Pending Approval'
        """, (status, decision_text, incident_id))

    if cursor.rowcount == 0:
        message = f"CP-{incident_id:04d} could not be updated. Check its current status."
    else:
        message = f"CP-{incident_id:04d}: {decision_text}."

    return redirect(url_for("dashboard", message=message))


@app.route("/status/<int:incident_id>", methods=["POST"])
def update_status(incident_id):
    status = request.form.get("status")

    if status not in ["In Progress", "Resolved"]:
        return redirect(
            url_for("dashboard", message="Invalid incident status.")
        )

    with connect_db() as con:
        cursor = con.execute("""
            UPDATE incidents
            SET status=?
            WHERE id=? AND status='Assigned'
        """, (status, incident_id))

    if cursor.rowcount == 0:
        message = f"CP-{incident_id:04d} could not be updated. Approve it before changing its status."
    else:
        message = f"CP-{incident_id:04d} status updated to {status}."

    return redirect(url_for("dashboard", message=message))


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=False)
