import numpy as np


class BaseAgent:
    __name__ = "BasedAgent"
    def __init__(self, police=None, env=None, seed=42, verbose=0, **kwargs):
        self.env = env
        self.seed = seed

    def predict(self, obs, deterministic=True):
        pass
    
    def learn(self, **kwargs):
        pass

    def save(self, path):
        pass

    def load(self, path):
        pass

#################### Baseline Agents ##################################################

class BuyAndHoldAgent(BaseAgent):
    __name__ = "BuyAndHoldAgent"
    def __init__(self, police=None, env=None, symbol='BTC-USDT-PERP', **kwargs):
        super().__init__(police=police, env=env, **kwargs)
        self.symbol = symbol

    def predict(self, obs, deterministic=True):
        action = np.zeros(self.env.action_space.shape)
        index = self.env.symbols.index(self.symbol)
        action[index] = 1.  # Buy coin
        #action[-1] = -1.
        return action, None


class RandomAgent(BuyAndHoldAgent):
    __name__ = "RandomAgent"
    def predict(self, obs, deterministic=True):
        action = np.zeros(self.env.action_space.shape)
        for i in range(len(action)):
            action[i] = np.random.uniform(-1., 1.)  # Buy or sell coins
        #action[-1] = -1.
        return action, None


class EqualWeightingAgent(BuyAndHoldAgent):
    __name__ = "EqualWeightingAgent"
    def predict(self, obs, deterministic=True):
        action = np.zeros(self.env.action_space.shape)
        for i in range(len(action)-1):
            action[i] = 1/(len(action)-1)
        action = np.round(action, 3)
        #action[-1] = -1.
        return action, None


class NoTradeAgent(BuyAndHoldAgent):
    __name__ = "NoTradeAgent"
    def predict(self, obs, deterministic=True):
        action = np.zeros(self.env.action_space.shape)
        #action[-1] = 1.
        return action, None


#################### Baseline Agents ##################################################

baseline_agents = {
    "BuyAndHoldAgent": BuyAndHoldAgent,
    "RandomAgent": RandomAgent,
    "EqualWeightingAgent": EqualWeightingAgent,
    "NoTradeAgent": NoTradeAgent,
}