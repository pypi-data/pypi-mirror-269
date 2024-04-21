import sys
sys.path.insert(0,r'C:\Users\LAPTOP T&T\Documents\Python\40_NGAY_LUYEN_CODE\Day_30\factorial-NHK')

import streamlit as st
from factorial_nhk.factorial import fact

def main():
    st.title("Factorial Calculator")
    number = st.number_input("Enter a number:", min_value=0, max_value=900)
    if st.button("Calculate"):
        result = fact(number)
        st.write(f"The factorial of {number} is {result}")
        st.balloons()

if __name__ == "__main__":
    main()
