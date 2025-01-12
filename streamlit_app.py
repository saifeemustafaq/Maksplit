import streamlit as st
import pandas as pd
from decimal import Decimal, InvalidOperation

# Configure Streamlit page settings
st.set_page_config(
    page_title="Shopping Expense Splitter",
    page_icon="🛍️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better alignment and to hide default menu items
st.markdown("""
    <style>
    .stTextInput > label { display: none; }
    .stCheckbox { margin-top: 0px !important; }
    .stCheckbox > label { font-size: 0.9rem; }
    div[data-testid="column"] { gap: 0rem; }
    /* Reduce spacing between rows */
    .row-widget { margin-bottom: -1rem; }
    
    /* Hide all default menu items */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}
    
    /* Retro-style GitHub button */
    .custom-github-btn {
        position: fixed;
        right: 1rem;
        top: 1rem;
        padding: 0.7rem 1.2rem;
        background: #ffd700;
        color: #000000;
        border-radius: 0;
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 0.7rem;
        font-size: 0.8rem;
        font-family: 'Press Start 2P', monospace;
        text-transform: uppercase;
        border: 3px solid #000000;
        box-shadow: 4px 4px 0px #000000;
        transition: all 0.1s ease;
        z-index: 1000;
    }
    
    .custom-github-btn:hover {
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0px #000000;
        background: #ffed4a;
    }
    
    .custom-github-btn:active {
        transform: translate(4px, 4px);
        box-shadow: 0px 0px 0px #000000;
    }

    .github-logo {
        width: 20px;
        height: 20px;
        display: inline-block;
    }
    </style>
    
    <!-- Import Google Font -->
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
    
    <!-- Custom GitHub button -->
    <a href="https://www.linkedin.com/posts/saifeemustafa_shopping-expense-splitter-activity-7284066826970435584-A-Kj" 
       target="_blank" 
       class="custom-github-btn">
        Fork this app
        <svg class="github-logo" viewBox="0 0 24 24" fill="#000000">
            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
        </svg>
    </a>
""", unsafe_allow_html=True)

# Initialize session state more efficiently
if "entries" not in st.session_state:
    st.session_state.entries = [{"cost": "", "Mustafa": False, "Adhi": False, "Karan": False}]
if "last_entry_count" not in st.session_state:
    st.session_state.last_entry_count = 1
if "active_index" not in st.session_state:
    st.session_state.active_index = 0

def move_to_next_row(current_index):
    """Move focus to the next row's text input"""
    if current_index < len(st.session_state.entries) - 1:
        st.session_state.active_index = current_index + 1
        return True
    return False

def process_input_text(text: str) -> tuple[str, dict]:
    """
    Process the input text to extract amount and determine which checkboxes should be ticked.
    Returns a tuple of (cleaned_amount, checkbox_states)
    """
    # Initialize checkbox states
    checkbox_states = {
        "Mustafa": False,
        "Adhi": False,
        "Karan": False
    }
    
    # Convert text to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # Check for special characters
    if 'm' in text_lower:
        checkbox_states["Mustafa"] = True
    if 'a' in text_lower:
        checkbox_states["Adhi"] = True
    if 'k' in text_lower:
        checkbox_states["Karan"] = True
    
    # Extract numbers from the text
    cleaned_amount = ''.join(c for c in text if c.isdigit() or c == '.' or c == '-')
    
    return cleaned_amount, checkbox_states

def handle_input_change(index: int):
    """Handle input changes and focus management"""
    # Get the current value from the input
    current_value = st.session_state[f"cost_{index}"]
    cleaned_amount, checkbox_states = process_input_text(current_value)
    
    # Update the entry in the session state
    st.session_state.entries[index]["cost"] = cleaned_amount
    st.session_state.entries[index]["Mustafa"] = checkbox_states["Mustafa"]
    st.session_state.entries[index]["Adhi"] = checkbox_states["Adhi"]
    st.session_state.entries[index]["Karan"] = checkbox_states["Karan"]

def is_valid_number(value: str) -> bool:
    """Validate if the input string is a valid positive number."""
    if not value.strip():
        return True
    try:
        num = Decimal(value)
        return num >= 0
    except InvalidOperation:
        return False

def calculate_totals():
    """Calculate split expenses in real-time."""
    totals = {"Mustafa": Decimal('0'), "Adhi": Decimal('0'), "Karan": Decimal('0')}
    
    for entry in st.session_state.entries:
        if not entry["cost"].strip():
            continue
        try:
            cost = Decimal(entry["cost"])
            if cost < 0:
                continue
            selected_people = [key for key in ["Mustafa", "Adhi", "Karan"] if entry[key]]
            if selected_people:
                split_cost = cost / len(selected_people)
                for person in selected_people:
                    totals[person] += split_cost
        except InvalidOperation:
            continue
    
    return {k: float(v.quantize(Decimal('0.01'))) for k, v in totals.items()}

# Header
st.markdown("<h1 style='text-align: center;'>Shopping Expense Splitter 🛍️</h1>", unsafe_allow_html=True)

# Dynamic form with automatic row addition
form_changed = False
entries_to_delete = []

# Process existing entries and add new ones dynamically
for index, entry in enumerate(st.session_state.entries):
    cols = st.columns([3, 1, 1, 1, 1])
    
    # Cost input
    current_value = cols[0].text_input(
        "Cost",
        value=entry["cost"],
        key=f"cost_{index}",
        placeholder=f"Item {index + 1} amount",
        label_visibility="collapsed",
        on_change=lambda i=index: handle_input_change(i)
    )
    
    # If this is the last row and user started typing, add a new row
    if index == len(st.session_state.entries) - 1 and current_value.strip():
        st.session_state.entries.append({"cost": "", "Mustafa": False, "Adhi": False, "Karan": False})
        form_changed = True
        move_to_next_row(index)
    
    # Checkboxes
    entry["Mustafa"] = cols[1].checkbox("Mustafa", value=entry["Mustafa"], key=f"Mustafa_{index}")
    entry["Adhi"] = cols[2].checkbox("Adhi", value=entry["Adhi"], key=f"Adhi_{index}")
    entry["Karan"] = cols[3].checkbox("Karan", value=entry["Karan"], key=f"Karan_{index}")
    
    # Delete button
    if cols[4].button("🗑️", key=f"delete_{index}"):
        entries_to_delete.append(index)

# Process deletions after the loop
if entries_to_delete:
    for index in sorted(entries_to_delete, reverse=True):
        st.session_state.entries.pop(index)
    # Ensure at least one row exists
    if not st.session_state.entries:
        st.session_state.entries.append({"cost": "", "Mustafa": False, "Adhi": False, "Karan": False})
    st.rerun()

# Calculate and display totals
totals = calculate_totals()

if any(totals.values()):
    st.markdown("---")
    st.subheader("💰 Total Split")
    
    cols = st.columns(3)
    for i, (person, amount) in enumerate(totals.items()):
        cols[i].metric(
            label=f"{person}'s Share",
            value=f"${amount:.2f}"
        )
    
    # Add total sum
    total_sum = sum(totals.values())
    st.markdown("---")
    st.markdown(f"""
        <div style='text-align: center; padding: 1rem; background-color: #f0f2f6; border-radius: 0.5rem;'>
            <h3 style='margin: 0;'>Total Amount: <span style='color: #ff4b4b;'>${total_sum:.2f}</span></h3>
        </div>
    """, unsafe_allow_html=True)

# App Guide Section
st.markdown("---")

# About section
st.subheader("📱 About This App")
st.write("""
While Splitwise is a popular expense-sharing app, it has limitations that can make it frustrating for quick, multiple-item splits:

- **Splitwise's Limitations:**
    - Limited to 2 free entries before blocking functionality
    - Requires multiple steps to split each item
    - Time-consuming for bulk entries (imagine splitting 50 shopping items!)
    - Needs login and setup

- **Our Solution:**
    - ⚡ Instant item addition with no limits
    - 🎯 Quick-entry with initials (e.g., "100mk" for instant split)
    - 🧮 Automatic split calculations (no manual calculator needed)
    - 🚀 No login, no setup - just start splitting!

Perfect for shopping trips where you're buying multiple items and need to split them quickly without the hassle of going through multiple steps for each item.
""")

# Quick Tips section
st.write("### ✨ Quick Tips")
st.write("""
- **Quick Entry:** Type amount followed by initials (m, a, k) to auto-select people
- **Examples:**
    - "100m" → $100 for Mustafa only
    - "50mk" → $50 split between Mustafa and Karan
    - "75mak" → $75 split equally among all three
- **Navigation:** Use Tab or Enter to move between fields
- **Delete:** Use the 🗑️ button to remove any entry
""")

# Use Cases section
st.write("### 💡 Use Cases")
st.write("""
- **Shopping Trips:** Quick split for groceries or mall purchases
- **Restaurant Bills:** Instantly divide shared and individual items
- **Group Activities:** Split tickets, rentals, or any shared expenses
""")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 0.8em;'>
    💡 Type amount followed by 'm', 'a', or 'k' to auto-select people (e.g., "100mk" for Mustafa and Karan)
    </div>
""", unsafe_allow_html=True)
