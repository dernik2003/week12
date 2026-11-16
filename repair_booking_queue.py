# repair_booking_queue.py
# Author: Nikita Lemeshenko


class RepairBookingQueue:
    """Hold booking requests until an employee approves them."""

    def __init__(self, price_tool):
        """Keep the repair tool and an empty list of requests."""
        self.price_tool = price_tool
        self.requests = []

    def request_repair_booking(self, service, customer_name):
        """Request a repair booking without confirming it.

        Args:
            service: The repair name, like flat tire.
            customer_name: The customer's full name.
        """
        # Keep service names consistent before checking the price list.
        service = service.strip().lower()
        if service not in self.price_tool.prices:
            return "That repair service was not found."
        # A waiting request is not the same as a confirmed booking.
        number = len(self.requests) + 1
        self.requests.append(
            {
                "number": number,
                "service": service,
                "customer_name": customer_name,
                "status": "waiting",
            }
        )
        return f"Request {number} was sent to staff. The repair is not booked yet."

    def waiting(self):
        """List only requests that still need a decision."""
        return [request for request in self.requests if request["status"] == "waiting"]

    def find(self, number):
        """Find a request by number."""
        for request in self.requests:
            if request["number"] == number:
                return request
        return None

    def approve(self, number):
        """Approve and book a request once."""
        request = self.find(number)
        if request is None:
            return f"There is no request {number}."
        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."
        request["status"] = "approved"
        # Only staff approval records the actual booking.
        self.price_tool.add_booking(request["service"], request["customer_name"])
        return f"Request {number} approved."

    def reject(self, number):
        """Reject a request without creating a booking."""
        request = self.find(number)
        if request is None:
            return f"There is no request {number}."
        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."
        request["status"] = "rejected"
        return f"Request {number} rejected."
