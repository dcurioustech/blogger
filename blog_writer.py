import os, sys
import logging

from crewai import Agent, Task, Crew
from IPython.display import Markdown
from openai import OpenAI

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
llm = os.getenv("OPENAI_MODEL_NAME")

client = OpenAI(
    api_key=openai_api_key,
)

planner = Agent(
    role="Blog Planner",
    goal="Plan engaging and factually accurate Blog on {topic}",
    backstory="You're working on planning a blog article about the topic: {topic}.",
    allow_delegation=False,
	verbose=False,
    llm = llm
)

writer = Agent(
    role="Blog Writer",
    goal="Write insightful and factually accurate "
         "opinion piece about the topic: {topic}",
    backstory="You're working on a writing a new opinion piece about the topic: {topic}",
    allow_delegation=False,
    verbose=False,
    llm = llm
)

editor = Agent(
    role="Editor",
    goal="Edit a given blog post to align with "
         "the writing style of the organization. ",
    backstory="You are an editor who receives a blog post from the Blog Writer.",
    allow_delegation=False,
    verbose=False,
    llm = llm
)

plan = Task(
    description=(
        "1. Prioritize the latest trends, key players, "
            "and noteworthy news on {topic}.\n"
        "2. Identify the target audience, considering "
            "their interests and pain points.\n"
        "3. Develop a detailed Blog outline including "
            "an introduction, key points, and a call to action.\n"
        "4. Include SEO keywords and relevant data or sources.\n"
    ),
    expected_output="A comprehensive Blog plan document "
        "with an outline, audience analysis, "
        "SEO keywords, and resources.",
    agent=planner,
)

write = Task(
    description=(
        "1. Use the Blog plan to craft a compelling blog post on {topic}.\n"
        "2. Incorporate SEO keywords naturally.\n"
		"3. Sections/Subtitles are properly named in an engaging manner.\n"
        "4. Ensure the post is structured with an engaging introduction, \
            insightful body, and a summarizing conclusion.\n"
        "5. Simplify the content for easy reading and understanding \
            for Tech & Teenager audience.\n"
        "6. Proofread for grammatical errors\n"
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
    generate_blog_post("Machine Learning")

def generate_blog_post(topic):
    result = crew.kickoff(inputs={"topic": topic})
    return result

if __name__ == "__main__":
    
    # Run the main process
    main()
    print("Process completed successfully!")
