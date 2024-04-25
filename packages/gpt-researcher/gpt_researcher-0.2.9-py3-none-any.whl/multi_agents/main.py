from dotenv import load_dotenv
from agents import MasterAgent
import asyncio

load_dotenv()

task = {
    "query": "What is langgraph?",
    "max_sub_headers": 3,
}


async def main():
    master_agent = MasterAgent(task)
    final_report = await master_agent.run()
    print(final_report)
    return final_report

if __name__ == "__main__":
    asyncio.run(main())
