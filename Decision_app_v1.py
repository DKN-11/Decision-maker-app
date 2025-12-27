import streamlit as st
import random
import matplotlib.pyplot as plt

# -----------------------------
# APP TITLE
# -----------------------------
st.set_page_config(page_title="Everyday Decision Maker", page_icon="🎲")
st.title("🎲 Everyday Decision Maker")
st.write("Let fate (or bias) decide your everyday choices 😄")

# -----------------------------
# USER INPUTS
# -----------------------------
decision_title = st.text_input(
    "What decision are you making?",
    placeholder="What should I eat today?"
)

options_text = st.text_area(
    "Enter your options (one per line)",
    placeholder="Pizza\nBiryani\nDosa\nSalad"
)

method = st.radio(
    "Choose a decision method:",
    ["🎲 Pure Random", "⚖️ Weighted Random", "🎡 Spin the Wheel"]
)

bias_strength = st.slider(
    "Bias strength (only for weighted methods)",
    min_value=0,
    max_value=100,
    value=50
)

# -----------------------------
# PROCESS INPUT OPTIONS
# -----------------------------
options = [o.strip() for o in options_text.split("\n") if o.strip()]

# -----------------------------
# DECISION BUTTON
# -----------------------------
if st.button("🚀 Decide for me"):

    if len(options) < 2:
        st.warning("Please enter at least two options.")
        st.stop()

    # -------- PURE RANDOM --------
    if method == "🎲 Pure Random":
        choice = random.choice(options)
        reason = "Chosen completely at random."

    # -------- WEIGHTED RANDOM --------
    elif method == "⚖️ Weighted Random":
        weights = []

        for i in range(len(options)):
            if i == 0:
                weights.append(bias_strength)
            else:
                weights.append(100 - bias_strength)

        choice = random.choices(options, weights=weights)[0]


        reason = f"Weighted choice with bias strength = {bias_strength}%."

    # -------- SPIN THE WHEEL --------
    elif method == "🎡 Spin the Wheel":
        choice = random.choice(options)
        reason = "The wheel has spoken 🎡"

        # Create wheel visualization
        fig, ax = plt.subplots()
        ax.pie(
            [1] * len(options),
            labels=options,
            autopct=None,
            startangle=90
        )
        ax.axis("equal")
        st.pyplot(fig)

    # -----------------------------
    # DISPLAY RESULT
    # -----------------------------
    st.success(f"🎉 Decision: **{choice}**")
    st.caption(reason)
