import streamlit as st
import random

# Function to deal a card
def deal_card():
    cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    return random.choice(cards)

# Function to calculate the score
def calculate_score(cards):
    if sum(cards) == 21 and len(cards) == 2:
        return 0
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
st.subheader("Can you beat the computer?")

if "user_cards" not in st.session_state:
    st.session_state.user_cards = []
if "computer_cards" not in st.session_state:
    st.session_state.computer_cards = []
if "is_game_over" not in st.session_state:
    st.session_state.is_game_over = False

# Start New Game
if st.button("Start New Game"):
    st.session_state.user_cards = [deal_card(), deal_card()]
    st.session_state.computer_cards = [deal_card(), deal_card()]
    st.session_state.is_game_over = False
    st.experimental_rerun()

if st.session_state.user_cards and not st.session_state.is_game_over:
    user_score = calculate_score(st.session_state.user_cards)
    computer_score = calculate_score(st.session_state.computer_cards)

    st.write(f"Your Cards: {st.session_state.user_cards}, Current Score: {user_score}")
    st.write(f"Computer's First Card: {st.session_state.computer_cards[0]}")

    if user_score == 0 or computer_score == 0 or user_score > 21:
        st.session_state.is_game_over = True

    if not st.session_state.is_game_over:
        if st.button("Hit Me! (Get another card)"):
            st.session_state.user_cards.append(deal_card())
            st.experimental_rerun()
        if st.button("Pass"):
            st.session_state.is_game_over = True
            st.experimental_rerun()

if st.session_state.is_game_over:
    user_score = calculate_score(st.session_state.user_cards)
    computer_score = calculate_score(st.session_state.computer_cards)
    while computer_score != 0 and computer_score < 17:
        st.session_state.computer_cards.append(deal_card())
        computer_score = calculate_score(st.session_state.computer_cards)

    st.write(f"Your Final Hand: {st.session_state.user_cards}, Final Score: {user_score}")
    st.write(f"Computer's Final Hand: {st.session_state.computer_cards}, Final Score: {computer_score}")
    st.write(compare(user_score, computer_score))

    if st.button("Play Again"):
        st.session_state.user_cards = []
        st.session_state.computer_cards = []
        st.session_state.is_game_over = False
        st.experimental_rerun()
