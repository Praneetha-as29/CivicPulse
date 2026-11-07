# CivicPulse — AI-Assisted Civic Incident Triage and Coordination

## Overview

CivicPulse is a civic incident management prototype designed to improve how public infrastructure complaints are analysed, prioritised, reviewed, and tracked.

Citizens frequently report issues such as damaged roads, garbage accumulation, drainage problems, water supply disruptions, and electrical hazards. Delays in identifying urgency and routing complaints to the appropriate department can affect public safety and service delivery.

CivicPulse provides a structured workflow for incident reporting, severity assessment, department recommendation, duplicate detection, human approval, and resolution tracking.

The project also explores human–AI coordination through Switch, where an AI agent analyses incidents, explains its recommendations, checks available incident history, and waits for explicit human approval.

## Problem Statement

Traditional civic complaint handling can involve fragmented reporting, inconsistent prioritisation, duplicate complaints, and delays in routing issues to responsible departments.

CivicPulse aims to make this process more organised, transparent, and accountable through an assisted incident management workflow.

## Key Features

### 1. Civic Incident Reporting
Users can submit complaints with a location, issue category, and description.

### 2. Severity Assessment
The application evaluates incident descriptions and assigns one of four severity levels:

- Low
- Medium
- High
- Critical

The current Flask implementation uses rule-based classification and predefined safety indicators.

### 3. Department Recommendation
The application recommends a relevant department based on the reported issue category.

### 4. Duplicate Incident Detection
The system compares new complaints with existing incidents using text similarity and location information to identify possible duplicates.

Duplicate detection is advisory and does not automatically merge or discard reports.

### 5. Human-in-the-Loop Approval
Every submitted incident initially enters a pending approval state. A human reviewer can approve or reject the proposed assignment.

### 6. Incident Status Tracking
Approved incidents can be tracked through:

- Assigned
- In Progress
- Resolved

### 7. Switch AI Agent
The `civicpulse-triage` agent provides an additional AI-assisted review workflow.

It can:
- Analyse incident descriptions.
- Recommend severity levels.
- Suggest responsible departments.
- Compare reports against available incident history.
- Explain possible duplicate matches and uncertainty.
- Present assignment proposals.
- Wait for explicit human approval.
- Record human decisions in Switch.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite |
| Frontend | HTML, CSS |
| AI coordination | Switch AI agent |
| Development environment | Visual Studio Code |
| Container tooling | Docker installed; container deployment not yet configured |

## System Workflow

1. A civic complaint is submitted through the Flask application.
2. The application analyses the report.
3. Severity and department recommendations are generated.
4. Potential duplicate incidents are identified.
5. The incident is stored in the SQLite database.
6. A human reviewer approves or rejects the proposed assignment.
7. Approved incidents move through the status tracking workflow.
8. The Switch AI agent can separately analyse incident information, explain its recommendations, and request human approval.

## Human–AI Coordination Through Switch

CivicPulse uses a dedicated Switch agent named `civicpulse-triage`.

The agent is configured to preserve incident details, avoid inventing missing information, explain uncertainty, and wait for explicit human approval before recording an approved triage decision.

The demonstration uses a simulated electrical safety incident:

- Flask classified the incident as High severity.
- Switch independently recommended Critical severity based on the active sparking wire and nearby pedestrians.
- The agent explained its reasoning and uncertainty about department ownership.
- A human approved the recommendation in Switch.
- The approval was recorded in the Switch conversation.

The corresponding Flask incident was separately approved in the dashboard.

**Current integration status:** The Flask application and Switch agent operate as separate components. Incident details are manually provided to the Switch agent, and decisions are recorded independently. Automatic API-based synchronization between the two components has not yet been implemented.

## Architecture

**Flask Application**
- Complaint submission
- Rule-based severity assessment
- Department recommendation
- Duplicate detection
- Human approval
- Incident status tracking

**SQLite Database**
- Incident records
- Severity information
- Department recommendations
- Approval decisions
- Status information

**Switch AI Agent**
- Incident analysis
- Evidence-based recommendations
- Duplicate assessment
- Human approval interaction
- Decision recording within Switch

## Installation and Setup

### Prerequisites

- Python 3.11 or later
- Visual Studio Code or another code editor

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd CivicPulse
```

Replace the placeholder with the actual repository URL.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python app.py
```

### 6. Open the dashboard

Visit:

```text
http://127.0.0.1:5000
```

The SQLite database is created and initialized automatically when the application starts.

## Future Enhancements

- Automatic communication between Flask and Switch through a supported API or integration layer.
- Shared incident identifiers and synchronized approval records.
- Machine-learning-based incident classification.
- Improved duplicate detection using semantic similarity.
- Image-based evidence analysis.
- Real-time incident coordination and notifications.
- Deployment through Docker and a cloud hosting platform.

## Safety and Limitations

- The application is a prototype and is not connected to official municipal systems.
- Severity and department recommendations are advisory.
- The current Flask classification engine is rule-based, not a trained machine-learning model.
- Switch approvals are recorded within Switch and do not constitute actual government department assignments.
- No emergency services or municipal departments are contacted.
- Duplicate detection identifies possible matches and does not establish that two reports concern the same physical incident.
- Demonstration incidents are simulated.

## Project Goal

CivicPulse demonstrates how structured civic reporting, automated triage, transparent recommendations, duplicate assessment, and human oversight can work together to support more accountable civic incident coordination.