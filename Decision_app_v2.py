import streamlit as st
import random
import time

# -----------------------------
# APP SETUP
# -----------------------------
st.set_page_config(page_title="Everyday Decision Maker", page_icon="🎲")
st.title("🎲 Everyday Decision Maker")
st.write("Let logic, bias, or chaos decide 😄")

# -----------------------------
# SESSION STATE (HISTORY)
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# INPUTS
# -----------------------------
decision_title = st.text_input(
    "What decision are you making?",
    placeholder="What should I eat today?"
)

options_text = st.text_area(
    "Enter options (one per line)",
    placeholder="Pizza\nBiryani\nDosa\nSalad"
)

method = st.radio(
    "Decision method",
    ["🎲 Pure Random", "⚖️ Weighted Random", "🏆 Tournament"]
)

options = [o.strip() for o in options_text.split("\n") if o.strip()]

# -----------------------------
# BIAS INPUT PER OPTION
# -----------------------------
weights = []

if method == "⚖️ Weighted Random" and options:
    st.subheader("🎚️ Set bias for each option")

    for opt in options:
        w = st.slider(
            f"Bias for {opt}",
            min_value=0,
            max_value=100,
            value=50
        )
        weights.append(w)

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
        if sum(weights) == 0:
            st.warning("At least one option must have bias > 0.")
            st.stop()

        choice = random.choices(options, weights=weights)[0]
        reason = "Chosen using per-option bias."

    # -------- TOURNAMENT --------
    elif method == "🏆 Tournament":
        contenders = options.copy()
        round_num = 1

        st.subheader("🏆 Tournament Progress")

        while len(contenders) > 1:
            st.markdown(f"### Round {round_num}")
            next_round = []
            random.shuffle(contenders)

            for i in range(0, len(contenders), 2):
                if i + 1 < len(contenders):
                    a = contenders[i]
                    b = contenders[i + 1]
                    winner = random.choice([a, b])
                    st.write(f"{a} vs {b} → **{winner}**")
                    next_round.append(winner)
                else:
                    next_round.append(contenders[i])

            contenders = next_round
            round_num += 1
            time.sleep(0.4)

        choice = contenders[0]
        reason = "Won through tournament elimination."

    # -----------------------------
    # STORE HISTORY
    # -----------------------------
    st.session_state.history.append({
        "decision": decision_title,
        "method": method,
        "result": choice
    })

    # -----------------------------
    # SHOW RESULT
    # -----------------------------
    st.success(f"🎉 Decision: **{choice}**")
    st.caption(reason)

# -----------------------------
# HISTORY DISPLAY
# -----------------------------
if st.session_state.history:
    st.subheader("🕘 Decision History")

    for i, h in enumerate(reversed(st.session_state.history), 1):
        st.write(
            f"{i}. **{h['decision']}** → {h['result']} ({h['method']})"
        )

    if st.button("🧹 Clear history"):
        st.session_state.history = []
