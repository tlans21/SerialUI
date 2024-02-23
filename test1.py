from PyQt5.QtCore import QTimer

# Define the function to be called
def my_function():
    print("Timer timeout")

# Create a QTimer object
timer = QTimer()

# Call the function immediately
my_function()

# Connect the timeout signal of the timer to the function
timer.timeout.connect(my_function)

# Start the timer with a period of 1 second (1000 milliseconds)
timer.start(1000)
        