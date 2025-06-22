# drinkfreezecalc.py

def estimate_cooling_time(volume_ml, start_temp_c, freezer_temp_c, drink_type, container_material):
    heat_capacities = {
        "water": 4.18,
        "soda": 3.9,
        "beer": 3.8,
        "wine": 3.6,
        "juice": 3.8
    }
    container_factors = {
        "plastic": 1.0,
        "aluminum": 0.7,
        "glass": 1.3
    }

    density = 1.0
    target_temp_c = 2
    heat_capacity = heat_capacities.get(drink_type.lower(), 4.0)
    container_factor = container_factors.get(container_material.lower(), 1.0)

    mass = volume_ml * density
    delta_temp = start_temp_c - target_temp_c
    energy_to_remove = mass * heat_capacity * delta_temp

    base_cooling_rate = 150  # J/min
    cooling_rate = base_cooling_rate / container_factor
    time_minutes = energy_to_remove / cooling_rate
    safe_time = time_minutes * 0.85

    return round(safe_time, 1)


# Try importing Streamlit
def is_streamlit():
    try:
        import streamlit.runtime.scriptrunner
        return True
    except ModuleNotFoundError:
        return False


# --- Streamlit UI ---
if is_streamlit():
    import streamlit as st

    st.title("🥤 Freezer Drink Timer")
    st.write("Estimate how long to chill a drink in the freezer without freezing or bursting.")

    volume = st.number_input("Drink volume (ml)", min_value=100, max_value=2000, value=355)
    start_temp = st.slider("Starting temperature (°C)", 0, 30, 22)
    freezer_temp = st.slider("Freezer temperature (°C)", -30, 0, -18)
    drink_type = st.selectbox("Drink type", ["water", "soda", "beer", "wine", "juice"])
    container_material = st.selectbox("Container material", ["plastic", "aluminum", "glass"])

    if st.button("Estimate Time"):
        time = estimate_cooling_time(volume, start_temp, freezer_temp, drink_type, container_material)
        st.success(f"⏱️ Suggested freezer time: **{time} minutes**")

# --- CLI fallback ---
else:
    def cli():
        print("=== Freezer Drink Timer (CLI Mode) ===")
        try:
            volume = float(input("Enter drink volume (ml): "))
            start_temp = float(input("Enter starting temperature (°C): "))
            freezer_temp = float(input("Enter freezer temperature (°C): "))
            drink = input("Enter drink type (water, soda, beer, wine, juice): ").strip().lower()
            container = input("Enter container type (plastic, aluminum, glass): ").strip().lower()

            time = estimate_cooling_time(volume, start_temp, freezer_temp, drink, container)
            print(f"\n⏱️ Suggested freezer time: {time} minutes")
        except Exception as e:
            print(f"Error: {e}")

    if __name__ == "__main__":
        cli()

