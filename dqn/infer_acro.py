from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv
import gymnasium as gym

env = gym.make('Acrobot-v1', render_mode='human')
env = DummyVecEnv([lambda: env])

model = DQN.load("dqn_acrobat")
obs = env.reset()

for _ in range(1000):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    if done:
        obs = env.reset()
env.close()

