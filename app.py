import streamlit as st
import random

# Function to deal a card
def deal_card():
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    return random.choice(cards)

# Function to calculate the score
def calculate_score(cards):
    if sum(cards) == 21 and len(cards) == 2:
        return 0  # Blackjack
    if 11 in cards and sum(cards) > 21:
        cards.remove(11)
        cards.append(1)
    return sum(cards)

# Function to compare scores
def compare(u_score, c_score):
    if u_score == c_score:
        return "It's a Draw! 🙃"
    elif c_score == 0:
        return "You Lose! Opponent has a Blackjack 😱"
    elif u_score == 0:
        return "You Win with a Blackjack! 😎"
    elif u_score > 21:
        return "You went over. You lose! 😭"
    elif c_score > 21:
        return "Opponent went over. You win! 😁"
    elif u_score > c_score:
        return "You Win! 😃"
    else:
        return "You Lose! 😤"

# Streamlit Blackjack Game
st.title("Blackjack Game 🃏")
st.subheader("Try your luck against the computer!")

# Instructions Panel
with st.expander("Instructions"):
    st.write("""
    Welcome to the Blackjack game! Here’s how to play:
    
    - **Goal**: Get as close to 21 as possible without going over.
    - **Gameplay**:
        1. You and the computer are dealt 2 cards each.
        2. You can choose to **Hit Me!** (get another card) or **Pass** (end your turn).
        3. The computer will draw cards until its score is at least 17.
    - **Winning Rules**:
        - If your cards total 21 with just 2 cards (Blackjack), you win automatically.
        - If your score is closer to 21 than the computer’s without going over, you win.
        - If your score exceeds 21, you lose.
        - If the computer's score exceeds 21, you win.
    - Have fun and good luck! 😄
    """)

# Initialize game state in session_state
if "user_cards" not in st.session_state:
    st.session_state.user_cards = []
if "computer_cards" not in st.session_state:
    st.session_state.computer_cards = []
if "is_game_over" not in st.session_state:
    st.session_state.is_game_over = False
if "message" not in st.session_state:
    st.session_state.message = ""

# Start a new game
if st.button("Start New Game"):
    st.session_state.user_cards = [deal_card(), deal_card()]
    st.session_state.computer_cards = [deal_card(), deal_card()]
    st.session_state.is_game_over = False
    st.session_state.message = ""

# Display game state
if st.session_state.user_cards:
    user_score = calculate_score(st.session_state.user_cards)
    computer_score = calculate_score(st.session_state.computer_cards)

    st.write(f"Your Cards: {st.session_state.user_cards}, Current Score: {user_score}")
    st.write(f"Computer's First Card: {st.session_state.computer_cards[0]}")

    # Check for end of game conditions
    if user_score == 0 or computer_score == 0 or user_score > 21:
        st.session_state.is_game_over = True

    if not st.session_state.is_game_over:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Hit Me! (Get another card)"):
                st.session_state.user_cards.append(deal_card())
        with col2:
            if st.button("Pass"):
                st.session_state.is_game_over = True

# Handle game over
if st.session_state.is_game_over and not st.session_state.message:
    user_score = calculate_score(st.session_state.user_cards)
    computer_score = calculate_score(st.session_state.computer_cards)

    while computer_score != 0 and computer_score < 17:
        st.session_state.computer_cards.append(deal_card())
        computer_score = calculate_score(st.session_state.computer_cards)

    st.session_state.message = compare(user_score, computer_score)

# Display final results
if st.session_state.message:
    user_score = calculate_score(st.session_state.user_cards)
    computer_score = calculate_score(st.session_state.computer_cards)
    st.write(f"Your Final Hand: {st.session_state.user_cards}, Final Score: {user_score}")
    st.write(f"Computer's Final Hand: {st.session_state.computer_cards}, Final Score: {computer_score}")
    st.write(st.session_state.message)

    if st.button("Play Again"):
        st.session_state.user_cards = []
        st.session_state.computer_cards = []
        st.session_state.is_game_over = False
        st.session_state.message = ""
