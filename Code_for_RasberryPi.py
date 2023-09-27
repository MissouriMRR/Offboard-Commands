import RPi.GPIO as GPIO
import time
from pymavlink import mavutil

# Define GPIO pins for the 6 MaxBotix sensors (adjust these to your actual GPIO pins)
sensor_pins = [17, 18, 22, 23, 24, 25]

# Define the orientations for each sensor in degrees (adjust as needed)
sensor_orientations = [0, 90, 180, 270, 45, 315]
#Right-Facing: 90 degrees - The sensor is facing to the right side.
#Rear-Facing: 180 degrees - The sensor is facing backward.
#Left-Facing: 270 degrees - The sensor is facing to the left side.
#Upward-Facing: 0 degrees or 360 degrees - The sensor is facing upward.

# Configure GPIO mode
GPIO.setmode(GPIO.BCM)

# Initialize MAVLink connection (adjust the device path as needed)
master = mavutil.mavlink_connection('/dev/ttyUSB0', baud=57600)

# Function to measure distance using the MaxBotix sensors
def measure_distance(sensor_pin, orientation):
    try:
        # Configure GPIO pin
        GPIO.setup(sensor_pin, GPIO.OUT)
        
        while True:
            # Trigger the sensor by sending a short HIGH pulse on the SIG pin
            GPIO.output(sensor_pin, GPIO.HIGH)
            time.sleep(0.00001)  # Wait for 10 microseconds
            GPIO.output(sensor_pin, GPIO.LOW)
            
            # Measure the time it takes for the echo signal to return
            GPIO.setup(sensor_pin, GPIO.IN)
            while GPIO.input(sensor_pin) == GPIO.LOW:
                pulse_start = time.time()
            while GPIO.input(sensor_pin) == GPIO.HIGH:
                pulse_end = time.time()
            
            # Calculate distance in meters
            pulse_duration = pulse_end - pulse_start
            distance_meters = (pulse_duration * 343) / 2  # Distance in meters (speed of sound is approximately 343 m/s)
            
            # Create a MAVLink DISTANCE_SENSOR message
            msg = master.messages['DISTANCE_SENSOR']
            msg.time_boot_ms = int(time.time() * 1000)
            msg.min_distance = 5  # Minimum measurable distance (adjust as needed)
            msg.max_distance = 64516  # Maximum measurable distance (adjust as needed)
            msg.current_distance = int(distance_meters * 100)  # Convert meters to centimeters for MAVLink
            msg.type = mavutil.mavlink.MAV_DISTANCE_SENSOR_ULTRASOUND
            msg.id = sensor_pins.index(sensor_pin)  # Sensor ID based on index
            msg.orientation = orientation  # Orientation of the sensor (adjust as needed)
            msg.covariance = 0  # Covariance (0 if unknown)

            # Send the MAVLink message
            master.mav.send(msg)
            
            # Implement collision avoidance logic based on distance
            if distance_meters < 0.3:  # Adjust the threshold as needed (e.g., 30 cm)
                print(f"Collision imminent on Sensor {msg.id}! Stop or change course.")
            else:
                print(f"Sensor {msg.id} Distance: {distance_meters:.2f} meters")
            
            time.sleep(0.1)  # Add a small delay between measurements 
    
    except KeyboardInterrupt:
        GPIO.cleanup()  # Clean up GPIO configuration on program exit

if __name__ == "__main__":
    for i, sensor_pin in enumerate(sensor_pins):
        orientation = sensor_orientations[i]
        measure_distance(sensor_pin, orientation)
