import pytest
from scanner import (
    check_input_validation,
    check_tool_poisoning,
    check_exfiltration,
    check_indirect_injection,
)
from types import SimpleNamespace

fake_block = SimpleNamespace(
    type="tool_use",
    name="read_path",
    input={"path": "../secret.txt"},
    id="toolu_fake_1",
)


class FakeLLM:
    def __init__(self, scripted_responses):
        self.responses = scripted_responses
        self.calls = 0
        self.messages = self

    def create(self, **kwargs):
        response = self.responses[self.calls]
        self.calls += 1
        return response


def fake_response(blocks, stop_reason="tool_use"):
    return SimpleNamespace(content=blocks, stop_reason=stop_reason)


@pytest.mark.asyncio
async def test_tool_poisoning_detects_unexpected_tool():
    fake = FakeLLM([fake_response([fake_block]) for _ in range(5)])
    result = await check_tool_poisoning(fake)
    assert result["verdict"] == "VULNERABLE"


@pytest.mark.asyncio
async def test_input_validation_detects_vulnerability():
    result = await check_input_validation()
    assert result["verdict"] == "VULNERABLE"
