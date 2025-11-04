import streamlit as st
import joblib
import numpy as np
import random

# Load trained model

model = joblib.load("puzzle.joblib")


# ------------------------------
# Puzzle Bank
# ------------------------------
puzzles = {
    1: [
        {"question": "3 + 2 =", "answer": 5},
        {"question": "6 - 3 =", "answer": 3},
        {"question": "4 + 1 =", "answer": 5},
        {"question": "10 - 8 =", "answer": 2},
        {"question": "7 + 2 =", "answer": 9},
    ],
    2: [
        {"question": "5 * 2 =", "answer": 10},
        {"question": "12 / 3 =", "answer": 4},
        {"question": "15 - 6 =", "answer": 9},
        {"question": "8 * 2 =", "answer": 16},
        {"question": "20 / 5 =", "answer": 4},
    ],
    3: [
        {"question": "10 + 5 * 2 =", "answer": 20},
        {"question": "30 / 5 + 4 =", "answer": 10},
        {"question": "(6 * 3) - 5 =", "answer": 13},
        {"question": "2 * (8 + 3) =", "answer": 22},
        {"question": "(9 + 1) * 2 =", "answer": 20},
    ]
}

# ------------------------------
# Streamlit UI
# ------------------------------
st.title("🧠 Brain Games – Adaptive Puzzle Edition")
st.write("Solve the puzzle and let AI decide your next challenge!")

# Initialize session state
if "current_difficulty" not in st.session_state:
    st.session_state.current_difficulty = 1
if "total_score" not in st.session_state:
    st.session_state.total_score = 0
if "question" not in st.session_state:
    st.session_state.question = random.choice(puzzles[st.session_state.current_difficulty])

# Display question
st.subheader(f"Level {st.session_state.current_difficulty} Puzzle:")
st.write(st.session_state.question["question"])

# User answer input
user_answer = st.number_input("Enter your answer:", step=1, format="%d")

if st.button("Submit Answer"):
    correct_ans = st.session_state.question["answer"]

    # Auto accuracy and score
    if user_answer == correct_ans:
        st.success("✅ Correct!")
        accuracy = 1
        score = 10
    else:
        st.error(f"❌ Wrong! Correct answer was {correct_ans}.")
        accuracy = 0
        score = 0

    # Update total score
    st.session_state.total_score += score

    # Predict next difficulty
    input_data = np.array([[st.session_state.current_difficulty, accuracy, score]])
    next_diff = model.predict(input_data)[0]

    # Update current difficulty and show result
    st.write(f"🎯 Next recommended difficulty: **Level {next_diff}**")

    if next_diff > st.session_state.current_difficulty:
        st.write("🔥 You're doing great! Leveling up!")
    elif next_diff < st.session_state.current_difficulty:
        st.write("💪 Let's take it easy and practice simpler puzzles.")
    else:
        st.write("✨ Staying steady! Keep going strong!")

    # Move to next question
    st.session_state.current_difficulty = int(next_diff)
    st.session_state.question = random.choice(puzzles[int(next_diff)])

st.write("---")
st.write(f"**Total Score:** {st.session_state.total_score}")
