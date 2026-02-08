import streamlit as st

st.set_page_config(page_title="Python Calculator", page_icon="🔢")

if 'history' not in st.session_state:
	st.session_state.history = []
	
st.title("🔢 Python Calculator")
st.write("Enter your numbers below and choose and operation.")

col1, col2, col3 = st.columns([2, 1, 2])

with col1:
	num1 = st.number_input("First Number", value=0.0)
	
with col2:
	operator = st.selectbox("Op", ["+", "-", "*", "/"])
	
with col3:
	num2 = st.number_input("Second Number", value = 0.0)
	
if st.button("Calculate", type="primary"):
	result = None
	error = False
	
	if operator == '+':
		result = num1 + num2
	elif operator == '-':
		result = num1 - num2
	elif operator == '*':
		result = num1 * num2
	elif operator == '/':
		if num2 != 0:
			result = num1 / num2
		else:
			st.error("Error! Division by zero.")
			error = True
			
	if result is not None and not error:
		st.success(f"**Result:** {result}")
		
		calc_entry = f"{num1} {operator} {num2} = {result}"
		st.session_state.history.append(calc_entry)
		
st.sidebar.header("Calculation History")
if not st.session_state.history:
	st.sidebar.write("No calculations yet.")
else:
	for entry in reversed(st.session_state.history):
		st.sidebar.text(entry)
		
	if st.sidebar.button("Clear History"):
		st.session_state.history = []
		st.rerun()