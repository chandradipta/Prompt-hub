import os
import random

class MockAdapter:
    def __init__(self, seed=None):
        self.seed = seed

    def generate(self, prompt, seed=None):
        # deterministic mock: return the expected line embedded if present in prompt
        if "<<EXPECTED:" in prompt:
            # prompt can embed expected value for mock tests
            start = prompt.find("<<EXPECTED:") + len("<<EXPECTED:")
            end = prompt.find(">>", start)
            if end != -1:
                return prompt[start:end].strip()
        # fallback deterministic short echo
        s = seed if seed is not None else self.seed
        if s is not None:
            random.seed(s)
        else:
            random.seed(0)
        # return a deterministic transformation
        return "MOCK_RESPONSE: " + str(abs(hash(prompt)) % 100000)

class OpenAIAdapter:
    def __init__(self, api_key=None):
        try:
            import openai
            self.openai = openai
        except Exception:
            self.openai = None
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.openai and self.api_key:
            self.openai.api_key = self.api_key

    def generate(self, prompt, seed=None):
        if not self.openai:
            raise RuntimeError("openai package not installed")
        resp = self.openai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=128, temperature=0)
        return resp.choices[0].text.strip()

def get_adapter(name="mock"):
    if name == "mock":
        return MockAdapter()
    if name == "openai":
        return OpenAIAdapter()
    raise ValueError(f"Unknown adapter: {name}")