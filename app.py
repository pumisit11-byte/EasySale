import streamlit as st

st.set_page_config(page_title="Salary Calculator", layout="centered")

st.title("🧮 Salary + OT + Expense Calculator")

# 1. Salary & OT Details
st.header("1. Salary & Overtime Details")
col1, col2 = st.columns(2)

with col1:
    salary = st.number_input("Base Salary", min_value=0.0, value=0.0, step=1000.0)
    hours_per_day = st.number_input("Work Hours/Day", min_value=0.0, value=8.0)
    work_days = st.number_input("Work Days (Opt)", min_value=0.0, value=0.0)
    travel_per_day = st.number_input("Travel Allowance/Day", min_value=0.0, value=0.0)

with col2:
    ot1 = st.number_input("OT x1.0 (Hrs)", min_value=0.0, value=0.0)
    ot15 = st.number_input("OT x1.5 (Hrs)", min_value=0.0, value=0.0)
    ot2 = st.number_input("OT x2.0 (Hrs)", min_value=0.0, value=0.0)
    ot3 = st.number_input("OT x3.0 (Hrs)", min_value=0.0, value=0.0)

# Calculation
if salary > 0 and hours_per_day > 0:
    hourly_rate = salary / 30 / hours_per_day
    money_ot1 = hourly_rate * ot1 * 1.0
    money_ot15 = hourly_rate * ot15 * 1.5
    money_ot2 = hourly_rate * ot2 * 2.0
    money_ot3 = hourly_rate * ot3 * 3.0
    total_ot = money_ot1 + money_ot15 + money_ot2 + money_ot3
    
    total_travel = work_days * travel_per_day
    social_security = min(salary * 0.05, 875.0)
    total_income = salary + total_ot + total_travel
    income_after_ss = total_income - social_security
else:
    total_ot = total_travel = social_security = total_income = income_after_ss = 0.0

# 2. Expense List
st.header("2. Expense List")
if "expenses" not in st.session_state:
    st.session_state.expenses = []

if st.button("+ Add Expense"):
    st.session_state.expenses.append({"name": "", "amount": 0.0})

total_expense = 0.0
to_delete = []

for idx, exp in enumerate(st.session_state.expenses):
    c1, c2, c3 = st.columns([2, 2, 1])
    exp["name"] = c1.text_input(f"Expense {idx+1}", value=exp["name"], key=f"name_{idx}")
    exp["amount"] = c2.number_input(f"Amount {idx+1}", min_value=0.0, value=exp["amount"], key=f"amt_{idx}")
    if c3.button("Delete", key=f"del_{idx}"):
        to_delete.append(idx)
    total_expense += exp["amount"]

for idx in reversed(to_delete):
    st.session_state.expenses.pop(idx)
    st.rerun()

# 3. Summary
st.header("3. Summary")
st.write(f"**Base Salary:** {salary:,.2f} THB")
st.write(f"**Total OT:** {total_ot:,.2f} THB")
st.write(f"**Travel Allowance:** {total_travel:,.2f} THB")
st.write(f"**Total Income:** {total_income:,.2f} THB")
st.write(f"**Social Security:** -{social_security:,.2f} THB")
st.write(f"**Income After SS:** {income_after_ss:,.2f} THB")
st.write(f"**Total Expenses:** -{total_expense:,.2f} THB")

remaining = income_after_ss - total_expense
st.markdown("---")
if remaining >= 0:
    st.success(f"### Balance: {remaining:,.2f} THB")
else:
    st.error(f"### Balance: {remaining:,.2f} THB")
