import streamlit as st
import time

st.set_page_config(page_title="Countdown Timer", page_icon="⏱️")
st.title("⏱️ Simple Countdown Timer")

# Session state initialization
for key, default in {
    "duration": 60,
    "running": False,
    "start_time": None,
    "remaining": None,
    "paused": False,
    "pause_start": None,
    "total_pause_time": 0,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Disable input while running
disabled_inputs = st.session_state.running
minutes = st.number_input("Minutes", 0, 60, 1, disabled=disabled_inputs)
seconds = st.number_input("Seconds", 0, 59, 0, disabled=disabled_inputs)
total_seconds = minutes * 60 + seconds

# Warning for zero time
if total_seconds == 0 and not st.session_state.running:
    st.warning("Please set a time greater than 0 seconds.")

# TIMER LOGIC
if st.session_state.running:
    if st.session_state.paused:
        elapsed = st.session_state.duration - st.session_state.remaining
    else:
        elapsed = (
            time.time()
            - st.session_state.start_time
            - st.session_state.total_pause_time
        )
        st.session_state.remaining = max(0, st.session_state.duration - elapsed)

    mins, secs = divmod(int(st.session_state.remaining), 60)
    st.header(f"⏳ Time Remaining: {mins:02d}:{secs:02d}")
    st.progress(
        min(1.0, max(0.0, 1 - st.session_state.remaining / st.session_state.duration))
    )

    if st.session_state.remaining <= 0 and not st.session_state.paused:
        st.success("⏰ Time's up!")
        st.balloons()
        st.session_state.running = False
        st.session_state.paused = False
    elif not st.session_state.paused:
        time.sleep(0.1)
        st.rerun()
else:
    st.header(f"⏲️ Set Timer: {minutes:02d}:{seconds:02d}")

# CONTROLS LAYOUT
col1, col2, col3, col4 = st.columns(4)

# ▶️ START button
with col1:
    if (
        not st.session_state.running
        and not st.session_state.paused
        and total_seconds > 0
    ):
        if st.button("▶️ Start", use_container_width=True):
            st.session_state.duration = total_seconds
            st.session_state.running = True
            st.session_state.start_time = time.time()
            st.session_state.paused = False
            st.session_state.total_pause_time = 0
            st.session_state.remaining = total_seconds
            st.rerun()

# ⏸️ PAUSE / 🔄 RESUME buttons
with col2:
    if st.session_state.running and not st.session_state.paused:
        if st.button("⏸️ Pause", use_container_width=True):
            st.session_state.paused = True
            st.session_state.pause_start = time.time()
            st.rerun()
    elif st.session_state.paused:
        if st.button("🔄 Resume", use_container_width=True):
            pause_duration = time.time() - st.session_state.pause_start
            st.session_state.total_pause_time += pause_duration
            st.session_state.paused = False
            st.rerun()

# 🔁 RESET button
with col3:
    if st.session_state.running or st.session_state.paused:
        if st.button("🔁 Reset", use_container_width=True):
            for key in [
                "running",
                "paused",
                "start_time",
                "remaining",
                "total_pause_time",
            ]:
                st.session_state[key] = (
                    False if isinstance(st.session_state[key], bool) else None
                )
            st.rerun()

# 🛑 STOP button
with col4:
    if st.session_state.running or st.session_state.paused:
        if st.button("🛑 Stop", use_container_width=True):
            for key in [
                "running",
                "paused",
                "start_time",
                "remaining",
                "total_pause_time",
            ]:
                st.session_state[key] = (
                    False if isinstance(st.session_state[key], bool) else None
                )
            st.success("⏹️ Timer stopped.")
            st.rerun()
