from controller import Robot

robot = Robot()

# Get gyro and accelerometer devices
gyro = robot.getDevice("Gyro")
accelerometer = robot.getDevice("Accelerometer")

# Get motor devices for the legs
motor_names = ["LegUpperR", "LegLowerR", "LegUpperL", "LegLowerL"]
leg_motors = [robot.getDevice(name) for name in motor_names]

# Enable sensors
gyro.enable(32)
accelerometer.enable(32)

while robot.step(64) != -1:

    gyro_values = gyro.getValues()  # Gyro readings along X, Y, and Z axes
    accel_values = accelerometer.getValues()  # Accelerometer readings along X, Y, and Z axes
    
    # Calculate adjustments based on gyro and accelerometer values
    gyro_adjustment = abs(gyro_values[1] * 0.05)  # Adjust leg position based on gyro Y-axis value
    accel_adjustment = abs(accel_values[1] * 0.0025)  # Adjust leg position based on accelerometer Y-axis value

    # Set target positions for the leg motors to maintain balance
    target_positions = [
        0.5 + gyro_adjustment + accel_adjustment,  # LegUpperR
        -0.5 - gyro_adjustment - accel_adjustment,  # LegLowerR
        0.5 + gyro_adjustment + accel_adjustment,  # LegUpperL
        -0.5 - gyro_adjustment - accel_adjustment,  # LegLowerL
    ]

    # Set the target positions for the leg motors if the Y-axis value is 
    # greater than 0.1 or less than -0.1, which indicates a push
    if abs(gyro_values[1]) > 0.1:
        for motor, target_position in zip(leg_motors, target_positions):
            motor.setPosition(target_position)
        
    