# repair_toolbox.py
# Author: Nikita Lemeshenko


class RepairToolbox:
    """Check every tool request before the model can use it."""

    def __init__(self, price_tool, booking_queue):
        """Store the price lookup and approval queue."""
        self.price_tool = price_tool
        self.booking_queue = booking_queue

    def tool_list(self):
        """List the two methods that the model may request."""
        return [
            self.price_tool.check_repair_price,
            self.booking_queue.request_repair_booking,
        ]

    def clean(self, arguments, key):
        """Get one requested value as trimmed text."""
        return str(arguments.get(key, "")).strip()

    def customer_said(self, history, text):
        """Check only messages originally typed by the customer."""
        # Only the customer's original messages count as permission.
        for message in history:
            if message["role"] == "user" and text.lower() in message["content"].lower():
                return True
        return False

    def run(self, name, arguments, history):
        """Refuse unknown tools, empty details, and invented booking details."""
        # Checking prices does not create a booking.
        if name == "check_repair_price":
            service = self.clean(arguments, "service")
            if service == "":
                return "Please ask which repair the customer wants."
            return self.price_tool.check_repair_price(service)
        # A booking needs both the requested service and customer's name.
        if name == "request_repair_booking":
            service = self.clean(arguments, "service")
            customer_name = self.clean(arguments, "customer_name")
            if service == "" or customer_name == "":
                return "Ask for both the repair service and customer's full name."
            if not self.customer_said(history, service):
                return "The customer has not given that repair service. Ask them."
            # Refuse a name that came from the model instead of the customer.
            if not self.customer_said(history, customer_name):
                return "The customer has not given that name. Ask them."
            return self.booking_queue.request_repair_booking(service, customer_name)
        return f"There is no tool named {name}."
