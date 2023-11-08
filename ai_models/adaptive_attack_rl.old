import gym
import numpy as np
from stable_baselines3 import PPO
import logging
import argparse
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('AdaptiveAttackAgent')

class AdaptiveAttackAgent:
    def __init__(self, environment_name):
        self.environment = gym.make(environment_name)
        self.model = PPO('MlpPolicy', self.environment, verbose=1)
        self.model_path = None

    def train(self, time_steps=10000):
        try:
            self.model.learn(total_timesteps=time_steps)
            logger.info("Training completed.")
        except Exception as e:
            logger.error(f"An error occurred during training: {e}")

    def save_model(self, path):
        try:
            self.model.save(path)
            self.model_path = path
            logger.info(f"Model saved to {path}")
        except Exception as e:
            logger.error(f"An error occurred while saving the model: {e}")

    def load_model(self, path):
        try:
            self.model = PPO.load(path, self.environment)
            logger.info(f"Model loaded from {path}")
        except Exception as e:
            logger.error(f"An error occurred while loading the model: {e}")

    def deploy_strategy(self, observation):
        try:
            action, _states = self.model.predict(observation)
            return action
        except Exception as e:
            logger.error(f"An error occurred while deploying strategy: {e}")
            return None

    def evaluate(self, num_episodes=10):
        try:
            episode_rewards = []
            for i in range(num_episodes):
                obs = self.environment.reset()
                done = False
                total_reward = 0
                while not done:
                    action = self.deploy_strategy(obs)
                    obs, reward, done, info = self.environment.step(action)
                    total_reward += reward
                episode_rewards.append(total_reward)
            average_reward = np.mean(episode_rewards)
            logger.info(f"Average reward over {num_episodes} episodes: {average_reward}")
            return average_reward
        except Exception as e:
            logger.error(f"An error occurred during evaluation: {e}")
            return None

# Command-line argument parsing for versatility
def main():
    parser = argparse.ArgumentParser(description='Adaptive Attack RL Agent')
    parser.add_argument('environment_name', help='The name of the Gym environment')
    parser.add_argument('--train', help='Train the model for a given number of steps', type=int)
    parser.add_argument('--save', help='Path to save the trained model')
    parser.add_argument('--load', help='Path to load an existing model')
    parser.add_argument('--evaluate', help='Evaluate the model for a given number of episodes', type=int)
    args = parser.parse_args()

    agent = AdaptiveAttackAgent(args.environment_name)
    
    if args.load:
        agent.load_model(args.load)

    if args.train:
        agent.train(args.train)
        if args.save:
            agent.save_model(args.save)

    if args.evaluate:
        agent.evaluate(args.evaluate)

if __name__ == "__main__":
    main()
