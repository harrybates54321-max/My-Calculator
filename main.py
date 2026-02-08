import streamlit as st
import math
import requests

st.set_page_config(page_title="Python Multi-Tool", page_icon="🔢")

if 'history' not in st.session_state:
	st.session_state.history = []
	
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Choose a tool:", ["Calculator", "Currency Converter"])

if app_mode == "Calculator":
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
elif app_mode == "Currency Converter":
			st.title("💱 Currency Converter")
			st.write("Real-time exchange rates via Frankfurter API")
			
			@st.cache_data(ttl=3600)
			def get_currencies():
				try:
					return requests.get("https://api.frankfurter.app/currencies").json()
				except:
					return None
					
			data = get_currencies()
			if data:
				curr_list = list(data.keys())
				
				c1, c2 = st.columns(2)
				with c1:
					amt = st.number_input("Amount", min_value=0.0, value=1.0)
					from_c = st.selectbox("From", curr_list, index=curr_list.index("USD"))
				with c2:
					to_c = st.selectbox("To", curr_list, index=curr_list.index("EUR"))
					
				if st.button("Convert Currency", type="primary"):
					if from_c == to_c:
						st.warning("Please select different currencies.")
					else:
						url = f"https://api.frankfurter.app/latest?amount={amt}&from={from_c}&to={to_c}"
						response = requests.get(url)
						if response.status_code == 200:
							res = response.json()
							final_amt = res['rates'][to_c]
							st.metric(label=f"Result in {to_c}", value=f"{final_amt:.2f}{to_c}")
							st.session_state.history.append(f"{amt} {from_c} ➔ {final_amt:.2f} {to_c}")
						else:
							st.error("Failed to fetch rates. API might be busy.")
			else:
						st.error("Could not load currency data. Check your internet connection.")			
						
st.sidebar.markdown("---")
st.sidebar.header("Global History")
if not st.session_state.history:
			st.sidebar.write("No history yet.")
else:
			for entry in reversed(st.session_state.history):
				st.sidebar.text(entry)
			
			if st.sidebar.button("Clear History"):
				st.session_state.history = []
				st.rerun()