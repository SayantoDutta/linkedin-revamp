# Skills section — universal rubric

The Skills section is the most underweighted real estate on LinkedIn. Recruiter search relies on it. Hover cards display top 5. The rest serves as keyword fodder.

This file gives you keep/drop/add logic that works for any role — no hardcoded tag set.

---

## Hard rules

1. **Top 5 are pinned and shown on hover cards.** Pick by reach × relevance to target_person.
2. **No more than 35 skills total.** Beyond that, signal-to-noise drops.
3. **No Forage / generic job simulations.** Unless the user is a recent grad with no other credentials, these signal junior.
4. **No expired tech.** Drop anything the user hasn't touched in 3+ years if it doesn't support their north_star.
5. **No "Microsoft Office" or "Excel" as a top skill.** Universal — implies nothing. Bury or drop.
6. **Every added skill must be linked to at least 1 Experience entry.** Phase 6 will ask which Experiences to link per add.

---

## Decision logic per skill

For each skill currently on the profile (from Phase 2 snapshot), classify into one of four categories:

### KEEP
The skill is:
- Relevant to `target_person` (a recruiter or client for this skill would care)
- Relevant to `north_star` (the user wants to be known for this in 2 years)
- Anchored by at least 1 Experience entry that legitimately used it

Examples per role:
- Product manager target_person = recruiter at PLG SaaS company → KEEP "Product Analytics", "A/B Testing", "PLG"
- Engineer target_person = staff role hiring manager → KEEP "Distributed Systems", "Python", "PostgreSQL", "Kubernetes"
- Designer target_person = brand director at consumer startup → KEEP "Brand Systems", "Figma", "Motion Design"

### DROP
The skill is:
- Pure clutter (Forage sims for a senior role)
- Stale (a tech the user hasn't used since 2019 that doesn't support the current direction)
- Misleading positioning (e.g. "Investment Banking" on a profile aimed at AI builder roles — the recruiter sees it and dismisses the AI builder claim)
- Generic to the point of meaninglessness (Microsoft Office, Time Management, Communication — unless the user's role is admin and the role explicitly requires these)

### ADD
A skill that:
- The user's CV demonstrates but it's missing from the live profile
- Is critical to `north_star` direction
- Has high recruiter-search volume (use known industry keywords)

For each, pick the canonical LinkedIn term — autocomplete picks the closest match, and small wording differences matter:
- "AI Agents" not "Agentic AI Development"
- "Large Language Models (LLM)" not "LLM"
- "Natural Language Processing (NLP)" not "NLP"
- "Amazon Web Services (AWS)" not "AWS"
- "PostgreSQL" not "Postgres"
- "Python (Programming Language)" not "Python"

When in doubt, use the term LinkedIn itself suggests when you type in the Add Skill modal.

### AMBIGUOUS
The skill could go either way. Bring to the user.

Examples:
- A user pivoting from finance to AI engineering — keep "Financial Modeling" or drop?
- A designer who used to do front-end — keep "React" or drop?

Phase 5 asks the user per-AMBIGUOUS skill.

---

## Universal ADD candidates by role direction

Use this only when the user's CV doesn't already list these. Adapt to the user's actual tools.

### Software Engineering
- The user's primary language (Python / TypeScript / Go / Rust / etc.)
- Their framework (React, Node.js, Django, FastAPI, Spring, etc.)
- Database they use (PostgreSQL / MySQL / MongoDB / Redis)
- Cloud platform (AWS / GCP / Azure)
- Specialty tags (distributed systems / API design / system design / CI-CD / observability)

### AI / ML
- Large Language Models (LLM)
- Natural Language Processing (NLP)
- Prompt Engineering
- Retrieval-Augmented Generation (RAG)
- Vector Databases
- Fine-tuning
- A specific framework (LangChain / LlamaIndex / Hugging Face)
- Cloud LLM API (OpenAI / Anthropic / Gemini)

### Product
- Product Management
- Product Analytics
- A/B Testing
- User Research
- Product Strategy
- The user's tool stack (Amplitude / Mixpanel / Pendo / Linear / Jira)

### Design
- UI/UX Design or Product Design
- Brand Systems
- Design Systems
- Motion Design (if relevant)
- Figma
- Prototyping
- User Research

### Sales / BD
- B2B Sales
- Outbound Sales
- Account-Based Marketing (if relevant)
- Sales Operations
- CRM tools (HubSpot / Salesforce)
- Negotiation
- Pipeline Management

### Marketing
- Growth Marketing
- Content Strategy
- SEO (if relevant)
- Demand Generation
- Brand Marketing
- Marketing Analytics
- Tool stack (HubSpot / Marketo / Customer.io / Brevo)

### Operations / Customer Success
- Customer Success
- Operations Management
- Process Improvement
- Project Management
- Tool stack (Asana / Notion / Linear / Zendesk)

### Founder / Operator
- Strategy
- Business Operations
- Fundraising (if true)
- Hiring
- Customer Discovery
- Product Strategy

### Data
- SQL
- Python
- Data Analysis
- Data Visualization (Tableau / Looker / Metabase)
- ETL / dbt
- Specific data warehouses (Snowflake / BigQuery / Redshift)

---

## Top-5 pin order — universal logic

Pin by:
1. **Highest reach** — recruiter search volume × relevance to target_person
2. **Strongest claim** — skills the user is most credible at (anchored to senior Experience entries)
3. **Differentiation** — skills that distinguish the user from generic peers
4. **Direction** — at least 1 skill that signals where they're heading, not just where they are

Bad top-5 pin order (generic):
1. Communication
2. Leadership
3. Project Management
4. Microsoft Office
5. Teamwork

Good top-5 pin order (engineer pivoting to AI):
1. AI Agents
2. Large Language Models (LLM)
3. Python
4. n8n
5. Prompt Engineering

Good top-5 pin order (designer):
1. Product Design
2. Design Systems
3. Figma
4. User Research
5. Brand Systems

Good top-5 pin order (founder):
1. Product Strategy
2. Fundraising (if true)
3. Customer Discovery
4. Hiring
5. Go-to-Market Strategy

---

## What to never add

- Generic skills with no work anchor: "Hard Worker", "Detail-Oriented", "Self-Starter"
- Acronyms the user can't explain on demand
- Tools the user has not personally shipped with
- More than 35 skills — diminishing returns
- Skills that contradict the user's positioning (e.g. "Sales" on a profile aimed at engineering roles)
- The same concept twice (don't have both "JavaScript" and "JS" — LinkedIn treats them differently)
