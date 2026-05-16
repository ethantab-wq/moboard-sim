import streamlit as st
import math
import random


# ==============================
# VECTOR FUNCTIONS
# ==============================

def polar_to_xy(course, speed):
    rad = math.radians(course)
    x = speed * math.sin(rad)
    y = speed * math.cos(rad)
    return x, y


def xy_to_polar(x, y):
    speed = math.sqrt(x**2 + y**2)
    course = math.degrees(math.atan2(x, y))
    if course < 0:
        course += 360
    return course, speed


# ==============================
# PAGE SETUP
# ==============================

st.set_page_config(page_title="MOBOARD SIM", layout="centered")

st.title("🚢 Naval MOBOARD Tactical Simulator")
st.caption("Relative Motion • CPA • Radar Intercept Game")


menu = st.sidebar.selectbox(
    "Select Function",
    [
        "Home",
        "CPA Calculator",
        "Relative Motion",
        "Bearing Conversion",
        "Target Angle",
        "Radar Game"
    ]
)


# ==============================
# HOME
# ==============================

if menu == "Home":
    st.subheader("Welcome, Officer")
    st.write("Select a function from the sidebar to begin operations.")

    st.markdown("### 📡 Capabilities")
    st.write("- CPA / TCPA calculation")
    st.write("- Relative motion vectors")
    st.write("- Bearing conversions")
    st.write("- Radar intercept training game")


# ==============================
# CPA CALCULATOR
# ==============================

elif menu == "CPA Calculator":

    st.subheader("CPA / TCPA Calculator")

    own_course = st.number_input("Own Ship Course", 0, 359)
    own_speed = st.number_input("Own Ship Speed", 0.0)

    target_course = st.number_input("Target Course", 0, 359)
    target_speed = st.number_input("Target Speed", 0.0)

    bearing = st.number_input("Initial Bearing to Target", 0, 359)
    distance = st.number_input("Initial Distance (nm)", 0.0)

    if st.button("Calculate CPA"):

        ex, ey = polar_to_xy(own_course, own_speed)
        mx, my = polar_to_xy(target_course, target_speed)

        rx = mx - ex
        ry = my - ey

        bx = distance * math.sin(math.radians(bearing))
        by = distance * math.cos(math.radians(bearing))

        rm_sq = rx**2 + ry**2

        if rm_sq == 0:
            st.error("No relative motion detected.")
        else:
            tcpa = -(bx * rx + by * ry) / rm_sq

            cpa_x = bx + rx * tcpa
            cpa_y = by + ry * tcpa

            cpa_distance = math.sqrt(cpa_x**2 + cpa_y**2)

            rm_course, rm_speed = xy_to_polar(rx, ry)

            st.success("Results")

            st.write(f"RM Course: {rm_course:.2f}°T")
            st.write(f"RM Speed: {rm_speed:.2f} kts")
            st.write(f"TCPA: {tcpa:.2f} hrs")
            st.write(f"CPA Distance: {cpa_distance:.2f} nm")


# ==============================
# RELATIVE MOTION
# ==============================

elif menu == "Relative Motion":

    st.subheader("Relative Motion Calculator")

    own_course = st.number_input("Own Ship Course", 0, 359)
    own_speed = st.number_input("Own Ship Speed", 0.0)

    target_course = st.number_input("Target Course", 0, 359)
    target_speed = st.number_input("Target Speed", 0.0)

    if st.button("Compute RM"):

        ex, ey = polar_to_xy(own_course, own_speed)
        mx, my = polar_to_xy(target_course, target_speed)

        rx = mx - ex
        ry = my - ey

        course, speed = xy_to_polar(rx, ry)

        st.write("ER Vector:", ex, ey)
        st.write("EM Vector:", mx, my)
        st.write("RM Vector:", rx, ry)
        st.success(f"RM Course: {course:.2f}°T | Speed: {speed:.2f} kts")


# ==============================
# BEARING CONVERSION
# ==============================

elif menu == "Bearing Conversion":

    st.subheader("Bearing Conversion")

    own_course = st.number_input("Own Ship Course", 0, 359)
    rel_bearing = st.number_input("Relative Bearing", 0, 359)

    if st.button("Convert"):

        true_bearing = (own_course + rel_bearing) % 360
        st.success(f"True Bearing: {true_bearing:.2f}°T")


# ==============================
# TARGET ANGLE
# ==============================

elif menu == "Target Angle":

    st.subheader("Target Angle")

    target_course = st.number_input("Target Course", 0, 359)
    bearing = st.number_input("Line of Sight Bearing", 0, 359)

    if st.button("Calculate"):

        angle = abs(target_course - bearing)
        if angle > 180:
            angle = 360 - angle

        st.success(f"Target Angle: {angle:.2f}°")


# ==============================
# RADAR GAME
# ==============================

elif menu == "Radar Game":

    st.subheader("Radar Intercept Game")

    if "score" not in st.session_state:
        st.session_state.score = 0

    own_course = random.randint(0, 359)
    own_speed = random.randint(10, 25)

    enemy_course = random.randint(0, 359)
    enemy_speed = random.randint(5, 30)

    bearing = random.randint(0, 359)
    distance = random.randint(5, 20)

    st.write("### Your Ship")
    st.write(f"Course: {own_course}°T")
    st.write(f"Speed: {own_speed} kts")

    st.write("### Radar Contact")
    st.write(f"Bearing: {bearing}°T")
    st.write(f"Distance: {distance} nm")

    guess_course = st.number_input("Guess Enemy Course", 0, 359)
    guess_speed = st.number_input("Guess Enemy Speed", 0.0)

    if st.button("Engage"):

        course_error = abs(guess_course - enemy_course)
        speed_error = abs(guess_speed - enemy_speed)

        round_score = max(0, 100 - course_error - speed_error * 3)

        st.session_state.score += int(round_score)

        st.success("Results")
        st.write(f"Enemy Course: {enemy_course}°T")
        st.write(f"Enemy Speed: {enemy_speed} kts")
        st.write(f"Round Score: {round_score}")
        st.write(f"Total Score: {st.session_state.score}")
        