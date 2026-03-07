# Product Requirements Document (PRD)

## MakSplit — Shopping Expense Splitter

| Field             | Detail                                     |
|-------------------|--------------------------------------------|
| **Product Name**  | MakSplit (Shopping Expense Splitter)       |
| **Author**        | Mustafa Saifee                             |
| **Status**        | v1.0 — Shipped                             |
| **Last Updated**  | March 2026                                 |
| **Platform**      | Web (Streamlit)                            |
| **Stack**         | Python, Streamlit, Pandas, Decimal         |

---

## 1. Executive Summary

MakSplit is a zero-friction, browser-based expense splitting tool purpose-built for **multi-item shopping trips**. Unlike general-purpose expense-sharing apps (e.g., Splitwise), MakSplit eliminates signup walls, entry limits, and multi-step workflows. Users type an item's cost, tag who it's for, and see real-time per-person totals — all in a single screen with no account required.

The product targets a narrow but high-frequency pain point: splitting a receipt with many line items across a small group, fast, at the checkout counter or in the parking lot.

---

## 2. Problem Statement

### 2.1 The Core Problem

Splitting expenses after a shared shopping trip is disproportionately tedious relative to the simplicity of the task. Existing tools force users through heavyweight flows — account creation, group setup, per-item entry wizards — that are over-engineered for the common scenario of "we just bought 30 items at Costco and need to know who owes what."

### 2.2 Pain Points (Validated)

| #  | Pain Point | Severity | Frequency |
|----|-----------|----------|-----------|
| P1 | **Entry limits behind paywalls.** Splitwise restricts free users to a small number of itemized entries, making bulk receipt splitting impossible without a subscription. | High | Every use |
| P2 | **Multi-step item entry.** Each expense in Splitwise requires: navigate → add expense → enter amount → select people → confirm. For 50 items, this is 200+ taps. | High | Every use |
| P3 | **Mandatory account creation.** Users must sign up, verify email, and create a group before splitting a single dollar. This is a hard blocker for spontaneous use. | High | First use |
| P4 | **No quick-input shorthand.** There is no way to rapidly enter both the amount and the split assignment in a single action. Users toggle between text fields and selection UIs. | Medium | Every use |
| P5 | **Mental math overhead.** Without a tool, users resort to calculator apps and manual tracking, leading to rounding errors and disputes. | Medium | Every use |
| P6 | **Overkill for simple groups.** Most expense-sharing apps are designed for ongoing groups (roommates, travel companions). A one-off shopping trip doesn't warrant the setup overhead. | Medium | Situational |

### 2.3 Who Feels This Pain?

- **Roommates / housemates** splitting grocery runs
- **Friends** on group shopping outings (malls, big-box stores)
- **Couples or small groups** dining out with a mix of shared and individual items
- **Travel groups** splitting miscellaneous purchases on the go

---

## 3. Solution Overview

MakSplit solves the above by collapsing the entire expense-splitting workflow into a **single-screen, zero-auth, real-time form**.

### 3.1 Problem ↔ Solution Mapping

| Pain Point | MakSplit Solution |
|-----------|-------------------|
| Entry limits behind paywalls | Unlimited entries, completely free, no paywall |
| Multi-step item entry | Single-row entry: type cost → tick names → done |
| Mandatory account creation | Zero auth — open the URL and start |
| No quick-input shorthand | **Quick-entry syntax**: `100mr` = $100 split between Mustafa and Rohit |
| Mental math overhead | Real-time per-person totals with precise Decimal arithmetic |
| Overkill for simple groups | Lightweight, disposable session; no group setup |

### 3.2 Key Design Principles

1. **Speed over features.** Every interaction should feel instant. No modals, no multi-page flows, no confirmations.
2. **Zero barrier to entry.** No signup, no installation, no configuration. A shareable URL is the entire onboarding.
3. **Opinionated defaults, flexible overrides.** Ship with a sensible default group (3 core members) but allow temporary members to be added on the fly.
4. **Real-time feedback.** Totals update as the user types. There is no "calculate" button.

---

## 4. Jobs To Be Done (JTBD)

### Primary JTBD

> **When** I finish a shared shopping trip with friends,
> **I want to** quickly figure out how much each person owes,
> **so that** we can settle up immediately without arguments or lingering debts.

### Supporting JTBDs

| # | Job Statement |
|---|--------------|
| J1 | **When** I'm standing at the checkout counter, **I want to** split items as I scan the receipt line by line, **so that** I don't have to remember or re-enter anything later. |
| J2 | **When** some items are shared and others are individual, **I want to** assign each item to specific people, **so that** the split is fair and precise. |
| J3 | **When** a friend who isn't a regular member joins the trip, **I want to** add them temporarily without disrupting the existing setup, **so that** they're included in the split. |
| J4 | **When** I make an entry mistake, **I want to** correct or delete it instantly, **so that** errors don't compound into the final totals. |
| J5 | **When** I'm entering many items quickly, **I want to** use a keyboard shorthand to specify both amount and people, **so that** I can go faster than clicking checkboxes. |

---

## 5. User Personas

### Persona 1: "The Builder & Splitter" — Mustafa (MS)

| Attribute | Detail |
|-----------|--------|
| Age | 28 |
| Context | Built MakSplit to solve his own problem; regularly shops with Rohit and Akhil |
| Goal | Split 30-50 items per trip quickly and accurately without the overhead of Splitwise |
| Frustration | Splitwise's free tier blocks him after a few entries; ends up using a spreadsheet or mental math |
| Tech comfort | High; built the tool himself, appreciates keyboard shortcuts and efficient UIs |

### Persona 2: "The Spontaneous Organizer" — Rohit (RS)

| Attribute | Detail |
|-----------|--------|
| Age | 29 |
| Context | Frequently joins group shopping trips and dinners; often the one holding the receipt |
| Goal | Split a bill or group shopping haul on the spot without back-and-forth later |
| Frustration | Doesn't want to create a Splitwise group for every ad-hoc outing or deal with entry limits |
| Tech comfort | High; appreciates fast, no-nonsense tools |

### Persona 3: "The Quick Settler" — Akhil (AD)

| Attribute | Detail |
|-----------|--------|
| Age | 27 |
| Context | Splits groceries, dining, and group purchases with Mustafa and Rohit regularly |
| Goal | Avoid the "I think you owe me $12?" text message chain; settle up immediately |
| Frustration | Doesn't want to sign up for yet another app just to split a Costco run |
| Tech comfort | High; mobile-first user |

---

## 6. Use Cases

### UC-1: Standard Multi-Item Receipt Split

**Actor:** Mustafa (The Builder & Splitter)
**Precondition:** Mustafa, Rohit, and Akhil just finished a Costco run.

| Step | Action |
|------|--------|
| 1 | Mustafa opens the MakSplit URL on his phone. |
| 2 | He reads the first item on the receipt: "Paper Towels — $15.99". |
| 3 | He types `15.99` in the first row and checks all 3 names (shared item). |
| 4 | Next item: "Mustafa's protein bars — $8.49". He types `8.49` and checks only MS. |
| 5 | He repeats for all 40 items. A new row auto-appears as he fills each one. |
| 6 | The right-side card shows real-time per-person totals. |
| 7 | He reads out: "MS owes $62.40, AD owes $55.12, RS owes $48.88." |

**Postcondition:** Everyone knows their share. Mustafa sends a quick Venmo request based on the totals.

---

### UC-2: Quick-Entry Shorthand for Power Users

**Actor:** Rohit (The Spontaneous Organizer)
**Precondition:** Rohit is splitting a restaurant bill with Mustafa and Akhil.

| Step | Action |
|------|--------|
| 1 | Rohit opens MakSplit. |
| 2 | He types `25mra` — the app parses this as $25 split among Mustafa, Rohit, and Akhil. Checkboxes auto-tick. |
| 3 | He types `18mr` — $18 split between Mustafa and Rohit only. |
| 4 | He types `12a` — $12 for Akhil only (individual dessert). |
| 5 | Totals update in real-time. |

**Postcondition:** Bill is split in under 30 seconds without touching a single checkbox.

---

### UC-3: Adding a Temporary Member

**Actor:** Rohit
**Precondition:** A friend "Sam" joins an outing that normally involves only Mustafa, Rohit, and Akhil.

| Step | Action |
|------|--------|
| 1 | Rohit types "Sam" in the "Add temporary member" field and clicks "Add Member". |
| 2 | Sam appears as a new checkbox column in the item entry form. |
| 3 | Rohit enters items, assigning some to Sam as needed. |
| 4 | After the outing, Rohit clicks the "X Sam" button to remove the temporary member. |

**Postcondition:** Sam is included in the split for this session only. Core group remains unchanged.

---

### UC-4: Correcting an Entry Error

**Actor:** Akhil
**Precondition:** Akhil mistyped an item cost.

| Step | Action |
|------|--------|
| 1 | Akhil notices row 7 says $55 instead of $5.50. |
| 2 | Akhil clicks the cost field for row 7 and corrects it to `5.50`. |
| 3 | Totals recalculate instantly. |
| 4 | Alternatively, Akhil clicks the trash icon to delete the row entirely and re-enters it. |

**Postcondition:** Totals reflect the corrected amount with zero delay.

---

### UC-5: Deleting an Entry

**Actor:** Any user
**Precondition:** User entered a duplicate or incorrect row.

| Step | Action |
|------|--------|
| 1 | User clicks the trash icon on the row to delete. |
| 2 | Row is removed. If it was the last row, a fresh empty row replaces it. |
| 3 | Totals recalculate. |

**Postcondition:** Unwanted entry is gone; at least one empty row always remains for new input.

---

## 7. User Journeys

### Journey 1: First-Time User — "Cold Start to First Split"

```
Open URL → See single-screen UI → Enter first item cost
    → Check names for that item → See totals update
    → Enter remaining items → Read final per-person totals
    → Settle up externally (Venmo, cash, etc.)
```

**Time to value:** < 10 seconds (no signup, no onboarding, no tutorial).

**Key moments of delight:**
- Instant load, no auth wall
- First total appears the moment the first item is assigned
- New row auto-appears — no "add row" button needed

---

### Journey 2: Returning User — "Weekly Grocery Split"

```
Open URL (bookmarked) → Session starts fresh
    → Add items using quick-entry shorthand (e.g., "15.99mr")
    → Checkboxes auto-tick → Totals update
    → Repeat for all items → Share totals → Done
```

**Key efficiency gain:** Quick-entry syntax eliminates ~60% of manual interactions compared to click-based splitting.

---

### Journey 3: Ad-Hoc Group — "One-Off Dinner with Extra Guest"

```
Open URL → Add temporary member "Sam"
    → Layout adjusts to accommodate 4th column
    → Enter items, assigning to various subsets of 4 people
    → Read totals → Remove "Sam" when done
```

**Key flexibility point:** Temporary members are fully integrated into the split logic without affecting the base group configuration.

---

## 8. Functional Requirements

### 8.1 Core Features

| ID | Feature | Description | Priority |
|----|---------|-------------|----------|
| F1 | **Item Entry** | Users enter a cost per row. Each row has checkboxes for all group members. | P0 |
| F2 | **Real-Time Totals** | Per-person and grand totals recalculate on every input change. | P0 |
| F3 | **Quick-Entry Syntax** | Typing initials after a number auto-ticks the corresponding checkboxes (`100mr` → MS + RS). | P0 |
| F4 | **Auto Row Addition** | A new empty row appears automatically when the user begins typing in the last row. | P0 |
| F5 | **Row Deletion** | Each row has a delete button. Deleting the last row replaces it with a fresh empty row. | P0 |
| F6 | **Temporary Members** | Users can add/remove ad-hoc members. All entries retroactively include the new member as a column. | P1 |
| F7 | **Clear All Temp Members** | One-click removal of all temporary members. | P1 |
| F8 | **Input Validation** | Non-numeric and negative values are gracefully ignored in calculations. | P1 |
| F9 | **Precise Arithmetic** | All calculations use Python's `Decimal` type to avoid floating-point rounding errors. | P1 |
| F10 | **Responsive Layout** | Three-column layout (default) collapses to two-column when temporary members expand the checkbox row. | P2 |

### 8.2 UI/UX Requirements

| ID | Requirement | Detail |
|----|------------|--------|
| U1 | Single-screen experience | All functionality must be accessible without scrolling to a different page or opening a modal. |
| U2 | Hidden chrome | Streamlit's default header, footer, toolbar, and hamburger menu are hidden for a clean, app-like feel. |
| U3 | Visual hierarchy | Total Split card uses blue accent; Total Amount card uses gold/amber accent; delete buttons are de-emphasized. |
| U4 | Empty state messaging | When no items are entered, the Total Split card displays "Add items to see splits" placeholder text. |
| U5 | Wide layout | The app uses Streamlit's `layout="wide"` with reduced container padding to maximize horizontal space. |

---

## 9. Non-Functional Requirements

| ID | Category | Requirement |
|----|----------|-------------|
| NF1 | **Performance** | Total recalculation must complete in < 50ms for up to 200 entries. |
| NF2 | **Accessibility** | The app must be usable via keyboard-only navigation (Tab/Enter between fields). |
| NF3 | **Availability** | Hosted on Streamlit Community Cloud for 99.9% uptime (platform SLA). |
| NF4 | **Data Privacy** | No data is persisted server-side. All state lives in the browser session and is discarded on close. |
| NF5 | **Zero Dependencies (User-Side)** | No installation, no plugins, no mobile app download. Works in any modern browser. |
| NF6 | **Precision** | Financial calculations use `Decimal` with 2-decimal-place quantization. No floating-point artifacts. |

---

## 10. Information Architecture

```
┌──────────────────────────────────────────────────────┐
│  [Add Temporary Member] [Add] [Clear All]            │ ← Member management bar
│  Temporary members: [X Sam] [X Jordan]               │ ← Removable chips
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐  ┌──────────────────┐  ┌────────┐ │
│  │  Total Split  │  │   Add Items      │  │ Total  │ │
│  │              │  │                  │  │ Amount │ │
│  │              │  │ [Cost] [MS][AD]  │  │        │ │
│  │ MS(Mustafa): │  │        [RS][🗑️] │  │ $X.XX  │ │
│  │   $X.XX      │  │ [Cost] [MS][AD]  │  │        │ │
│  │ AD(Akhil):   │  │        [RS][🗑️] │  │        │ │
│  │   $X.XX      │  │ ...              │  │        │ │
│  │ RS(Rohit):   │  │ [auto new row]   │  │        │ │
│  │   $X.XX      │  │                  │  │        │ │
│  └──────────────┘  └──────────────────┘  └────────┘ │
├──────────────────────────────────────────────────────┤
│  About · Quick Tips · Use Cases · Footer             │ ← Informational sections
└──────────────────────────────────────────────────────┘
```

When temporary members are added, the layout shifts to a 2-column arrangement (form left, cards stacked right) to accommodate the wider checkbox row.

---

## 11. Competitive Landscape

| Dimension | Splitwise | MakSplit |
|-----------|-----------|----------|
| **Signup required** | Yes (email + verification) | No |
| **Free entry limit** | ~2 itemized entries | Unlimited |
| **Per-item entry steps** | 4-5 taps/clicks | 1 row (type + check) |
| **Quick-entry shorthand** | No | Yes (`100mr` syntax) |
| **Real-time totals** | No (must save first) | Yes (on every keystroke) |
| **Temporary members** | Requires group modification | One-click add/remove |
| **Optimized for** | Ongoing group balances | One-off multi-item splits |
| **Persistent history** | Yes | No (session only) |
| **Settlement tracking** | Yes | No (out of scope) |
| **Mobile app** | Native iOS/Android | Responsive web |

**Positioning:** MakSplit does not compete with Splitwise's full ledger and settlement capabilities. It targets the **narrow, high-frequency job** of splitting a single receipt with many line items — a job Splitwise handles poorly due to its generalist architecture.

---

## 12. Metrics & Success Criteria

### North Star Metric

**Items entered per session** — a proxy for whether users trust the tool enough to enter an entire receipt rather than abandoning partway.

### Supporting Metrics

| Metric | Target | Rationale |
|--------|--------|-----------|
| Time to first entry | < 10s | Measures zero-friction onboarding |
| Session completion rate | > 80% | % of sessions where user enters 3+ items (signals real use vs. bounce) |
| Quick-entry adoption rate | > 30% | % of entries using the shorthand syntax |
| Temp member usage rate | Track baseline | Understand how often ad-hoc groups deviate from default |
| Items per session (median) | > 10 | Confirms the tool is used for bulk splitting, not one-off calculations |

---

## 13. Assumptions & Constraints

### Assumptions

1. The primary use case involves **small groups (2-6 people)** splitting **many items (10-50+)**.
2. Users do not need persistent history — they settle up immediately and move on.
3. The default group (MS = Mustafa, AD = Akhil, RS = Rohit) represents the app creator's personal group; a generalized version would make all members configurable.
4. Quick-entry syntax is discoverable through the in-app guide; no external onboarding is needed.

### Constraints

1. **Streamlit platform limitations:** No native mobile app; limited control over input focus management; session state is ephemeral.
2. **No backend / database:** All state is client-session-scoped. Closing the browser tab loses all data.
3. **No authentication layer:** There is no concept of user identity, which precludes features like saved groups or expense history.

---

## 14. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| User accidentally closes tab, losing all entries | High | Medium | Future: Add "Copy totals to clipboard" or browser `beforeunload` warning |
| Quick-entry syntax is not discovered by new users | Medium | Medium | In-app guide section explains syntax with examples; footer hint persists |
| Large number of temporary members breaks layout | Low | Low | Layout dynamically switches from 3-col to 2-col; CSS handles overflow |
| Decimal precision edge cases | Low | Medium | All arithmetic uses Python `Decimal` with explicit `quantize` to 2 decimal places |
| Streamlit Community Cloud downtime | Low | High | Self-hosting option via Docker (devcontainer provided) |

---

## 15. Future Roadmap (Backlog)

| Priority | Feature | Description |
|----------|---------|-------------|
| Next | **Configurable default members** | Replace hardcoded MS/AD/RS with a first-run setup flow |
| Next | **Copy / share totals** | One-click copy of the summary to clipboard for sharing via text/chat |
| Later | **Receipt photo OCR** | Upload a receipt photo; auto-populate item rows via OCR |
| Later | **Settlement suggestions** | "Mustafa pays Rohit $12.40" — net settlement instructions to minimize transactions |
| Later | **Session persistence** | Optional localStorage or URL-encoded state so refreshing doesn't lose data |
| Later | **Currency selector** | Support for non-USD currencies with locale-aware formatting |
| Later | **Export to CSV** | Download the full itemized split as a spreadsheet |
| Explore | **PWA wrapper** | Installable progressive web app for a native-like mobile experience |

---

## 16. Glossary

| Term | Definition |
|------|-----------|
| **Quick-entry syntax** | A shorthand where the user types a number followed by member initials (e.g., `100mr` for Mustafa and Rohit) to simultaneously set the cost and auto-select the relevant checkboxes. |
| **Temporary member** | A group member added for the current session only, not part of the hardcoded default group. |
| **Entry / Row** | A single line item in the expense form, consisting of a cost field, member checkboxes, and a delete button. |
| **Split** | The calculated per-person share of an item, derived by dividing the item cost equally among selected members. |
| **Session** | A single browser session. All data is ephemeral and tied to the Streamlit session state. |

---

## Appendix A: Technical Architecture

```
Browser (User)
    │
    ▼
Streamlit Frontend (Python-rendered HTML/JS)
    │
    ├── Session State (st.session_state)
    │       ├── entries[]        → list of {cost, MS, AD, RS, ...temp_members}
    │       ├── temp_members[]   → list of temporary member names
    │       ├── active_index     → tracks focus row
    │       └── last_entry_count → tracks row count
    │
    ├── Input Processing
    │       ├── process_input_text()  → parses quick-entry syntax
    │       ├── handle_input_change() → syncs input to state
    │       └── handle_checkbox_change() → syncs checkbox to state
    │
    ├── Calculation Engine
    │       ├── calculate_totals()    → Decimal-based split math
    │       └── is_valid_number()     → input validation
    │
    └── Rendering
            ├── Dynamic column layout (3-col or 2-col)
            ├── Custom HTML/CSS cards for totals
            └── Informational sections (About, Tips, Use Cases)
```

---

## Appendix B: Quick-Entry Syntax Reference

The quick-entry parser operates by scanning the input string for alphabetic characters that match member initials:

| Character | Matches Member | Case Sensitive? |
|-----------|---------------|-----------------|
| `m`       | MS (Mustafa)  | No              |
| `a`       | AD (Akhil)    | No              |
| `r`       | RS (Rohit)    | No              |

**Parsing rules:**
1. All alphabetic characters are stripped; remaining digits and `.` form the cost.
2. Presence of `m` anywhere in the string checks the MS (Mustafa) box.
3. Presence of `a` anywhere in the string checks the AD (Akhil) box.
4. Presence of `r` anywhere in the string checks the RS (Rohit) box.
5. Temporary members are not currently addressable via quick-entry syntax (checkbox-only).

**Examples:**

| Input | Parsed Cost | MS | AD | RS |
|-------|-------------|----|----|-----|
| `100` | 100 | - | - | - |
| `100m` | 100 | Yes | - | - |
| `50mr` | 50 | Yes | - | Yes |
| `75mra` | 75 | Yes | Yes | Yes |
| `25a` | 25 | - | Yes | - |

---

*End of document.*
