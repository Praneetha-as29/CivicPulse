# CivicPulse – AI-Assisted Civic Incident Reporting and Coordination

CivicPulse is a civic incident reporting and coordination prototype designed to make it easier for citizens to report local problems and help civic teams review, prioritize, and track them.

The project combines a Flask-based reporting dashboard with a Switch AI agent for incident analysis and operational coordination. It demonstrates how structured reporting, rule-based prioritization, duplicate detection, and human approval can support a more organized civic response workflow.

## Problem Statement

Citizens frequently encounter civic issues such as damaged roads, garbage accumulation, water supply problems, drainage blockages, and non-functional streetlights. Reporting these issues and following their progress can be difficult when information is scattered or lacks a clear process.

CivicPulse demonstrates a centralized workflow where incidents can be submitted, reviewed, categorized, prioritized, and tracked.

## Key Features

- **Civic Incident Reporting:** Submit civic complaints with a category, location, and description.
- **Rule-Based Severity Classification:** Assigns severity levels based on incident details.
- **Department Recommendation:** Suggests the relevant civic department based on the selected category.
- **Duplicate Detection:** Identifies potentially similar reports using category, location, and description similarity.
- **Human-in-the-Loop Approval:** Keeps new reports pending until a human reviews and approves or rejects them.
- **Incident Tracking:** Tracks reports through Pending Approval, Assigned, In Progress, and Resolved statuses.
- **Dashboard and Statistics:** Displays incident records and summary information.
- **Switch AI Agent:** Uses a dedicated agent named `civicpulse-triage` to analyze incident information and support operational coordination.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite |
| Frontend | HTML, CSS |
| AI Coordination | Switch |
| Development Environment | Visual Studio Code |

## Civic Incident Categories and Department Recommendations

| Incident Category | Recommended Department |
|---|---|
| Road Damage | GHMC Roads & Engineering |
| Garbage | GHMC Sanitation Department |
| Water Supply | HMWSSB |
| Streetlight | GHMC Electrical Department |
| Drainage | GHMC Drainage Department |
| Public Safety | Local Civic Safety Authority |
| Other | Relevant Municipal Department |

These are prototype recommendations and do not represent confirmed assignments to government departments.

## How the Workflow Works

1. A citizen submits a civic incident through the CivicPulse reporting form.
2. The application stores the report in the SQLite database.
3. The system applies rule-based severity classification.
4. A relevant civic department is recommended based on the incident category.
5. Duplicate detection checks whether a similar report may already exist.
6. The incident enters **Pending Approval** status.
7. A human reviewer approves or rejects the report.
8. Approved incidents can move through Assigned, In Progress, and Resolved.
9. Incident information can be shared with the Switch agent for additional analysis and coordination.

## How Switch Is Used

Switch is used as the AI coordination layer of CivicPulse.

The project includes a Switch agent named:

`civicpulse-triage`

The agent supports incident analysis by examining submitted incident information, identifying its severity and relevant context, and assisting with coordination decisions.

### Switch Coordination Workflow

1. Incident information is taken from the CivicPulse application.
2. The information is manually provided to the `civicpulse-triage` agent through the Switch environment.
3. The agent analyzes the incident and provides its assessment.
4. A human reviews the agent's recommendation before making an operational decision.

### Human-in-the-Loop Example

During testing, a streetlight-related incident was recorded in CivicPulse with a **High** severity classification.

A separate demonstration scenario was provided to the Switch agent involving an electrical hazard with an exposed sparking wire and pedestrians nearby. The agent assessed that scenario as **Critical** because of the immediate safety risk.

The human reviewer remained responsible for the final approval decision.

The two assessments were based on different incident inputs. They were not automatically synchronized.

### Important Integration Note

CivicPulse and Switch operate as separate components in this prototype. Incident information is transferred manually between the Flask application and the Switch agent.

There is currently no automatic API integration or database synchronization between the two components. Approval and status changes made in one component do not automatically update the other.

## System Architecture

The prototype consists of two main components:

### 1. CivicPulse Application

- Flask backend
- SQLite database
- Incident reporting interface
- Severity classification
- Department recommendation
- Duplicate detection
- Human approval and status tracking

### 2. Switch Coordination Layer

- Switch environment
- `civicpulse-triage` agent
- Discord messaging integration
- Incident analysis and coordination support
- Human review of agent recommendations

The components work together through a manual information handoff.

## Installation and Setup

### Prerequisites

- Python 3.11 or later
- Git
- Visual Studio Code (recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Praneetha-as29/CivicPulse.git
cd CivicPulse
```

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 3: Activate the Virtual Environment

**Windows:**

```bash
.venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the Application

```bash
python app.py
```

### Step 6: Open CivicPulse

Open the following address in your browser:

```text
http://127.0.0.1:5000
```

The SQLite database is created locally by the application when required.

## Project Structure

```text
CivicPulse/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

The SQLite database is generated locally and is excluded from Git tracking.

## Testing and Demonstration

The prototype can be demonstrated using simulated civic incident reports.

The demonstration covers:

- Submitting a new civic complaint.
- Viewing the incident on the dashboard.
- Checking rule-based severity classification.
- Viewing the recommended department.
- Identifying potential duplicate reports.
- Reviewing an incident pending human approval.
- Approving or rejecting an incident.
- Updating incident status.
- Manually sharing incident information with the Switch agent.
- Reviewing the agent's assessment and human decision.

All incidents used for demonstration are simulated. The prototype does not dispatch emergency services or directly communicate with municipal authorities.

## Safety and Limitations

- Severity classification is rule-based and does not use a trained machine learning model.
- Duplicate detection provides an indication of possible duplicates; it does not guarantee that two reports describe the same incident.
- Department recommendations are suggestions and are not official government assignments.
- Human approval is required before an incident proceeds beyond the pending review stage.
- Switch agent recommendations are advisory and require human judgment.
- CivicPulse and Switch do not currently have automatic API-based synchronization.
- The prototype is intended for demonstration and evaluation, not deployment as a live emergency response system.

## Future Enhancements

- Automatic integration between CivicPulse and Switch through APIs.
- Real-time incident updates and notifications.
- Map-based incident visualization.
- Citizen account management and report history.
- Improved duplicate detection and incident prioritization.
- Integration with verified civic authority systems.
- Deployment to a production hosting environment.

## Project Goal

CivicPulse demonstrates how civic reporting, structured incident management, AI-assisted analysis, and human-in-the-loop decision-making can be combined into a practical coordination workflow.

The goal is to make civic issue reporting more organized, transparent, and easier to manage while keeping important decisions under human control.

---

**Built for the Flip the Switch Hackathon.**
