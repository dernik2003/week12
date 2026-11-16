# my_tool.py
# Author: Nikita Lemeshenko


class RepairPriceTool:
    """Keep the shop's repair prices and record approved bookings."""

    def __init__(self, prices):
        """Save repair prices and start with no confirmed bookings."""
        self.prices = prices
        self.bookings = []

    def find_service(self, text):
        """Find a known repair service in the text."""
        # Compare the customer's words with known repair names.
        for service in self.prices:
            if service in text.lower():
                return service
        return None

    def price_for(self, service):
        """Return a price, or None when the service is not known."""
        return self.prices.get(service)

    def check_repair_price(self, service):
        """Look up the price of one bike repair.

        Args:
            service: The repair name, like flat tire.
        """
        # Use a saved price instead of letting the model guess.
        found = self.find_service(service)
        if found is None:
            return "I can check flat tire, brake adjustment, or chain replacement."
        return f"The price for {found} is ${self.price_for(found)}."

    def add_booking(self, service, customer_name):
        """Record a booking after a person has approved it."""
        # Only an approved request reaches this method.
        self.bookings.append({"service": service, "customer_name": customer_name})
