import streamlit as st
import pandas as pd
from decimal import Decimal, InvalidOperation

# Configure Streamlit page settings
st.set_page_config(
    page_title="Shopping Expense Splitter",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize temporary members in session state
if "temp_members" not in st.session_state:
    st.session_state.temp_members = []

# Get the appropriate names based on the state
def get_names():
    base_names = ["MS", "AD", "RS"]
    return base_names + st.session_state.temp_members

# Custom CSS for better alignment and to hide default menu items
st.markdown("""
    <style>
    .stTextInput > label { display: none; }
    .stCheckbox { margin-top: 0px !important; }
    .stCheckbox > label { font-size: 0.9rem; }
    div[data-testid="column"] { gap: 0rem; }
    /* Reduce spacing between rows */
    .row-widget { margin-bottom: -1rem; }
    
    /* Reduce main container padding for wider layout */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }
    
    /* Ensure columns have proper spacing */
    .stColumns > div {
        padding: 0 0.5rem;
    }
    
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
    st.session_state.entries = [{"cost": "", **{name: False for name in get_names()}}]
if "last_entry_count" not in st.session_state:
    st.session_state.last_entry_count = 1
if "active_index" not in st.session_state:
    st.session_state.active_index = 0
if "show_tax" not in st.session_state:
    st.session_state.show_tax = False
if "show_delivery" not in st.session_state:
    st.session_state.show_delivery = False
if "tax_amount" not in st.session_state:
    st.session_state.tax_amount = ""
if "delivery_amount" not in st.session_state:
    st.session_state.delivery_amount = ""

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
    names = get_names()
    checkbox_states = {name: False for name in names}
    
    # Convert text to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # Check for special characters
    if 'm' in text_lower:
        checkbox_states["MS"] = True
    if 'r' in text_lower:
        checkbox_states["RS"] = True
    if 'a' in text_lower:
        checkbox_states["AD"] = True
    
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
    names = get_names()
    for name in names:
        st.session_state.entries[index][name] = checkbox_states[name]
        st.session_state[f"{name}_{index}"] = checkbox_states[name]

def handle_checkbox_change(index: int, name: str):
    """Handle checkbox changes"""
    # Get the current checkbox value from the session state
    checkbox_key = f"{name}_{index}"
    if checkbox_key in st.session_state:
        st.session_state.entries[index][name] = st.session_state[checkbox_key]

def handle_tax_input_change(widget_key: str):
    st.session_state.tax_amount = st.session_state[widget_key]

def handle_delivery_input_change(widget_key: str):
    st.session_state.delivery_amount = st.session_state[widget_key]

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
    """Calculate split expenses with pro-rata tax and delivery."""
    names = get_names()
    subtotals = {name: Decimal('0') for name in names}
    
    for entry in st.session_state.entries:
        if not entry["cost"].strip():
            continue
        try:
            cost = Decimal(entry["cost"])
            if cost < 0:
                continue
            selected_people = [key for key in names if entry[key]]
            if selected_people:
                split_cost = cost / len(selected_people)
                for person in selected_people:
                    subtotals[person] += split_cost
        except InvalidOperation:
            continue
    
    grand_subtotal = sum(subtotals.values())
    
    tax_val = Decimal('0')
    delivery_val = Decimal('0')
    if st.session_state.show_tax and st.session_state.tax_amount.strip():
        try:
            tv = Decimal(st.session_state.tax_amount)
            if tv >= 0:
                tax_val = tv
        except InvalidOperation:
            pass
    if st.session_state.show_delivery and st.session_state.delivery_amount.strip():
        try:
            dv = Decimal(st.session_state.delivery_amount)
            if dv >= 0:
                delivery_val = dv
        except InvalidOperation:
            pass

    extras = tax_val + delivery_val
    totals = dict(subtotals)
    if extras > 0 and grand_subtotal > 0:
        for name in names:
            proportion = subtotals[name] / grand_subtotal
            totals[name] = subtotals[name] + extras * proportion

    result_totals = {k: float(v.quantize(Decimal('0.01'))) for k, v in totals.items()}
    result_subtotals = {k: float(v.quantize(Decimal('0.01'))) for k, v in subtotals.items()}
    return result_totals, result_subtotals, float(tax_val.quantize(Decimal('0.01'))), float(delivery_val.quantize(Decimal('0.01')))

# Add temporary member section
st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    new_member = st.text_input("Add temporary member", placeholder="Enter name (e.g., Ram)", key="new_member_input")

with col2:
    if st.button("Add Member", key="add_member_button"):
        if new_member.strip() and new_member.strip() not in get_names():
            st.session_state.temp_members.append(new_member.strip())
            # Add the new member to all existing entries
            for entry in st.session_state.entries:
                entry[new_member.strip()] = False
            st.rerun()
        elif new_member.strip() in get_names():
            st.error("Member already exists!")

with col3:
    if st.button("Clear All", key="clear_temp_members_button"):
        st.session_state.temp_members = []
        # Remove temp members from all entries
        for entry in st.session_state.entries:
            for temp_member in st.session_state.temp_members:
                if temp_member in entry:
                    del entry[temp_member]
        st.rerun()

# Show current temporary members with individual remove buttons
if st.session_state.temp_members:
    st.markdown("**Temporary members:**")
    member_cols = st.columns(len(st.session_state.temp_members))
    for idx, member in enumerate(st.session_state.temp_members):
        with member_cols[idx]:
            if st.button(f"❌ {member}", key=f"remove_temp_{idx}"):
                st.session_state.temp_members.remove(member)
                for entry in st.session_state.entries:
                    entry.pop(member, None)
                st.rerun()
    st.markdown("---")

# Header
st.markdown("<h1 style='text-align: center;'>Shopping Expense Splitter 🛍️</h1>", unsafe_allow_html=True)

# Calculate totals
totals, subtotals, tax_applied, delivery_applied = calculate_totals()
subtotal_sum = sum(subtotals.values())
total_sum = sum(totals.values())

# Check if we have temporary members to determine layout
has_temp_members = len(st.session_state.temp_members) > 0

if has_temp_members:
    # When temporary members exist, use two-column layout: Left (Form), Right (Cards stacked)
    left_col, right_col = st.columns([3, 1])
    
    with left_col:
        # Main expense splitter form
        st.markdown("### 🛍️ Add Items")
        
        # Dynamic form with automatic row addition
        form_changed = False
        entries_to_delete = []

        # Process existing entries and add new ones dynamically
        for index, entry in enumerate(st.session_state.entries):
            names = get_names()
            # Create columns: cost input + checkboxes for all names + delete button
            col_weights = [3] + [1] * len(names) + [1]
            cols = st.columns(col_weights)
            
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
                st.session_state.entries.append({"cost": "", **{name: False for name in get_names()}})
                form_changed = True
                move_to_next_row(index)
            
            # Checkboxes for all names (base + temporary)
            for i, name in enumerate(names):
                cb_key = f"{name}_{index}"
                if cb_key not in st.session_state:
                    st.session_state[cb_key] = st.session_state.entries[index].get(name, False)
                entry[name] = cols[i+1].checkbox(
                    name, 
                    key=cb_key,
                    on_change=lambda i=index, n=name: handle_checkbox_change(i, n)
                )
            
            # Delete button
            delete_col_index = len(names) + 1
            if cols[delete_col_index].button("🗑️", key=f"delete_{index}"):
                entries_to_delete.append(index)

        # Process deletions after the loop
        if entries_to_delete:
            for index in sorted(entries_to_delete, reverse=True):
                st.session_state.entries.pop(index)
            if not st.session_state.entries:
                st.session_state.entries.append({"cost": "", **{name: False for name in get_names()}})
            st.rerun()

        # Tax & Delivery toggle buttons
        tax_col, delivery_col, _ = st.columns([1, 1, 2])
        with tax_col:
            if st.button("Remove Tax" if st.session_state.show_tax else "Add Tax", key="toggle_tax_temp"):
                st.session_state.show_tax = not st.session_state.show_tax
                if not st.session_state.show_tax:
                    st.session_state.tax_amount = ""
                st.rerun()
        with delivery_col:
            if st.button("Remove Delivery" if st.session_state.show_delivery else "Add Delivery", key="toggle_delivery_temp"):
                st.session_state.show_delivery = not st.session_state.show_delivery
                if not st.session_state.show_delivery:
                    st.session_state.delivery_amount = ""
                st.rerun()

        if st.session_state.show_tax or st.session_state.show_delivery:
            extra_cols = st.columns(2)
            if st.session_state.show_tax:
                with extra_cols[0]:
                    st.text_input(
                        "Tax Amount",
                        value=st.session_state.tax_amount,
                        placeholder="Enter tax amount",
                        key="tax_input_temp",
                        on_change=handle_tax_input_change,
                        args=("tax_input_temp",),
                    )
            if st.session_state.show_delivery:
                with extra_cols[1]:
                    st.text_input(
                        "Delivery Amount",
                        value=st.session_state.delivery_amount,
                        placeholder="Enter delivery amount",
                        key="delivery_input_temp",
                        on_change=handle_delivery_input_change,
                        args=("delivery_input_temp",),
                    )

    with right_col:
        # Total Split card (top)
        has_extras = tax_applied > 0 or delivery_applied > 0
        if any(totals.values()):
            splits_lines = []
            for person in totals:
                sub = subtotals[person]
                extra = totals[person] - sub
                if has_extras and extra > 0:
                    amount_html = (
                        f"<span style='color: #6c757d;'>${sub:.2f}</span>"
                        f" <span style='color: #6c757d;'>+</span> "
                        f"<span style='color: #856404;'>${extra:.2f}</span>"
                        f" <span style='color: #6c757d;'>=</span> "
                        f"<span style='font-weight: bold; color: #28a745;'>${totals[person]:.2f}</span>"
                    )
                else:
                    amount_html = f"<span style='font-weight: bold; color: #28a745;'>${totals[person]:.2f}</span>"
                splits_lines.append(
                    f"<div style='display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #e9ecef; font-size: 0.9rem;'>"
                    f"<span style='font-weight: 500;'>{person}:</span>"
                    f"<span>{amount_html}</span>"
                    f"</div>"
                )
            splits_html = "".join(splits_lines)
            st.markdown(f"""<div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem; border-left: 4px solid #007bff; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1rem;'>
<h3 style='margin: 0 0 1rem 0; color: #007bff; font-size: 1.1rem;'>💰 Total Split</h3>
{splits_html}
</div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem; border-left: 4px solid #007bff; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1rem;'>
<h3 style='margin: 0 0 1rem 0; color: #007bff; font-size: 1.1rem;'>💰 Total Split</h3>
<p style='color: #6c757d; font-size: 0.9rem; margin: 0;'>Add items to see splits</p>
</div>""", unsafe_allow_html=True)
        
        # Total Amount card (bottom)
        breakdown_lines = ""
        if tax_applied > 0 or delivery_applied > 0:
            breakdown_lines += f"<div style='font-size: 0.85rem; color: #856404; margin-bottom: 0.3rem;'>Subtotal: ${subtotal_sum:.2f}</div>"
            if tax_applied > 0:
                breakdown_lines += f"<div style='font-size: 0.85rem; color: #856404; margin-bottom: 0.3rem;'>Tax: ${tax_applied:.2f}</div>"
            if delivery_applied > 0:
                breakdown_lines += f"<div style='font-size: 0.85rem; color: #856404; margin-bottom: 0.3rem;'>Delivery: ${delivery_applied:.2f}</div>"
        st.markdown(f"""<div style='background-color: #fff3cd; padding: 1.5rem; border-radius: 0.5rem; border-left: 4px solid #ffc107; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;'>
<h3 style='margin: 0 0 1rem 0; color: #856404; font-size: 1.1rem;'>💵 Total Amount</h3>
{breakdown_lines}
<div style='font-size: 1.8rem; font-weight: bold; color: #ff4b4b;'>${total_sum:.2f}</div>
</div>""", unsafe_allow_html=True)

else:
    # When no temporary members, use three-column layout: Left (Total Split), Middle (Form), Right (Total Amount)
    left_col, middle_col, right_col = st.columns([1, 2, 1])

    with left_col:
        # Left card - Total Split
        has_extras = tax_applied > 0 or delivery_applied > 0
        if any(totals.values()):
            splits_lines = []
            for person in totals:
                sub = subtotals[person]
                extra = totals[person] - sub
                if has_extras and extra > 0:
                    amount_html = (
                        f"<span style='color: #6c757d;'>${sub:.2f}</span>"
                        f" <span style='color: #6c757d;'>+</span> "
                        f"<span style='color: #856404;'>${extra:.2f}</span>"
                        f" <span style='color: #6c757d;'>=</span> "
                        f"<span style='font-weight: bold; color: #28a745;'>${totals[person]:.2f}</span>"
                    )
                else:
                    amount_html = f"<span style='font-weight: bold; color: #28a745;'>${totals[person]:.2f}</span>"
                splits_lines.append(
                    f"<div style='display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #e9ecef; font-size: 0.9rem;'>"
                    f"<span style='font-weight: 500;'>{person}:</span>"
                    f"<span>{amount_html}</span>"
                    f"</div>"
                )
            splits_html = "".join(splits_lines)
            st.markdown(f"""<div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem; border-left: 4px solid #007bff; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1rem;'>
<h3 style='margin: 0 0 1rem 0; color: #007bff; font-size: 1.1rem;'>💰 Total Split</h3>
{splits_html}
</div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem; border-left: 4px solid #007bff; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1rem;'>
<h3 style='margin: 0 0 1rem 0; color: #007bff; font-size: 1.1rem;'>💰 Total Split</h3>
<p style='color: #6c757d; font-size: 0.9rem; margin: 0;'>Add items to see splits</p>
</div>""", unsafe_allow_html=True)

    with middle_col:
        # Main expense splitter form
        st.markdown("### 🛍️ Add Items")
        
        # Dynamic form with automatic row addition
        form_changed = False
        entries_to_delete = []

        # Process existing entries and add new ones dynamically
        for index, entry in enumerate(st.session_state.entries):
            names = get_names()
            # Create columns: cost input + checkboxes for all names + delete button
            col_weights = [3] + [1] * len(names) + [1]
            cols = st.columns(col_weights)
            
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
                st.session_state.entries.append({"cost": "", **{name: False for name in get_names()}})
                form_changed = True
                move_to_next_row(index)
            
            # Checkboxes for all names (base + temporary)
            for i, name in enumerate(names):
                cb_key = f"{name}_{index}"
                if cb_key not in st.session_state:
                    st.session_state[cb_key] = st.session_state.entries[index].get(name, False)
                entry[name] = cols[i+1].checkbox(
                    name, 
                    key=cb_key,
                    on_change=lambda i=index, n=name: handle_checkbox_change(i, n)
                )
            
            # Delete button
            delete_col_index = len(names) + 1
            if cols[delete_col_index].button("🗑️", key=f"delete_{index}"):
                entries_to_delete.append(index)

        # Process deletions after the loop
        if entries_to_delete:
            for index in sorted(entries_to_delete, reverse=True):
                st.session_state.entries.pop(index)
            if not st.session_state.entries:
                st.session_state.entries.append({"cost": "", **{name: False for name in get_names()}})
            st.rerun()

        # Tax & Delivery toggle buttons
        tax_col, delivery_col, _ = st.columns([1, 1, 2])
        with tax_col:
            if st.button("Remove Tax" if st.session_state.show_tax else "Add Tax", key="toggle_tax_main"):
                st.session_state.show_tax = not st.session_state.show_tax
                if not st.session_state.show_tax:
                    st.session_state.tax_amount = ""
                st.rerun()
        with delivery_col:
            if st.button("Remove Delivery" if st.session_state.show_delivery else "Add Delivery", key="toggle_delivery_main"):
                st.session_state.show_delivery = not st.session_state.show_delivery
                if not st.session_state.show_delivery:
                    st.session_state.delivery_amount = ""
                st.rerun()

        if st.session_state.show_tax or st.session_state.show_delivery:
            extra_cols = st.columns(2)
            if st.session_state.show_tax:
                with extra_cols[0]:
                    st.text_input(
                        "Tax Amount",
                        value=st.session_state.tax_amount,
                        placeholder="Enter tax amount",
                        key="tax_input_main",
                        on_change=handle_tax_input_change,
                        args=("tax_input_main",),
                    )
            if st.session_state.show_delivery:
                with extra_cols[1]:
                    st.text_input(
                        "Delivery Amount",
                        value=st.session_state.delivery_amount,
                        placeholder="Enter delivery amount",
                        key="delivery_input_main",
                        on_change=handle_delivery_input_change,
                        args=("delivery_input_main",),
                    )

    with right_col:
        # Right card - Total Amount
        breakdown_lines = ""
        if tax_applied > 0 or delivery_applied > 0:
            breakdown_lines += f"<div style='font-size: 0.85rem; color: #856404; margin-bottom: 0.3rem;'>Subtotal: ${subtotal_sum:.2f}</div>"
            if tax_applied > 0:
                breakdown_lines += f"<div style='font-size: 0.85rem; color: #856404; margin-bottom: 0.3rem;'>Tax: ${tax_applied:.2f}</div>"
            if delivery_applied > 0:
                breakdown_lines += f"<div style='font-size: 0.85rem; color: #856404; margin-bottom: 0.3rem;'>Delivery: ${delivery_applied:.2f}</div>"
        st.markdown(f"""<div style='background-color: #fff3cd; padding: 1.5rem; border-radius: 0.5rem; border-left: 4px solid #ffc107; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; margin-bottom: 1rem;'>
<h3 style='margin: 0 0 1rem 0; color: #856404; font-size: 1.1rem;'>💵 Total Amount</h3>
{breakdown_lines}
<div style='font-size: 1.8rem; font-weight: bold; color: #ff4b4b;'>${total_sum:.2f}</div>
</div>""", unsafe_allow_html=True)

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
names = get_names()
initials = ''.join(name[0].lower() for name in names)
st.write(f"""
- **Quick Entry:** Type amount followed by initials ({initials}) to auto-select people
- **Examples:**
    - "100m" → $100 for Mustafa only
    - "50mr" → $50 split between Mustafa and Rohit
    - "75mra" → $75 split equally among all three
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
st.markdown(f"""
    <div style='text-align: center; color: gray; font-size: 0.8em;'>
    💡 Type amount followed by '{initials}' to auto-select people (e.g., "100mr" for Mustafa and Rohit)
    </div>
""", unsafe_allow_html=True)
