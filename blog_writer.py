import os
import logging

from crewai import Agent, Task, Crew
from IPython.display import Markdown
from openai import OpenAI
from crewai import LLM

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("blog_writer.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("blog_writer")

def get_openai_api_key():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return openai_api_key

openai_api_key = get_openai_api_key()

# Change the llm based on remote or local
# client = OpenAI(api_key=openai_api_key)
# llm = os.getenv("OPENAI_MODEL")
llm = LLM(
    model="ollama/mistral:7B", # change to your model
    base_url="http://localhost:11434"
)

planner = Agent(
    role="Blog Planner",
    goal="Plan engaging and factually accurate Blog on {topic}",
    backstory="You're working on planning a blog article about the topic: {topic}. \
                You collect information that helps the audience learn something \
                and make informed decisions. Your work is the basis for the Blog Writer.",
    allow_delegation=False,
	verbose=True,
    llm = llm
)

writer = Agent(
    role="Blog Writer",
    goal="Write insightful and factually accurate "
         "opinion piece about the topic: {topic}",
    backstory="You're working on a writing a new opinion piece about the topic: {topic} \
                You base your writing on the work of the Blog Planner, \
                who provides an outline and key points for the article. \
                You follow the main objectives and direction of the outline. \
                You also provide impartial insights and back them up with information \
                provided by the Blog Planner.",
    allow_delegation=False,
    verbose=True,
    llm = llm
)

editor = Agent(
    role="Editor",
    goal="Edit a given blog post to align with "
         "the writing style of the organization. ",
    backstory="You are an editor who receives a blog post from the Blog Writer. \
                Your job is to proofread the blog post for grammatical errors, \
                provide balanced feedback to avoid bias, avoid controversies \
                and make any necessary corrections.",
    allow_delegation=False,
    verbose=True,
    llm = llm
)

plan = Task(
    description=(
        "1. Prioritize the latest trends, key players, and noteworthy news on {topic}.\n \
        2. Identify the target audience, considering their interests and pain points.\n \
        3. Develop a detailed Blog outline including an introduction, key points, \
                and a call to action.\n \
        4. Include SEO keywords and relevant data or sources.\n"
    ),
    expected_output="A comprehensive Blog plan document "
        "with an outline, audience analysis, "
        "SEO keywords, and resources.",
    agent=planner,
)

write = Task(
    description=(
        "1. Use the Blog plan to craft a compelling blog post on {topic}.\n \
        2. Incorporate SEO keywords naturally.\n \
		3. Sections/Subtitles are properly named in an engaging manner.\n \
        4. Ensure the post is structured with an engaging introduction, \
            insightful body, and a summarizing conclusion.\n \
        5. Simplify the content for easy reading and understanding \
            for Teenager audience.\n \
        6. Proofread for grammatical errors\n"
    ),
    expected_output="A well-written blog post "
        "in markdown format, ready for publication, "
        "each section should have 2 or 3 paragraphs.",
    agent=writer,
)

edit = Task(
    description=("Proofread the given blog post for grammatical errors."),
    expected_output="A well-written blog post in markdown format, "
                    "ready for publication, each section should have 2 or 3 paragraphs.",
    agent=editor
)

crew = Crew(
    agents=[planner, writer, editor],
    tasks=[plan, write, edit],
    verbose=True
)

def main():
    generate_blog_post("Agentic AI")

def generate_blog_post(topic):
    result = crew.kickoff(inputs={"topic": topic}, )
    print(result)
    print(Markdown(result["raw"]))
    return result

if __name__ == "__main__":
    
    # Run the main process
    main()
    print("Process completed successfully!")
