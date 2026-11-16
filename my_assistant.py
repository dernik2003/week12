# my_assistant.py
# Author: Nikita Lemeshenko

HANDOFF_WORDS = ["cancel", "reschedule", "payment", "card"]
MAX_TOOL_ROUNDS = 3


class RepairAssistant:
    """Let a model choose tools but check requests and protect sensitive actions."""

    def __init__(self, name, instructions, tools, model):
        """Set the assistant's name, instructions, toolbox, model, and history."""
        self.name = name
        self.instructions = instructions
        self.tools = tools
        self.model = model
        self.history = []

    def respond(self, user_message):
        """Save the question and the answer to the conversation history."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Send risky questions to staff before asking the model."""
        # Handle risky changes through staff rather than an AI reply.
        if self.needs_human(user_message.lower()):
            return "I can't change or cancel that here. Please speak to an employee."
        return self.model_reply()

    def needs_human(self, text):
        """Check for actions that must be handled directly by an employee."""
        for word in HANDOFF_WORDS:
            if word in text:
                return True
        return False

    def model_reply(self):
        """Run at most three checked tool calls before returning a reply."""
        rounds = 0
        # Three calls maximum prevents repeated or endless tool use.
        while rounds < MAX_TOOL_ROUNDS:
            decision = self.model.decide(
                self.instructions, self.history, self.tools.tool_list()
            )
            if decision is None:
                return "Sorry, I can't answer that right now. Please ask an employee."
            if "text" in decision:
                return decision["text"]
            name = decision["tool"]
            arguments = decision["arguments"]
            # All requested tools pass through the toolbox validation.
            result = self.tools.run(name, arguments, self.history)
            self.history.append(
                {
                    "role": "tool",
                    "tool_name": name,
                    "arguments": arguments,
                    "content": result,
                }
            )
            rounds += 1
        return "Sorry, I couldn't finish that. Please speak to an employee."
