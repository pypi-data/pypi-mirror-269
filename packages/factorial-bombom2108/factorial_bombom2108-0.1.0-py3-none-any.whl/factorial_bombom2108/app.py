import streamlit as st
from factorial_bombom2108.factorial import fact

def main():
    st.title("Factorial Calculator")
    number = st.number_input("Enter a number",
                             min_value=0,
                             max_value=900)
    
    if st.button("Caculate"):
        result = fact(number)
        st.write(F"The factorial of {number} is {result}")
        st.balloons()


if __name__ == '__main__':
    main()