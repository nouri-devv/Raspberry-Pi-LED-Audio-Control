import speech_recognition as sr
import gpiod


# Create the chip object once
chip = gpiod.Chip('gpiochip4')


# Define the GPIO pin for the LED
LED_PIN = 17
LED_line = chip.get_line(LED_PIN)
LED_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)


# Initialize the speech recognizer
recognizer = sr.Recognizer()


# Function to listen for voice commands
def listen_for_command():
   with sr.Microphone() as source:
       print("Listening for command...")
       audio = recognizer.listen(source)
       try:
           command = recognizer.recognize_google(audio)
           print("You said: " + command)
           return command.lower()
       except sr.UnknownValueError:
           print("Sorry, I did not get that.")
           return None
       except sr.RequestError:
           print("Could not request results; check your network connection.")
           return None


# Main loop to continuously listen for commands and control the LED
def main():
   while True:
       command = listen_for_command()
       if command:
           if "on" in command:
               LED_line.set_value(1)
               print("on")
           elif "off" in command:
               LED_line.set_value(0)
               print("LED is OFF")


if __name__ == "__main__":
   main()
