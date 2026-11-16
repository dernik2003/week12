# my_main.py
# Author: Nikita Lemeshenko

from my_assistant import RepairAssistant
from my_tool import RepairPriceTool
from ollama_model import OllamaModel
from repair_booking_queue import RepairBookingQueue
from repair_toolbox import RepairToolbox

MODEL_NAME = "granite4.1:3b"

INSTRUCTIONS = """You are Jamie, a friendly customer service assistant for Bayside Bike Repair.
Answer in one short sentence.
The shop is open Monday through Saturday from 9 am to 6 pm.
Simple repairs usually take 2 business days.
If the customer only says hello, greet them and ask how you can help.
Use the price tool for repair cost questions and use the booking request tool only when the customer wants to book a repair.
For booking requests, collect the exact repair service and the customer's full name from their own messages before asking for the tool.
Never claim a booking is confirmed before staff approves it.
Only state facts that appear in these instructions or tool results.
If you do not know an answer, say so and suggest asking an employee."""

PRICES = {
    "flat tire": 25,
    "brake adjustment": 35,
    "chain replacement": 40,
}


def main():
    price_tool = RepairPriceTool(PRICES)
    booking_queue = RepairBookingQueue(price_tool)
    toolbox = RepairToolbox(price_tool, booking_queue)
    model = OllamaModel(MODEL_NAME)
    assistant = RepairAssistant("Jamie", INSTRUCTIONS, toolbox, model)

    print("Welcome to Bayside Bike Repair!")
    print("Type a message, or type quit to stop.")
    user_message = input("You: ")

    while user_message != "quit":
        print(f"{assistant.name}: {assistant.respond(user_message)}")
        user_message = input("You: ")

    print(f"Messages in this conversation: {len(assistant.history)}")
    print("Staff review")
    for request in booking_queue.waiting():
        number = request["number"]
        print(
            f"Request {number}: {request['customer_name']} - {request['service']}"
        )
        answer = input("Approve? yes or no: ")
        if answer.lower() == "yes":
            print(booking_queue.approve(number))
        else:
            print(booking_queue.reject(number))

    print("Confirmed bookings:", len(price_tool.bookings))


if __name__ == "__main__":
    main()
