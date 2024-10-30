import streamlit as st

# Set the title of the app
st.title("BMI Calculator")

# Create input fields for height and weight
height = st.number_input("Enter your height in meters:", min_value=0.0, step=0.01)
weight = st.number_input("Enter your weight in kilograms:", min_value=0.0, step=0.1)

# Create a button to calculate BMI
if st.button("Calculate BMI"):
    if height > 0:
        bmi = (weight / (height * 2)) * 100
        st.write(f"Your BMI is: {bmi:.3f}")
    else:
        st.error("Please enter a valid height.")
# aigooooooo
# Add a section for BMI interpretation
st.write("### BMI Categories")
st.write("Underweight: BMI < 18.5")
st.write("Normal weight: 18.5 ≤ BMI < 24.9")
st.write("Overweight: 25 ≤ BMI < 29.9")
st.write("Obesity: BMI ≥ 30")

