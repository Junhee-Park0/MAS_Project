import os
from src.Multi_Agent.functions import get_news_context
from src.Multi_Agent.graph import agent_debate_graph

# 환경 변수 설정 (필요시 API 키 입력)
# os.environ["OPENAI_API_KEY"] = "sk-..."

def main():
    # 1. 설정
    ticker = "GOOGL"
    keywords = ["AI", "Gemini", "Cloud"]
    
    print(f"--- [{ticker}] 데이터 수집 중 ---")
    
    # 2. Context 데이터 가져오기
    news_context, sec_context = get_news_context(ticker, keywords)
    
    # 리스트 형태의 컨텍스트를 하나의 문자열로 합침 (nodes.py에서 문자열을 기대함)
    combined_context = "\n\n".join([str(item) for item in news_context])
    combined_context += "\n\n### SEC Data ###\n" + "\n".join([str(item) for item in sec_context])

    print(f"--- 데이터 수집 완료 (뉴스 {len(news_context)}건, SEC {len(sec_context)}건) ---")

    # 3. 초기 상태 설정 (State 주입)
    initial_state = {
        "ticker": ticker,
        "keywords": keywords,
        "context": combined_context,  # 합친 컨텍스트 주입
        "debate_history": [],
        "turn_count": 0,
        "max_turns": 4,  # 토론 턴 수 (낙관 -> 비관 -> 낙관 -> 비관 -> 중재자)
        "current_agent": "start",
        "final_consensus": None
    }

    # 4. 그래프 생성 및 실행
    print("--- 멀티 에이전트 토론 시작 ---")
    graph = agent_debate_graph()
    result = graph.invoke(initial_state)

    # 5. 결과 출력
    print("\n===========================================")
    print("               최종 합의안")
    print("===========================================")
    print(result["final_consensus"])
    print("===========================================")

if __name__ == "__main__":
    main()

