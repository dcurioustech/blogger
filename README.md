# Blog Writer

## Overview

This project provides a framework for generating blog posts using AI agents. It leverages the `crewai` library to orchestrate a team of agents, each with a specific role, to plan, write, and edit blog content. The project also uses the OpenAI API to generate the content.

## Features

- **Agent-Based Architecture:** Uses `crewai` to define agents with specific roles (Planner, Writer, Editor) for blog creation.
- **Task Management:** Defines tasks for each agent to ensure a structured content creation process.
- **OpenAI Integration:** Utilizes the OpenAI API for content generation and editing.
- **Logging:** Configures logging to track the execution and any errors that may occur.
- **API Key Handling:** Securely retrieves the OpenAI API key from environment variables.
- **Text Formatting:** Includes a utility function to format the generated text for better readability.

## Requirements

- Python 3.12+
- `crewai`
- `openai`
- `IPython`
- `pytest` (for testing)

To install the dependencies, run:

```bash
pip install -r requirements.txt

# Environment variables to be set
OPENAI_MODEL_NAME=gpt-4o
OPENAI_API_KEY=<Your API Key>