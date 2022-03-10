# Jetson-state
NVIDIA Jetson state and energy consumption.
You can change sleep(15) to other number to view the jetson state and energy consumption in certain time.

If you want to calculate the total energy consumption in certain time, you can add this code statistics.mean(power_consumption_list) / 1000 * total_time after analyser.stop_recording()
# Start
python3 power-agx.py
python3 power-tx2.py
python3 power-nano.py
