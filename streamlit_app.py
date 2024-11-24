import streamlit as st
import pandas as pd
from decimal import Decimal, InvalidOperation

# Configure Streamlit page settings
st.set_page_config(
    page_title="Shopping Expense Splitter",
    page_icon="🛍️",
    layout="centered",
    initial_sidebar_state="collapsed"  # Improve initial load time
)

# Custom CSS for better alignment
st.markdown("""
    <style>
    .stTextInput > label { display: none; }
    .stCheckbox { margin-top: 0px !important; }
    .stCheckbox > label { font-size: 0.9rem; }
    div[data-testid="column"] { gap: 0rem; }
    /* Reduce spacing between rows */
    .row-widget { margin-bottom: -1rem; }
    </style>
""", unsafe_allow_html=True)

# Initialize session state more efficiently
if "entries" not in st.session_state:
    st.session_state.entries = [{"cost": "", "Mustafa": False, "Adhi": False, "Karan": False}]
if "last_entry_count" not in st.session_state:
    st.session_state.last_entry_count = 1

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
    previous_value = entry["cost"]
    current_value = cols[0].text_input(
        "Cost",
        value=entry["cost"],
        key=f"cost_{index}",
        placeholder=f"Item {index + 1} amount",
        label_visibility="collapsed"
    )
    
    # If this is the last row and user started typing, add a new row
    if (index == len(st.session_state.entries) - 1 and 
        current_value and 
        current_value != previous_value):
        st.session_state.entries.append({"cost": "", "Mustafa": False, "Adhi": False, "Karan": False})
        form_changed = True
    
    entry["cost"] = current_value
    
    # Checkboxes
    entry["Mustafa"] = cols[1].checkbox("Mustafa", value=entry["Mustafa"], key=f"Mustafa_{index}")
    entry["Adhi"] = cols[2].checkbox("Adhi", value=entry["Adhi"], key=f"Adhi_{index}")
    entry["Karan"] = cols[3].checkbox("Karan", value=entry["Karan"], key=f"Karan_{index}")
    
    # Delete button - collect indices to delete after the loop
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

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 0.8em;'>
    💡 Start typing to add new rows automatically
    </div>
""", unsafe_allow_html=True)
