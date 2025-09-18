import streamlit as st
import random
from PIL import Image

# Load board image (make sure "board.png" is in the same folder as app.py)
board_img = Image.open("41a30364-49a2-44af-a12a-3796c5e44d6b.png")

class SnakeAndLadder:
    def __init__(self):
        self.snakes = {
            99: 78, 95: 75, 92: 88, 89: 68, 74: 53,
            64: 60, 62: 19, 49: 11, 46: 25, 16: 6
        }
        self.ladders = {
            2: 38, 7: 14, 8: 31, 15: 26, 21: 42,
            28: 84, 36: 44, 51: 67, 71: 91, 78: 98, 87: 94
        }

    def roll_dice(self):
        return random.randint(1, 6)


# --- Streamlit App ---
st.title("🎲 Snake and Ladder Game")
st.image(board_img, caption="Snake and Ladder Board", use_container_width=True)

# Initialize session state
if "players" not in st.session_state:
    st.session_state.players = {}
if "turn" not in st.session_state:
    st.session_state.turn = 0
if "game" not in st.session_state:
    st.session_state.game = SnakeAndLadder()
if "winner" not in st.session_state:
    st.session_state.winner = None
if "log" not in st.session_state:
    st.session_state.log = []


# Setup players
if not st.session_state.players:
    st.sidebar.header("Setup Game")
    num_players = st.sidebar.number_input("Enter number of players (1-4)", 1, 4, 2)
    temp_players = {}
    for i in range(1, num_players + 1):
        name = st.sidebar.text_input(f"Enter Player {i} name", f"Player {i}")
        if name:
            temp_players[name] = 0

    if st.sidebar.button("Start Game"):
        st.session_state.players = temp_players
        st.session_state.log.append("Starting positions:")
        for name in st.session_state.players:
            st.session_state.log.append(f"{name}: 0")
        st.rerun()

else:
    # Show current game log
    st.subheader("📜 Game Log")
    st.text("\n".join(st.session_state.log))

    players = list(st.session_state.players.keys())
    current_player = players[st.session_state.turn]

    if st.session_state.winner is None:
        st.subheader(f"🎯 {current_player}'s Turn")
        if st.button("Roll Dice 🎲"):
            dice = st.session_state.game.roll_dice()
            st.session_state.log.append(f"\n{current_player}'s turn. Press Enter to roll the dice...")
            st.session_state.log.append(f"{current_player} rolled a {dice}")

            new_pos = st.session_state.players[current_player] + dice

            if new_pos > 100:
                st.session_state.log.append(f"{current_player} cannot move, needs exact roll to win.")
            else:
                if new_pos in st.session_state.game.snakes:
                    st.session_state.log.append(
                        f"Oh no! {current_player} got bitten by a snake at {new_pos} → {st.session_state.game.snakes[new_pos]}"
                    )
                    new_pos = st.session_state.game.snakes[new_pos]
                elif new_pos in st.session_state.game.ladders:
                    st.session_state.log.append(
                        f"Yay! {current_player} climbed a ladder at {new_pos} → {st.session_state.game.ladders[new_pos]}"
                    )
                    new_pos = st.session_state.game.ladders[new_pos]

                st.session_state.players[current_player] = new_pos
                st.session_state.log.append(f"{current_player} moved to {new_pos}")

                if new_pos == 100:
                    st.session_state.winner = current_player
                    st.session_state.log.append(f"\n {current_player} wins the game!")

            # Show current positions
            st.session_state.log.append("\nCurrent Positions:")
            for name, pos in st.session_state.players.items():
                st.session_state.log.append(f"{name}: {pos}")

            # Next player's turn
            st.session_state.turn = (st.session_state.turn + 1) % len(players)
            st.rerun()

    else:
        st.success(f"🏆 {st.session_state.winner} wins the game!")
        st.balloons()

# Reset button
if st.button("🔄 Restart Game"):
    st.session_state.players = {}
    st.session_state.turn = 0
    st.session_state.winner = None
    st.session_state.game = SnakeAndLadder()
    st.session_state.log = []
    st.rerun()
