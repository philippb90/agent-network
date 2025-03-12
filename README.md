# Agent Network

A network of AI agents that can interact in a hierarchical structure, simulating company-like interactions between supervisor and worker agents.

## Overview

This project implements a dual-agent system where agents interact in a supervisor-worker relationship, similar to a company setting. The supervisor agent assigns tasks, provides requirements, and reviews work, while the worker agent executes tasks and provides progress updates.

## Features

- **Hierarchical Agent Structure**: Supervisor-worker relationship between agents
- **Task Management**: Clear task assignment and tracking
- **Quality Control**: Built-in evaluation of task completion and interaction quality
- **Flexible Configuration**: Easily configurable agent roles and interaction parameters
- **Conversation Memory**: Persistent storage of agent interactions
- **Performance Evaluation**: Automated assessment of agent performance and role adherence

## Installation

1. Clone the repository:
```bash
git clone https://github.com/philippb90/agent-network.git
cd agent-network
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

The system uses a YAML-based configuration system. The main configuration parameters are:

- **Agent Roles**: Define supervisor and worker behaviors
- **Interaction Parameters**: Control conversation flow and limits
- **Model Parameters**: Configure the underlying language model
- **System Settings**: Set up logging and storage options

## Usage

Basic usage example:

```python
from agent_network.config import ConfigManager
from agent_network.agents.qwen_agent import QwenAgent
from agent_network.mediator.agent_mediator import AgentMediator
from agent_network.evaluation.conversation_evaluator import ConversationEvaluator

# Load configuration
config_manager = ConfigManager()

# Create agents
agent1 = QwenAgent(
    agent_config=config_manager.get_agent_config("agent_1"),  # Supervisor
    model_config=config_manager.get_model_parameters(),
    agent_id="agent_1"
)

agent2 = QwenAgent(
    agent_config=config_manager.get_agent_config("agent_2"),  # Worker
    model_config=config_manager.get_model_parameters(),
    agent_id="agent_2"
)

# Create mediator
mediator = AgentMediator(
    agent1=agent1,
    agent2=agent2,
    interaction_params=config_manager.get_interaction_parameters(),
    system_config=config_manager.get_system_config()
)

# Run interaction
results = mediator.run_complete_conversation()
```

## Evaluation

The system includes built-in evaluation metrics:

- Task completion rate
- Role adherence
- Communication effectiveness
- Goal achievement
- Quality of deliverables

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.