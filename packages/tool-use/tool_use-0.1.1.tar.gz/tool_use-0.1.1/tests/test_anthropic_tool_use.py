import os
import unittest
from ast import literal_eval
from typing import Tuple

import pytest
import pytest_asyncio

from tool_use.tools.anthropic_tool_use import AnthropicConnection, anthropic_tool_use

# Run the unit tests
if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    unittest.main()


@pytest_asyncio.fixture
def load_env():
    from dotenv import load_dotenv

    load_dotenv()


@pytest_asyncio.fixture
def my_connection(load_env) -> AnthropicConnection:
    return AnthropicConnection(
        secrets=dict(
            api_key=os.environ.get("ANTHROPIC_API_KEY"),
            api_type="anthropic",
            api_base="https://api.anthropic.com",
            client_key=None,
        ),
    )


@pytest_asyncio.fixture
def my_custom_connection(load_env) -> AnthropicConnection:
    return AnthropicConnection(
        secrets=dict(
            api_key=os.environ.get("ANTHROPIC_API_KEY"),
            api_type="anthropic",
            api_base=os.environ.get("ANTHROPIC_API_BASE"),
            client_key=None,
        ),
    )


def load_tool_prompts() -> Tuple[str, dict]:
    prompt = ""
    with open(
        os.path.join(os.path.dirname(__file__), "claude_tool_prompt.jinja2")
    ) as f:
        prompt = f.read()
    sample_tool = {}
    with open(os.path.join(os.path.dirname(__file__), "claude_tool.jinja2")) as f:
        sample_tool = f.read()
        sample_tool = literal_eval(sample_tool)
    return prompt, sample_tool


def load_prompt() -> str:
    prompt = ""
    with open(os.path.join(os.path.dirname(__file__), "claude_prompt.jinja2")) as f:
        prompt = f.read()
    return prompt


args = {
    "locale": "ko-KR",
    "current_datetime": "2024-04-17 16:17:11",
    "chat_history": [
        {"role": "user", "content": "뤼튼 이세영의 본가는?"},
        {
            "role": "assistant",
            "content": "알겠습니다. 뤼튼 이세영 대표님의 본가에 대해 자세히 살펴보겠습니다.\n\n🔍 정보 조사 결과:\n- 이세영 대표님은 서울에 위치한 Wrtn Technologies, Inc.의 창립자이자 CEO입니다. [[1]](https://kr.linkedin.com/in/seyoung-lee-noah/ko)\n- 그는 연세대학교를 졸업했으며, 현재 3,000명의 팔로워를 보유하고 있습니다. [[1]](https://kr.linkedin.com/in/seyoung-lee-noah/ko)\n- 이세영 대표님은 한국형 생성 AI '뤼튼'의 대표이기도 합니다. 뤼튼은 최근 100만 명의 가입자를 돌파했습니다. [[3]](https://www.idaegu.com/newsView/idg202309140064)\n- 이세영 대표님은 포브스코리아가 선정한 '30세 미만 30인' 중 한 명으로 선정되었습니다. [[4]](https://www.aitimes.com/news/articleView.html?idxno=157738)\n\n🤔 추가 정보:\n- 이세영 대표님의 본가 정보는 공개되어 있지 않습니다. 그러나 그가 서울에 위치한 Wrtn Technologies, Inc.의 창립자라는 점을 고려할 때, 본가 또한 서울 근처에 있을 것으로 추정됩니다.\n- 이세영 대표님은 연세대학교 출신으로, 본가가 서울 근처일 가능성이 높습니다. 하지만 정확한 위치는 공개되지 않았습니다.\n\n🙂 결론:\n이세영 대표님의 본가 정확한 위치는 공개되지 않았지만, 그가 서울에 위치한 Wrtn Technologies, Inc.의 창립자이자 연세대학교 출신이라는 점을 고려할 때 서울 근처에 있을 것으로 추정됩니다. 더 자세한 정보는 추후 공개될 수 있습니다. 궁금한 점이 더 있다면 언제든 물어보세요!",
        },
    ],
    "tool_calls": [
        {
            "id": "call_kRMGVaaeM5CJ2OuPbINXyUb7",
            "type": "function",
            "function": {
                "name": "browsing_with_google",
                "arguments": {
                    "search_query": "뤼튼 이세영 본가 위치",
                    "reason_for_selection": "To find the location of Luton Lee Se-young's hometown.",
                },
            },
        }
    ],
    "question": "뤼튼 이세영의 본가는?",
    "tool_messages": [
        {
            "id": "call_kRMGVaaeM5CJ2OuPbINXyUb7",
            "function": {
                "name": "browsing_with_google",
                "arguments": {
                    "search_query": "뤼튼 이세영 본가 위치",
                    "reason_for_selection": "To find the location of Luton Lee Se-young's hometown.",
                },
            },
            "content": "[{'inner_text': '{\n  \"summary\": \"Yiseoung Lee is the founder and CEO of Wrtn Technologies, Inc., located in Seoul, South Korea. She is also an alumna of Yonsei University with 3,000 followers.\"\n}', 'res_idx': 1, 'link': 'https://kr.linkedin.com/in/seyoung-lee-noah/ko'}, {'inner_text': '{\n  \"title\": \"이세영 뤼튼 대표 등 AI 전문가 5인, 포브스코리아 %%'30세 미만 30인%%' 선정\",\n  \"content\": \"포브스코리아가 %%'30세 미만 30인%%'에 인공지능(AI) 전문가 5명을 포함시켰다. 김정현, 김형준, 박찬준, 심규현, 이세영 뤼튼테크놀로지스 대표가 주요 주인공으로 선정되었다.\"\n}', 'res_idx': 2, 'link': 'https://www.aitimes.com/news/articleView.html?idxno=157738'}, {'inner_text': '{\n  \"summary\": \"The video is 21 minutes and 38 seconds long.\"\n}', 'res_idx': 3, 'link': 'https://www.youtube.com/watch?v=SYG-zG3o4fQ'}, {'inner_text': '{\n  \"store_guide\": \"Log in to the Chat Studio Store to access official character dialogues and set up your own character.\",\n  \"ai_search\": \"Lutens AI may generate inaccurate information due to referencing various data models, so it%%'s important to verify the accuracy of important information.\",\n  \"character_creation\": \"Create your own character with options like Hyesung Jeon, Taehoon Jang, Maeve, Cha Youngbin, Suni Chan, Minji Lee, and more.\",\n  \"prompt_options\": \"Explore prompt options like PowerPoint creation, initial email writing for marketing, game recommendations, Python interpreter, advertising copywriting, and persona generation.\"\n}', 'res_idx': 4, 'link': 'https://wrtn.ai/'}]",
        }
    ],
}


@pytest.mark.asyncio(scope="class")
class TestTool:
    async def test_anthropic_tool_use(self, my_connection):
        prompt, sample_tool = load_tool_prompts()
        result = await anthropic_tool_use(
            connection=my_connection,
            prompt=prompt,
            model="claude-3-haiku-20240307",
            max_tokens=500,
            tools=[sample_tool],
        )
        assert result is not None
        print(result)

    async def test_anthropic(self, my_connection):
        prompt = load_prompt()
        result = await anthropic_tool_use(
            connection=my_connection,
            prompt=prompt,
            model="claude-3-haiku-20240307",
            max_tokens=500,
            **args,
        )
        assert result is not None
        print(result)

    async def test_anthropic_stream(self, my_connection):
        prompt = load_prompt()
        result = await anthropic_tool_use(
            connection=my_connection,
            prompt=prompt,
            model="claude-3-haiku-20240307",
            max_tokens=500,
            stream=True,
            is_raw_output=True,
            **args,
        )
        chunk_count = 0
        total_result = ""
        async for chunk in result:
            chunk_count += 1
            if hasattr(chunk, "delta") and hasattr(chunk.delta, "text"):
                total_result += chunk.delta.text
        # raise Exception("This test is not working as expected")
        print(chunk_count)
        print(total_result)
        assert len(total_result) > 0

    async def test_anthropic_tool_use_2(self, my_custom_connection):
        prompt, sample_tool = load_tool_prompts()
        result = await anthropic_tool_use(
            connection=my_custom_connection,
            prompt=prompt,
            model="anthropic.claude-3-haiku-20240307-v1:0",
            max_tokens=500,
            tools=[sample_tool],
            stream=False,
        )
        assert result is not None
        print(result)

    async def test_anthropic_2(self, my_custom_connection):
        prompt = load_prompt()
        result = await anthropic_tool_use(
            connection=my_custom_connection,
            prompt=prompt,
            model="anthropic.claude-3-haiku-20240307-v1:0",
            max_tokens=500,
            stream=False,
            **args,
        )
        assert result is not None
        print(result)

    async def test_anthropic_stream_2(self, my_custom_connection):
        prompt = load_prompt()
        result = await anthropic_tool_use(
            connection=my_custom_connection,
            prompt=prompt,
            model="anthropic.claude-3-haiku-20240307-v1:0",
            max_tokens=500,
            stream=True,
            is_raw_output=True,
            extra_headers={"x-feature-id": "1"},
            **args,
        )
        chunk_count = 0
        total_result = ""
        total_result = ""
        async for chunk in result:
            chunk_count += 1
            if hasattr(chunk, "delta") and hasattr(chunk.delta, "text"):
                total_result += chunk.delta.text
        # raise Exception("This test is not working as expected")
        print(chunk_count)
        print(total_result)
        assert len(total_result) > 0, chunk_count


# Run the unit tests
if __name__ == "__main__":
    unittest.main()
