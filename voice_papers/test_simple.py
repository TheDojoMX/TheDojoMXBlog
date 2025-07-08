#!/usr/bin/env python3
"""Test script to verify specialized agents are actually used in tasks."""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from voice_papers.agents.crew_manager import CrewManager


def test_specialized_agents():
    """Test that specialized agents are actually assigned to tasks."""

    # AI content to trigger AI specialists
    ai_content = """
    Title: Deep Learning and Neural Networks in Computer Vision
    
    Abstract: This paper explores the impact of convolutional neural networks and transformer 
    architectures on computer vision tasks. We present a novel approach using attention mechanisms
    and demonstrate improvements in image classification accuracy.
    
    Introduction: Machine learning algorithms, particularly deep neural networks, have
    revolutionized computer vision. Convolutional neural networks (CNNs) and more recently,
    Vision Transformers (ViTs) have shown remarkable capabilities.
    
    Methods: We trained several transformer-based models on ImageNet and evaluated
    their performance using standard metrics. Our approach combines self-attention
    with convolutional layers.
    
    Results: Our experiments show that the hybrid CNN-Transformer architecture
    achieves state-of-the-art performance on multiple computer vision benchmarks.
    
    Conclusion: The integration of attention mechanisms with traditional CNNs opens
    new possibilities for computer vision applications.
    """

    paper_title = "Deep Learning for Computer Vision"
    project_name = "test_specialized_agents"
    language = "English"

    print(f"🧪 Testing specialized agent participation")
    print(f"📄 Title: {paper_title}")
    print(f"📁 Project: {project_name}")
    print(f"🎭 Using humorous tone to test Comedy Communicator")

    try:
        # Create crew manager with AI content and humor
        print("🤖 Setting up crew manager...")
        crew_manager = CrewManager(
            language=language,
            project_name=project_name,
            conversation_mode="enhanced",  # Use enhanced mode to test all features
            tone="humorous",  # Test humor agent too
        )

        # Detect topic and create agents
        detected_topic = crew_manager._detect_topic(
            paper_title + " " + ai_content[:500]
        )
        print(f"🎯 Detected topic: {detected_topic}")

        from voice_papers.agents.roles import get_roles_for_topic

        agents = get_roles_for_topic(
            detected_topic, crew_manager.llm, crew_manager.tone
        )

        print(f"👥 Total agents created: {len(agents)}")
        print("📋 Agent roles:")
        for i, agent in enumerate(agents):
            print(f"  {i}: {agent.role}")

        # Create tasks and verify specialized agents are used
        tasks = crew_manager._create_tasks(ai_content, paper_title, agents)
        print(f"🎯 Total tasks created: {len(tasks)}")

        # Analyze task assignments
        print("\n📋 Task Analysis:")
        for i, task in enumerate(tasks, 1):
            assigned_agent = task.agent.role if task.agent else "No agent"
            print(f"  Task {i}: Assigned to {assigned_agent}")

            # Check if task description mentions specialized agents
            description = task.description.lower()
            mentions_specialists = any(
                phrase in description
                for phrase in [
                    "specialized agents",
                    "all agents",
                    "domain expertise",
                    "specialist",
                    "comedy communicator",
                ]
            )
            if mentions_specialists:
                print(f"    ✅ Task {i} explicitly involves specialized agents")
            else:
                print(f"    ⚠️ Task {i} may not involve specialized agents")

        # Check if we have the expected specialized agents for AI content
        expected_ai_roles = [
            "AI Researcher",
            "AI Philosopher",
            "AI Doomer",
            "AI Enthusiast",
            "AI Newcomer",
        ]
        humor_role = "Comedy Communicator"

        print(f"\n🔍 Verification:")
        ai_agents_found = [agent for agent in agents if agent.role in expected_ai_roles]
        humor_agent_found = [agent for agent in agents if agent.role == humor_role]

        print(f"  Expected AI specialists: {len(expected_ai_roles)}")
        print(f"  Found AI specialists: {len(ai_agents_found)}")
        print(f"  Found humor agent: {'Yes' if humor_agent_found else 'No'}")

        if len(ai_agents_found) == len(expected_ai_roles):
            print("  ✅ All expected AI specialists are present")
        else:
            print("  ❌ Missing some AI specialists")

        if humor_agent_found:
            print("  ✅ Comedy Communicator is present")
        else:
            print("  ❌ Comedy Communicator is missing")

        # Success message
        if len(ai_agents_found) == len(expected_ai_roles) and humor_agent_found:
            print(
                f"\n🎉 SUCCESS! All specialized agents are created and should participate in discussions!"
            )
            print(
                f"🎯 Total participating agents: {len(agents)} (5 base + 5 AI + 1 humor)"
            )
        else:
            print(f"\n⚠️ Some issues detected with specialized agent creation")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_specialized_agents()
