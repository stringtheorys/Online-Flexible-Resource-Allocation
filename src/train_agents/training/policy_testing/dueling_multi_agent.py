"""Initial training of the agents using the basic environments"""

from __future__ import annotations

import gin

from agents.rl_agents.dueling_dqn import TaskPricingDuelingDqnAgent, ResourceWeightingDuelingDqnAgent
from agents.rl_agents.neural_networks.dueling_dqn_networks import DuelingDqnLstmNetwork
from env.environment import OnlineFlexibleResourceAllocationEnv
from train_agents.training_core import generate_eval_envs, run_training, setup_tensorboard

if __name__ == "__main__":
    gin.parse_config_file('./train_agents/training/standard_config.gin')

    folder = 'dueling_multi_agents'
    writer = setup_tensorboard(folder)

    env = OnlineFlexibleResourceAllocationEnv.make('./train_agents/env_settings/basic_env.json')
    eval_envs = generate_eval_envs(env, 5, f'./train_agents/eval_envs/{folder}/')

    task_pricing_agents = [
        TaskPricingDuelingDqnAgent(agent_num, DuelingDqnLstmNetwork(9, 10), save_folder=folder)
        for agent_num in range(3)
    ]
    resource_weighting_agents = [
        ResourceWeightingDuelingDqnAgent(agent_num, DuelingDqnLstmNetwork(10, 10), save_folder=folder)
        for agent_num in range(3)
    ]

    print('TP Agents: [' + ', '.join(agent.name for agent in task_pricing_agents) + ']')
    print('RW Agents: [' + ', '.join(agent.name for agent in resource_weighting_agents) + ']')

    with writer.as_default():
        run_training(env, eval_envs, 150, task_pricing_agents, resource_weighting_agents, 5)

    for agent in task_pricing_agents:
        agent._save()
    for agent in resource_weighting_agents:
        agent._save()

    print('TP Total Obs: {' + ', '.join(f'{agent.name}: {agent.total_obs}' for agent in task_pricing_agents) + '}')
    print(
        'RW Total Obs: {' + ', '.join(f'{agent.name}: {agent.total_obs}' for agent in resource_weighting_agents) + '}')
