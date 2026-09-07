import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("OPENAI_API_KEY를 찾을 수 없습니다.")
else:
    print("OPENAI_API_KEY 읽기 성공")

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input="안녕하세요. 연결 테스트입니다. 한 문장으로 답해주세요."
    )

    print("OpenAI 응답:")
    print(response.output_text)