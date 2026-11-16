# test_my_assistant.py
# Author: Nikita Lemeshenko

from fake_model import FakeModel
from my_assistant import RepairAssistant
from my_tool import RepairPriceTool
from repair_booking_queue import RepairBookingQueue
from repair_toolbox import RepairToolbox


class SilentModel:
    def decide(self, instructions, history, tools):
        return None


def make_assistant(model):
    prices = {"flat tire": 25, "brake adjustment": 35, "chain replacement": 40}
    price_tool = RepairPriceTool(prices)
    queue = RepairBookingQueue(price_tool)
    return RepairAssistant("Jamie", "Be friendly.", RepairToolbox(price_tool, queue), model)


def test_find_service():
    assert RepairPriceTool({"flat tire": 25}).find_service("Cost for flat tire?") == "flat tire"


def test_price_tool_is_available():
    model = FakeModel([
        {"tool": "check_repair_price", "arguments": {"service": "flat tire"}},
        {"text": "A flat tire repair costs $25."},
    ])
    assistant = make_assistant(model)
    assert "$25" in assistant.respond("How much is a flat tire?")
    assert "$25" in assistant.history[1]["content"]


def test_unknown_repair():
    tool = RepairPriceTool({"flat tire": 25})
    assert "can check" in tool.check_repair_price("tune-up")


def test_model_can_greet():
    assistant = make_assistant(FakeModel([{"text": "Hello! How can I help you?"}]))
    assert "Hello" in assistant.respond("hello")


def test_payment_handoff_happens_before_model():
    assistant = make_assistant(FakeModel([]))
    assert "employee" in assistant.respond("Can I pay by card?")


def test_missing_name_is_refused():
    assistant = make_assistant(FakeModel([
        {"tool": "request_repair_booking",
         "arguments": {"service": "flat tire", "customer_name": "Dana Cruz"}},
        {"text": "What is your full name?"},
    ]))
    assistant.respond("Please book a flat tire repair")
    assert "has not given that name" in assistant.history[1]["content"]
    assert assistant.tools.booking_queue.waiting() == []


def test_booking_waits_for_staff():
    assistant = make_assistant(FakeModel([
        {"tool": "request_repair_booking",
         "arguments": {"service": "flat tire", "customer_name": "Dana Cruz"}},
        {"text": "Your request is waiting for staff."},
    ]))
    assistant.respond("Please book a flat tire repair for Dana Cruz")
    assert len(assistant.tools.booking_queue.waiting()) == 1
    assert assistant.tools.price_tool.bookings == []


def test_booking_approved_only_once():
    tool = RepairPriceTool({"flat tire": 25})
    queue = RepairBookingQueue(tool)
    queue.request_repair_booking("flat tire", "Dana Cruz")
    assert queue.approve(1) == "Request 1 approved."
    assert queue.approve(1) == "Request 1 is already approved."
    assert len(tool.bookings) == 1


def test_rejected_booking_stays_rejected():
    tool = RepairPriceTool({"flat tire": 25})
    queue = RepairBookingQueue(tool)
    queue.request_repair_booking("flat tire", "Dana Cruz")
    assert queue.reject(1) == "Request 1 rejected."
    assert queue.approve(1) == "Request 1 is already rejected."
    assert tool.bookings == []


def test_unknown_tool_is_refused():
    assistant = make_assistant(FakeModel([
        {"tool": "charge_card", "arguments": {}},
        {"text": "I cannot do that."},
    ]))
    assistant.respond("Charge me now")
    assert "no tool named" in assistant.history[1]["content"]


def test_loop_limit():
    request = {"tool": "check_repair_price", "arguments": {"service": "flat tire"}}
    assistant = make_assistant(FakeModel([request, request, request]))
    assert "employee" in assistant.respond("How much for a flat tire?")


def test_model_unavailable():
    assistant = make_assistant(SilentModel())
    assert "can't answer" in assistant.respond("hello")
