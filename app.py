import streamlit as st

st.set_page_config(page_title="Tower of Hanoi", page_icon="🏰", layout="centered")

st.title("🏰 Tower of Hanoi Game")

if "disks" not in st.session_state:
    st.session_state.disks = 3
if "towers" not in st.session_state:
    st.session_state.towers = {'A': list(range(st.session_state.disks, 0, -1)), 'B': [], 'C': []}
if "moves" not in st.session_state:
    st.session_state.moves = 0
if "selected_from" not in st.session_state:
    st.session_state.selected_from = None

def reset_game(num_disks):
    st.session_state.disks = num_disks
    st.session_state.towers = {'A': list(range(num_disks, 0, -1)), 'B': [], 'C': []}
    st.session_state.moves = 0
    st.session_state.selected_from = None

with st.sidebar:
    st.header("⚙️ Game Settings")
    num_disks = st.slider("Select Disks", 3, 8, st.session_state.disks)
    if st.button("New Game"):
        reset_game(num_disks)
    st.markdown("---")
    st.write(f"**Moves:** {st.session_state.moves}")
    st.write(f"**Optimal Moves:** {(2**st.session_state.disks) - 1}")

def handle_click(tower_name):
    if st.session_state.selected_from is None:
        if len(st.session_state.towers[tower_name]) > 0:
            st.session_state.selected_from = tower_name
    else:
        src = st.session_state.selected_from
        dst = tower_name
        st.session_state.selected_from = None
        
        if src != dst:
            if not st.session_state.towers[dst] or st.session_state.towers[src][-1] < st.session_state.towers[dst][-1]:
                disk = st.session_state.towers[src].pop()
                st.session_state.towers[dst].append(disk)
                st.session_state.moves += 1
            else:
                st.error("Cannot place a larger disk on a smaller one!")

cols = st.columns(3)
tower_names = ['A', 'B', 'C']

for i, t_name in enumerate(tower_names):
    with cols[i]:
        btn_label = f"Select {t_name}" if st.session_state.selected_from != t_name else f"| {t_name} |"
        if st.button(btn_label, key=f"btn_{t_name}", use_container_width=True):
            handle_click(t_name)
        
        tower_content = st.session_state.towers[t_name]
        max_d = st.session_state.disks
        
        for _ in range(max_d - len(tower_content)):
            st.markdown("<div style='text-align:center; color:gray;'>|</div>", unsafe_allow_html=True)
            
        for disk in reversed(tower_content):
            width_pct = int((disk / max_d) * 100)
            st.markdown(
                f"<div style='background-color:#00adb5; width:{width_pct}%; margin:2px auto; "
                f"text-align:center; color:white; border-radius:5px; font-weight:bold;'>{disk}</div>",
                unsafe_allow_html=True
            )

if len(st.session_state.towers['C']) == st.session_state.disks or len(st.session_state.towers['B']) == st.session_state.disks:
    st.balloons()
    st.success(f"🎉 Congratulations! You won in {st.session_state.moves} moves!")
    
