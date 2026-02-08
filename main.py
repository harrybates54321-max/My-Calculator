import streamlit as st
import math 

st.set_page_config(page_title="Python Calculator", page_icon="🔢")

if 'history' not in st.session_state:
	st.session_state.history = []
	
st.title("🔢 Python Calculator")

st.sidebar.header("Settings")
scientific_mode = st.sidebar.toggle("Scientific Mode", value=False)

if scientific_mode:
	ops = ["+", "-", "*", "/", "x^y", "sqrt", "sin", "cos", "tan", "log"]
	st.write("---")
	st.info("Scientific Mode Active: Trig functions use Degrees.")
else:
	ops = ["+", "-", "*", "/"]

col1, col2, col3 = st.columns([2, 1, 2])

with col1:
	num1 = st.number_input("First Number", value=0.0, format="%.4f")
	
unary_ops = ["sqrt", "sin", "cos", "tan", "log"]
is_unary = scientific_mode and (st.session_state.get('operator_choice') in  unary_ops)
	
with col2:
	operator = st.selectbox("Op", ops, key='operator_choice')
	
with col3:
	num2 = st.number_input("Second Number", value = 0.0, format="%.4f",disabled=is_unary)
	
if st.button("Calculate", type="primary"):
	result = None
	error_msg = None
	
	try:
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
				error_msg = "Division by zero"
				
		elif operator == "x^y":
				result = math.pow(num1, num2)
		elif operator == "sqrt":
				if num1 >= 0:
					result = math.sqrt(num1)
				else:
					error_msg = "Cannot square root a negative number"
		elif operator == "sin":
			result = math.sin(math.radians(num1))
		elif operator == "cos":
			result = math.cos(math.radians(num1))
		elif operator == "tan":
			result = math.tan(math.radians(num1))
		elif operator == "log":
			if num1 > 0:
				result = math.log10(num1)
			else:
				error_msg = "Log of non-positive"
				
	except Exception as e:
		error_msg = str(e)
		
	if error_msg:
		st.error(f"Error: {error_msg}")
	elif result is not None:
		st.success(f"**Result:** {result}")
		
		if is_unary:
			entry = f"{operator}({num1}) = {result}"
		else:
			entry = f"{num1} {operator} {num2} = {result}"
			
		st.session_state.history.append(entry)
		
st.sidebar.markdown("--")
st.sidebar.header("Calculation History")
if not st.session_state.history:
	st.sidebar.write("No calculations yet.")
else:
	for entry in reversed(st.session_state.history):
		st.sidebar.text(entry)
		
	if st.sidebar.button("Clear History"):
		st.session_state.history = []
		st.rerun()