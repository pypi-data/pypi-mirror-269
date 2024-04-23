import pandas as pd
import numpy as np
import gym
from gym import spaces
from stable_baselines3.common.vec_env import DummyVecEnv, VecNormalize, SubprocVecEnv
import empyrical as ep
from typing import List, Tuple, Any, Optional, Dict
from tradegym.rewards import all_rewards_func


class TradingEnv(gym.Env):
    """Trading environment for reinforcement learning.

    This environment is for training trading algorithms using reinforcement learning. It 
    allows the agent to take actions representing portfolio weights for different assets.

    Attributes:
        metadata: Metadata for the environment rendering.
    """
    metadata = {"render.modes": ["human"]}

    def __init__(self, 
            data: pd.DataFrame,
            window: int = 1, 
            features_list: list = None,
            mode_train: bool = False, 
            random_start_step: bool = False,
            reward_type: str = "tanh_rew", 
            reward_settings: dict = {'alpha': 0.19, 'beta': 0.145},
            risk_free_rate: float = 0.0005,
            reward_metric_window: int = 24, 
            init_balance: float = 10_000,
            verbose: int = 0, 
            random_seed: int = 10,
            buy_commission: float = 0.03, # in percentage
            sell_commission: float = 0.03, # in percentage
            obs_type: str = 'np' # 'pd'
            ):
        
        self.data = data
        self.window = window

        if features_list is None or len(features_list) == 0:
            self.features_list = ['open', 'high', 'low', 'close', 'volume']
        else:
            self.features_list = features_list
        self.reward_settings = reward_settings
        self.mode_train = mode_train
        self.random_start_step = random_start_step
        self.reward_type = reward_type
        self.risk_free_rate = risk_free_rate
        self.reward_metric_window = reward_metric_window
        self.init_balance = init_balance
        self.verbose = verbose
        self.random_seed = random_seed
        self.buy_commission = buy_commission
        self.sell_commission = sell_commission
        self.obs_type = obs_type

        # data preprocessing
        self.data = self.data.sort_values(['date', 'symbol'])
        self.data.reset_index(drop=True, inplace=True)
        self.data.ffill(inplace=True)
        self.data.fillna(0, inplace=True)

        self._check_dates(self.data)

        fe_lst = self.features_list.copy()
        fe_lst.extend(['date', 'symbol'])
        #fe_lst = list(set(('date', 'symbol', *self.features_list)))

        if self.obs_type == 'np':
            self.fe_data = self._data_to_3d_tensor(self.data[fe_lst])

            self.data_close = self._data_to_3d_tensor(self.data[['date', 'symbol', 'close']].copy())
            self.data_close = self.data_close[:, :, 0]
        elif self.obs_type == 'pd':
            self.fe_data = self.data.copy()
            self.data_close = self._data_to_3d_tensor(self.data[['date', 'symbol', 'close']].copy())
            self.data_close = self.data_close[:, :, 0]
        else:
            raise ValueError("Invalid observation type. Use 'pd' or 'np'.")
            

        # Unique symbols and dates in the dataset
        self.all_dates = np.array(self.data.date.unique())
        self.total_dates = len(self.data.date.unique())

        self.symbols = list(self.data.symbol.unique())
        self.stock_dimension = len(self.symbols)

        if self.window > self.total_dates:
            raise ValueError("Window size is larger than the number of dates.")

        # Observation and action spaces
        if self.obs_type == 'np':
            if self.window > 1:
                self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(self.window, self.fe_data.shape[1], self.fe_data.shape[2]), dtype=np.float32)
            else:
                self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(self.fe_data.shape[1], self.fe_data.shape[2]))
        elif self.obs_type == 'pd':
            if self.window > 1:
                self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(self.window, len(self.features_list), self.stock_dimension),)
            else:
                self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(len(self.features_list), self.stock_dimension),)


        # The agent can choose to buy from 0% to 100% of any stock or future contracts available in the portfolio
        self.action_space = spaces.Box(low=-1, high=1, shape=(self.stock_dimension,)) #STOCKS + USDT

        # seed for reproducibility
        _ = self.seed(self.random_seed)

        # initialize memory structures
        self.reset()

    def _check_dates(self, df: pd.DataFrame):
        """Check that the number of dates for each symbol matches.
        
        Args:
            df (DataFrame): Input data.
            
            Raises:
                ValueError: If the number of dates for each symbol does not match.
        """
        symbol_counts = df.groupby('symbol')['date'].count()
        if symbol_counts.std() != 0:
            raise ValueError('The number of dates for each symbol does not match.')

    def _data_to_3d_tensor(self, data: pd.DataFrame) -> np.array:
        """
        Convert input data to 3D tensor.

        Args:
            data (DataFrame): Input data.

        Returns:
            np.array: Transformed 3D tensor.
        """
        df = data.sort_values(['date', 'symbol']).copy()
        df = df.set_index(['date', 'symbol'])
        dates = df.index.get_level_values('date').unique()
        data_3d = np.array([df.loc[date].values for date in dates])
        return data_3d
    
    def reset(self) -> np.array:
        """Reset the state of the environment to an initial state.

        Returns:
            np.array: The initial state.

        """
        # Initialize memory structures
        self.actions_memory = [np.zeros(self.stock_dimension),]
        self.total_commission = 0
        self.total_commission_memory = [0,]
        self.balance = self.init_balance
        self.balance_memory = [self.init_balance,]
        self.finish_portfolio_value = 0
        self.portfolio_value_memory = [0,]
        self.date_memory = [self.all_dates[0],]
        self.portfolio_weights = np.zeros(self.stock_dimension)
        self.portfolio_weights_memory = [self.portfolio_weights,]

        # Initialize an empty array to store the asset prices
        self.asset_prices = np.zeros(self.stock_dimension)
        self.asset_prices_memory = [self.asset_prices,]
        self.positions = np.zeros(self.stock_dimension)
        self.positions_memory = [np.zeros(self.stock_dimension),]
        self.total_profit_memory = [0,]
        # Rewards received for each trading step i.e profit or loss
        self.reward_memory = [0,]
        self.trades = 0

        # Initialize reward
        self.reward = 0
        self.episode = 0

        # Reset counters and memory
        self.current_step = 0
        self.total_step_profit = 0
        self.done = False

        # if self.mode_train and self.random_start_step:
        #     # Randomly select a starting point for each episode
        #     # This introduces some randomness in the data the agent sees in each episode, 
        #     # helping the agent to explore different market conditions.
        #     max_starting_point = self.total_dates - (self.reward_metric_window * 3)  # Reserve 500 timesteps for the episode
        #     self.data_step = np.random.randint(self.window, max_starting_point)
        # else:
        self.data_step = self.window+1

        self.current_date = self.all_dates[self.data_step]
        self.date_memory = [self.current_date,]

        # get the first state
        state = self.get_state(self.data_step)
        return state
    
    def get_state(self, data_step: int) -> np.array:
        """Retrieve the current state of the environment.

        Args:
            data_step (int): The current step in the data.

        Returns:
            np.array: The current state.

        """
        # Get the current window of data
        if self.obs_type == 'np':
            if self.window > 1:
                obs = self.fe_data[(data_step-self.window + 1):data_step + 1]
            else:
                obs = np.array(self.fe_data[data_step])
        elif self.obs_type == 'pd':
            # slice windows df
            obs = self.fe_data[((data_step-self.window + 1)*len(self.symbols)):(data_step + 1)*len(self.symbols)].copy()
            #obs = obs.drop(['date', 'symbol'], axis=1)
            #obs = obs.values

        # Get the current date
        self.current_date = self.all_dates[data_step]

        # Get the current asset prices
        self.asset_prices = self.data_close[data_step]
        return obs
    
    def seed(self, seed: int = 1) -> list:
        """Set the random seed for the environment.

        Args:
            seed (int, optional): The random seed value.

        Returns:
            list: The random seed.

        """
        self.np_random, seed = gym.utils.seeding.np_random(seed)
        return [seed]

    def get_sb_env(self, num_workers = 1) -> Tuple[DummyVecEnv, np.array]:
        """Get Stable Baselines Environment.

        Returns:
            A tuple containing the DummyVecEnv and initial observation.
        """
        
        if num_workers > 1:
            e = SubprocVecEnv([lambda: self for i in range(num_workers)])
        else:
            e = DummyVecEnv([lambda: self])
        obs = e.reset()
        return e, obs
    
    def render(self, mode: str = "human"):
        """Render the environment.

        Args:
            mode (str, optional): The mode for rendering.

        """
        # simple rendering of the current state
        print(
            f"Date: {self.date_memory[-1]}, Balance: {self.balance:.2f}, " \
            f"Portfolio Value: {self.finish_portfolio_value:.2f}, " \
            f"Profit: {self.total_step_profit:.2f}, " \
            f"Trades: {self.trades}, " \
            f"Total Commission: {self.total_commission:.5f}"
            )

    def _calculate_commission(self, balance, portfolio_weights, old_portfolio_weights, positions, asset_prices, buy_commission, sell_commission):
        """Calculate commission for the trading.

        Args:
            balance: Current balance.
            portfolio_weights: New portfolio weights.
            old_portfolio_weights: Old portfolio weights.
            positions: Current positions.
            asset_prices: Current asset prices.
            buy_commission: Buy commission rate.
            sell_commission: Sell commission rate.

        Returns:
            Total commission cost.
        """

        changes_in_quantity = (np.divide(portfolio_weights, old_portfolio_weights, out=np.zeros_like(portfolio_weights), where=old_portfolio_weights!=0) * positions) - positions
        changes_in_quantity[old_portfolio_weights==0] = (balance*portfolio_weights/asset_prices)[old_portfolio_weights==0]


        buy_cost = np.sum(np.maximum(changes_in_quantity*asset_prices, 0))
        sell_cost = np.sum(np.abs(np.minimum(changes_in_quantity*asset_prices, 0)))
        total_buy_commission = buy_cost * (buy_commission / 100)
        total_sell_commission = sell_cost * (sell_commission / 100)
        total_commission = total_buy_commission + total_sell_commission

        if np.isfinite(total_commission):
            total_commission = round(total_commission, 10)

        if np.isnan(total_commission):
            total_commission = 0
        return total_commission
    
    def _norm_portfolio_weights(self, actions):
        """Normalize portfolio weights.

        Args:
            actions: Actions representing raw portfolio weights.

        Returns:
            Normalized portfolio weights.
        """
        # Calculating the portfolio weights based on actions
        total_action = np.sum(np.abs(actions)) 
        if total_action > 1:
            portfolio_weights = actions / total_action if total_action != 0 else np.zeros(self.stock_dimension)
        else:
            portfolio_weights = actions
        portfolio_weights = np.clip(portfolio_weights, -1, 1)
        portfolio_weights = np.round(portfolio_weights, 3)
        return portfolio_weights
    
    def _get_reward(self):
        """Calculate the reward based on the selected reward type."""
        if self.reward_type in ["sharpe", "sortino", 'mean_return', 'alpha_penalize']:
            if self.current_step < self.reward_metric_window or len(self.balance_memory) < self.reward_metric_window:
                self.reward = 0
            else:
                # Setup
                self.reward_settings['balances'] = self.balance_memory[(self.current_step - self.reward_metric_window) -1: self.current_step]
                self.reward_settings['returns'] = np.diff(self.reward_settings['balances']) / self.reward_settings['balances'][:-1]
                self.reward_settings['risk_free_rate'] = self.risk_free_rate
                self.reward_settings['total_commission'] = self.total_commission
                
                # Calculate metrics
                self.reward = all_rewards_func[self.reward_type](**self.reward_settings)
        
        else:
            self.reward_settings['asset_prices'] = self.asset_prices
            self.reward_settings['old_asset_prices'] = self.old_asset_prices
            self.reward_settings['portfolio_weights'] = self.portfolio_weights
            self.reward_settings['total_step_profit'] = self.total_step_profit

            # Calculate metrics
            self.reward = all_rewards_func[self.reward_type](**self.reward_settings)

        # Handling edge cases to avoid NaN or infinite rewards
        if not np.isfinite(self.reward):
            self.reward = 0
    
    def _calc_positions(self, portfolio_weights: np.array, balance: float, asset_prices: np.array):
        """Calculate positions based on portfolio weights and current balance.

        Args:
            portfolio_weights: Portfolio weights.
            balance: Current balance.
            asset_prices: Current asset prices.

        Returns:
            Positions.
        """
        positions = (portfolio_weights * balance) / asset_prices
        return positions
    
    def _calc_portfolio_value(self, positions: np.array, asset_prices: np.array):
        """Calculate portfolio value based on positions and current asset prices.

        Args:
            positions: Current positions.
            asset_prices: Current asset prices.

        Returns:
            Portfolio value.
        """
        portfolio_value = np.round(np.sum(np.abs(positions) * asset_prices), 3)
        return portfolio_value
    
    def _calc_portfolio_weights(self, balance: int, positions: np.array, asset_prices: np.array):
        """Calculate portfolio weights based on current positions and asset prices."""
        asset_values = positions * asset_prices #+ self.portfolio_weights[-1]*self.balance  # Value of each asset
        total_portfolio_value = np.sum(np.abs(asset_values))  # Total portfolio value
        allocate_cash_pcr = (balance - total_portfolio_value)/balance  # Value to allocate to cash
        
        portfolio_weights_full = np.zeros(len(asset_prices))

        if total_portfolio_value > 0: # if there are assets in the portfolio
            portfolio_weights = (asset_values / total_portfolio_value)*(1-allocate_cash_pcr)  # Portfolio weights
            #portfolio_weights_full[:len(asset_prices)] =  portfolio_weights
            portfolio_weights_full =  portfolio_weights

        #portfolio_weights_full[-1] = allocate_cash_pcr

        return np.round(portfolio_weights_full, 2)

    def _step_profit(self, asset_prices: np.array, old_asset_prices: np.array, positions: np.array):
        """Calculate the total profit or loss from the current step.

        Args:
            asset_prices: Current asset prices.
            old_asset_prices: Asset prices from the previous step.
            positions: Current positions.

        Returns:
            Total profit
        """
        price_change = asset_prices - old_asset_prices

        # Calculate the profit or loss for long and short positions
        long_profit_loss = np.sum(np.where(positions > 0, positions * price_change, 0))
        short_profit_loss = np.sum(np.where(positions < 0, positions * -price_change, 0))

        step_profit = (long_profit_loss - short_profit_loss)
        return step_profit

    def _update_memory_structures(self):
        # Update portfolio_weights
        self.portfolio_value = self._calc_portfolio_value(self.positions, self.asset_prices)
        self.portfolio_weights = self._calc_portfolio_weights(self.balance, self.positions, self.asset_prices)

        # Update the memory structures
        #self.actions_memory.append(actions)
        self.portfolio_value_memory.append(self.portfolio_value)
        self.total_profit_memory.append(self.total_step_profit)
        self.portfolio_weights_memory.append(self.portfolio_weights.copy())
        self.asset_prices_memory.append(self.asset_prices.copy())
        self.reward_memory.append(self.reward)
        self.balance_memory.append(self.balance)
        self.total_commission_memory.append(self.total_commission)
        self.date_memory.append(self.current_date)

    def step(self, actions: np.array) -> Tuple[np.array, float, bool, Dict[str, Any]]:
        """Execute one time step within the environment.

        Args:
            actions: An array of actions to execute in the environment.

        Returns:
            A tuple containing the next state, reward, done, and info.
        """
        ####################################### Chenge positions #######################################
        self.actions_memory.append(actions.copy())
        
        self.old_portfolio_weights = self.portfolio_weights.copy()
        self.old_asset_prices = self.asset_prices.copy() 
        
        self.new_portfolio_weights = self._norm_portfolio_weights(actions)
        # Commission
        self.total_commission = self._calculate_commission(
            self.balance,
            self.new_portfolio_weights, #[:-1], #the last is usdt
            self.old_portfolio_weights, #[:-1],
            self.positions,
            self.asset_prices,
            self.buy_commission,
            self.sell_commission,
            )
        # Update the balance based on the commission
        
        self.balance -= self.total_commission
        # Trades
        if self.total_commission > 0:
            self.trades+=1

        ## Calculate the updated positions after accounting for commissions
        self.positions = self._calc_positions(self.new_portfolio_weights, self.balance, self.asset_prices)
        ####################################### Get new prices ##########################################
        # Move to the next time step
        self.current_step += 1
        self.data_step += 1

        # Get the new state
        state = self.get_state(self.data_step)
        
        # total profit from the current step
        self.step_profit = self._step_profit(self.asset_prices, self.old_asset_prices, self.positions)
        self.total_step_profit = self.step_profit - self.total_commission
        # Update the balance based on the reward
        self.balance += self.step_profit

        # Calculate reward
        self._get_reward()

        # Check if the episode is done
        if self.data_step == self.total_dates - 1 or self.balance <= 0:
            self.done = True

        ####################################### Save data ##############################################
        # Update the memory structures
        #self.portfolio_weights = self.new_portfolio_weights
        self._update_memory_structures()

        info = {}
        return state, self.reward, self.done, info

    def save_balance_memory(self):
        df_memory = pd.DataFrame(
            {
                "date": self.date_memory, 
                "account_value": self.balance_memory,
            }
            )
        return df_memory

    def save_memory(self):
        df_memory = pd.DataFrame(
            {
                "date": self.date_memory, 
                "account_value": self.balance_memory,
                "actions": self.actions_memory,
                "portfolio_weights": self.portfolio_weights_memory,
                "portfolio_value": self.portfolio_value_memory,
                "reward": self.reward_memory,
            }
        )
        return df_memory

    def save_action_memory(self, action_list=None):
        if self.stock_dimension > 1:
            # date and close price length must match actions length
            date_list = self.date_memory
            df_date = pd.DataFrame(date_list)
            df_date.columns = ["date"]

            if action_list is None:
                action_list = self.actions_memory
            else:
                action_list = action_list
            
            df_actions = pd.DataFrame(action_list)
            df_actions.columns = self.symbols
            df_actions.index = df_date.date
        else:
            date_list = self.date_memory[:-1]
            action_list = self.actions_memory
            df_actions = pd.DataFrame({"date": date_list, "actions": action_list})
            
        return df_actions