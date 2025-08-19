#!/usr/bin/env python3
"""Test pure technical extraction of the betting against agents article."""

from voice_papers.agents.o3_llm import O3LLM
from voice_papers.agents.technical_writer import get_technical_writer_agent, create_technical_writing_task
from voice_papers.config import OPENAI_API_KEY
from crewai import Task, Crew

# Read the synthesis
with open("projects/test_objective_betting_agents/synthesis/synthesis_concatenation.txt", "r") as f:
    content = f.read()

# Get LLM and agent
llm = O3LLM(api_key=OPENAI_API_KEY, model="o3-mini")
agent = get_technical_writer_agent(llm)

# Create task for technical extraction
task_description = create_technical_writing_task(
    content=content,
    title="Why I'm Betting Against AI Agents in 2025",
    target_length="comprehensive",
    language="Spanish"
)

# Run the extraction
task = Task(
    description=task_description,
    agent=agent,
    expected_output="Extracción técnica objetiva con atribución adecuada de opiniones"
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True
)

print("Running technical extraction...\n")
result = crew.kickoff()

# Save the result
with open("technical_extraction_result.txt", "w", encoding="utf-8") as f:
    f.write(str(result))

print("\n\nTechnical extraction saved to technical_extraction_result.txt")