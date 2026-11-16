# Week 12 Answers
Nikita Lemeshenko

## Exercise 1

1. The customer typed three messages: "I want to change my shipping address", "It's order A102", and "9 Pine Street, Tampa".
2. Two tool requests were refused. The first one tried A100, which the customer never gave. The second one used an address that the customer did not provide.
3. Ollama receives 14 messages: one system message, seven user/assistant messages including the new "thanks", and six messages for the three tool calls.
4. The payment rule also catches the word "card" inside "gift cards". This is okay because sending a harmless question to a person is safer than accidentally letting payment information reach the model.

## Exercise 2

I added check_return in order_tool.py, added it to toolbox.py, and added one tool test and one FakeModel chatbot test. Only delivered orders can be returned within 30 days.

## Exercise 3

I temporarily added `return True` to `customer_said` in `toolbox.py`. Then I typed "I want to change my shipping address" without giving an order ID or a new address. The model created a change request using details I had never entered.

Here is the staff review output from my real Ollama test:

```text
Messages in this conversation: 3
Staff review
Request 1: A100 to 123 Main St, Anytown, AN 12345
Approve? yes or no: no
Request 1 rejected.
A100 14 Bay Road
A101 3 Gull Lane
A102 88 Pier Street
```

The made-up order ID was A100 and the made-up address was 123 Main St, Anytown, AN 12345. I selected "no" at staff review, so no shipping address changed. This experiment shows that a model can make up a convincing request if the toolbox skips its customer-message check. An employee might approve a wrong address if they are busy. The approval queue helps, but the check should stay enabled too. The extra question to the customer is worth it. The committed `toolbox.py` has the temporary `return True` removed.

## Exercise 4

I added `FallbackModel` so the chatbot first asks Ollama and then uses `KeywordModel` if Ollama returns `None`. I also connected the fallback model in `main.py`. The automated test uses `FallbackModel(SilentModel(), KeywordModel())` to simulate Ollama being unavailable. It checks that the customer can still look up order A100 without Ollama.
