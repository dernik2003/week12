# Week 12 - Tools and Guardrails
Nikita Lemeshenko

## Project

This project has the Week 12 customer support chatbot and my Bayside Bike Repair mini-project. The support chatbot can check orders, returns, and stock. It also has a tool that sends address changes to staff for approval instead of changing an address right away.

For the mini-project, I kept the bike repair shop from Week 11 and added a repair price lookup and a booking approval queue. In a real Ollama test, Jamie answered that a flat tire repair costs $25. The booking tool refused a made-up customer name in a FakeModel test, and a real booking request waited until staff approved it. I added instructions to greet customers, collect the customer's name and repair type, and not say a booking is confirmed before approval.

## How to Run

Install the requirements and start Ollama with the `granite4.1:3b` model if you want to try the real chatbot.

```bash
python3 -m pip install -r requirements.txt
python3 main.py
python3 my_main.py
```

## Tests

```bash
ruff format .
ruff check .
pytest -v
```

## Development note

I used AI assistance to adapt parts of the bike repair classes. The Python files contain the generated class code with docstrings and explanatory comments, and I reviewed the behavior with tests and real Ollama conversations.
