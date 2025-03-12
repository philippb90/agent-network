#!/usr/bin/env python
"""
Script to run a business idea evaluation using the agent network.
"""

import os
import sys
import time

# Add parent directory to path to import agent_network
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_network.config import ConfigManager
from agent_network.agents.qwen_agent import QwenAgent
from agent_network.mediator.agent_mediator import AgentMediator
from agent_network.evaluation.conversation_evaluator import ConversationEvaluator


def load_idea_file(file_path):
    """Load the business idea file content.

    Args:
        file_path: Path to the idea file.

    Returns:
        String content of the file.
    """
    with open(file_path, "r") as f:
        return f.read()


def main():
    """Run the business idea evaluation."""
    # Check for idea file argument
    if len(sys.argv) > 1:
        idea_file = sys.argv[1]
    else:
        idea_file = os.path.join(os.path.dirname(__file__), "idea.txt")
    
    if not os.path.exists(idea_file):
        print(f"Error: Idea file '{idea_file}' not found.")
        return 1

    # Load configuration
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "config/business_eval_config.yaml"
    )
    
    if not os.path.exists(config_path):
        print(f"Error: Configuration file '{config_path}' not found.")
        return 1

    config_manager = ConfigManager(config_path)
    
    # Load idea file content
    idea_content = load_idea_file(idea_file)
    
    # Create agents
    print("Creating Business Analyst agent...")
    agent1 = QwenAgent(
        agent_config=config_manager.get_agent_config("agent_1"),  # Business Analyst
        model_config=config_manager.get_model_parameters(),
        agent_id="agent_1"
    )

    print("Creating Venture Capital Analyst agent...")
    agent2 = QwenAgent(
        agent_config=config_manager.get_agent_config("agent_2"),  # VC Analyst
        model_config=config_manager.get_model_parameters(),
        agent_id="agent_2"
    )

    # Create mediator
    print("Creating mediator for business evaluation...")
    mediator = AgentMediator(
        agent1=agent1,
        agent2=agent2,
        interaction_params=config_manager.get_interaction_parameters(),
        system_config=config_manager.get_system_config()
    )

    # Create evaluator
    evaluator = ConversationEvaluator(
        agent1_config=config_manager.get_agent_config("agent_1"),
        agent2_config=config_manager.get_agent_config("agent_2")
    )

    # Prepare starting prompt with the business idea
    starting_prompt = f"""
As a Business Analyst, your task is to analyze and create a comprehensive business plan 
for the following business idea:

{idea_content}

Please analyze this idea thoroughly and present your business plan to the Venture Capital Analyst.
"""

    # Print header
    print("\n" + "=" * 80)
    print(f"BUSINESS IDEA EVALUATION: {os.path.basename(idea_file)}")
    print("=" * 80)

    # Callback to print messages as they are generated
    def print_message(agent_name, message, turn, is_complete):
        print(f"\n[Turn {turn + 1}] {agent_name}:")
        print(message)
        if is_complete:
            print("\n" + "=" * 80)
            print("EVALUATION COMPLETE")
            print("=" * 80)

    # Run conversation
    print("\nStarting business evaluation process...")
    start_time = time.time()
    
    results = mediator.run_complete_conversation(
        starting_prompt=starting_prompt,
        callback=print_message
    )
    
    end_time = time.time()

    # Print summary
    print(f"\nEvaluation completed in {end_time - start_time:.2f} seconds")
    print(f"Conversation saved in {config_manager.get_system_config().get('conversation_dir', 'conversations')}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())