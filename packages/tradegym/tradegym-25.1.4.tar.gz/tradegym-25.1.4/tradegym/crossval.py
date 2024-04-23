import pandas as pd
import numpy as np
from datetime import datetime
from typing import Any, Dict, Type
from tqdm import tqdm
from pathlib import Path
#import ffn
import quantstats as qs
#import vectorbt as vbt
import plotly

MODELS_FOLDER = "models"

class BackTest():
    """
    Backtest Agent. This class is used to backtest the model.
    """
    def __init__(self,
                env: Type,
                agent: Type,
                verbose: int = 1,
                verbose_step: int = 1000,
                benchmark_coin_name='BTC-USDT-PERP',
                ):
        self.verbose = verbose
        self.verbose_step = verbose_step
        self.benchmark_coin_name = benchmark_coin_name

        self.env = env
        self.agent = agent

    def print_metrics(self, metrics: dict) -> None:
        # Note that the dollar signs in f-strings were escaped by doubling them
        print(
            f'> Model Agent Total Profit: {metrics["profit_$"]:<6}$'
            f' | Cumulative Return: {metrics["return_%"]:<4}%'
            f' | Sharpe: {metrics["sharpe"]:<5.2f}'
            f' | Sortino: {metrics["sortino"]:<5.2f}'
            f' | Max Drawdown: {metrics["max_drawdown"] * 100}%'
            f' | Total Comission: {metrics["commission_$"]}$'
        )
        print('_' * 120)

    def render(self, deterministic: bool = True):
        obs = self.env.reset()

        i = 0
        while not self.env.done:
            action, _states = self.agent.predict(obs, deterministic=deterministic)
            obs, rewards, done, info = self.env.step(action)
            i += 1
            if self.verbose > 1 and i % self.verbose_step == 0:
                self.env.render()

        if self.verbose > 0:
            metrics = self.get_metrics()
            self.print_metrics(metrics)
        
    def get_balance_df(self) -> pd.DataFrame:
        if len(self.env.balance_memory) <= 1:
            raise Exception('You must .run() the backtest first!')
        # Create Balance DataFrame
        stategy = self.env.save_balance_memory().set_index('date')
        return stategy

    def get_benchmark_df(self) -> pd.DataFrame:
        # Create Benchmark DataFrame
        stategy = self.get_balance_df()
        bench = self.env.data.pivot_table(index='date', columns='symbol', values='close')
        bench['Strategy']= stategy['account_value']
        bench.dropna(inplace=True)
        return bench

    def get_profit_benchmark_df(self) -> pd.DataFrame:
        # Create Benchmark DataFrame
        bench = self.get_benchmark_df()
        profit_benchmark = (bench.divide(bench.iloc[0]) * self.env.init_balance) - self.env.init_balance
        return profit_benchmark

    def get_portfolio_weights_memory(self) -> list:
        if len(self.env.portfolio_weights_memory) <= 1:
            raise Exception('You must .run() the backtest first!')
        return self.env.portfolio_weights_memory

    def get_action_memory_df(self, action_list=None) -> list:
        if len(self.env.actions_memory) <= 1:
            raise Exception('You must .run() the backtest first!')
        return self.env.save_action_memory(action_list=action_list)

    def get_metrics(self, mode='base') -> dict:
        # Calculate bench
        bench = self.get_benchmark_df()

        metrics = {
            'start_date': bench.index[0].strftime('%Y-%m-%d %H:%M'),
            'end_date': bench.index[-1].strftime('%Y-%m-%d %H:%M'),
            'trade_days': (bench.index[-1] - bench.index[0]).days,
            'trades': self.env.trades,
            'initial_balance_$': np.round(self.env.init_balance,2),
            'final_balance_$': np.round(self.env.balance,2),
            'profit_$': np.round(self.env.balance - self.env.init_balance, 2),
            'commission_$': np.round(np.sum(self.env.total_commission_memory),2),
            'return_%': np.round((self.env.balance - self.env.init_balance) / self.env.init_balance * 100, 2),
            'max_drawdown': 0,
            'sharpe': 0,
            'sortino': 0,
            'calmar': 0,
            'profit_factor': 0,
            'value_at_risk': 0,
            }
        
        if metrics['trades'] != 0:
            metrics['max_drawdown'] = np.round(qs.stats.max_drawdown(bench['Strategy'])*100,2)
            metrics['sharpe'] = np.round(qs.stats.sharpe(bench['Strategy'],),3)
            metrics['sortino'] = np.round(qs.stats.sortino(bench['Strategy'],),3)
            metrics['calmar'] = np.round(qs.stats.calmar(bench['Strategy']),3)
            metrics['profit_factor'] = np.round(qs.stats.profit_factor(bench['Strategy']),2)
            metrics['value_at_risk'] = np.round(qs.stats.value_at_risk(bench['Strategy']),2)

            if mode == 'full':
                metrics['tail_ratio'] = np.round(qs.stats.tail_ratio(bench['Strategy']),2)
                metrics['common_sense_ratio'] = np.round(qs.stats.common_sense_ratio(bench['Strategy']),2)
                metrics['conditional_value_at_risk'] = np.round(qs.stats.conditional_value_at_risk(bench['Strategy']),2)
                metrics['information_ratio'] = np.round(qs.stats.information_ratio(bench['Strategy'], bench[self.benchmark_coin_name]),2)
                metrics['gain_to_pain_ratio'] = np.round(qs.stats.gain_to_pain_ratio(bench['Strategy']),2)
                metrics['ulcer_index'] = np.round(qs.stats.ulcer_index(bench['Strategy']),2)
        return metrics

    def check_total_trades(self) -> bool:
        metrics = self.get_metrics()
        if metrics['trades'] == 0:
            print('!!! No trades were made! nothing to plot')
            return False
        else:
            return True
    
    def plot_qs_report(self, bench_symbol='BTC-USDT-PERP', mode='full', ) -> None:
        if self.check_total_trades():
            bench = self.get_benchmark_df()
            qs.reports.plots(bench['Strategy'], benchmark=bench[bench_symbol], periods_per_year=365, mode=mode)

    def save_qs_report(self, bench_symbol='BTC-USDT-PERP', mode='full', name='quantstats-report.html') -> None:
        if self.check_total_trades():
            bench = self.get_benchmark_df()
            qs.reports.html(bench['Strategy'], benchmark=bench[bench_symbol], periods_per_year=365, mode=mode, output=name)

    def _get_plotly_fig(self, data: pd.DataFrame, template='plotly_dark', title="Weights", xaxis_title='Date', yaxis_title='Weight') -> plotly.graph_objs.Figure:
        traces = []

        for column in data.columns:
            traces.append(plotly.graph_objs.Scatter(x=data.index, y=data[column], mode='lines', name=column))

        layout = plotly.graph_objs.Layout(
            title=title,
            xaxis=dict(title=xaxis_title),
            yaxis=dict(title=yaxis_title)
            )

        fig = plotly.graph_objs.Figure(data=traces, layout=layout,)
        fig.update_layout(template=template)
        return fig
    
    def get_plot_profit_benchmark(self, profit_benchmark=None, template='plotly_dark') -> plotly.graph_objs.Figure:
        if profit_benchmark is None:
            profit_benchmark = self.get_profit_benchmark_df()
        fig = self._get_plotly_fig(data=profit_benchmark, template=template, title='Top Coins vs Strategy by Profit', yaxis_title='Profit $')
        return fig

    def get_plot_drawdowns_benchmark(self, profit_benchmark=None, template='plotly_dark') -> plotly.graph_objs.Figure:
        if profit_benchmark is None:
            profit_benchmark = self.get_profit_benchmark_df()
        profit_benchmark = profit_benchmark + self.env.init_balance
        # Вычисление максимума кумулятивной доходности до текущей даты
        cummax = profit_benchmark.cummax()
        # Вычисление посадки в процентах
        drawdowns_percent = ((profit_benchmark - cummax) / cummax) * 100
        # Визуализация
        traces = [plotly.graph_objs.Scatter(x=drawdowns_percent.index, y=drawdowns_percent[column], fill='tozeroy', name=column) for column in drawdowns_percent.columns]
        layout = plotly.graph_objs.Layout(title='Underwater Drawdowns', template=template, xaxis=dict(title='Date'), yaxis=dict(title='Drawdowns %'))
        fig = plotly.graph_objs.Figure(traces, layout=layout)
        return fig

    def get_plot_actions(self, template='plotly_dark',) -> plotly.graph_objs.Figure:
        df = self.get_action_memory_df()
        fig = self._get_plotly_fig(data=df, template=template, title='Actions',)
        return fig

    def get_plot_portfolio_weights(self, template='plotly_dark',) -> plotly.graph_objs.Figure:
        df = self.get_action_memory_df(action_list=self.env.portfolio_weights_memory)
        fig = self._get_plotly_fig(data=df, template=template, title='Portfolio Weights',)
        return fig

    # @staticmethod
    # def _get_avg_trades_per_day(df):
    #     trades_df = df.copy()
    #     # Преобразуйте Timestamp в формат datetime
    #     trades_df['Timestamp'] = pd.to_datetime(trades_df['Timestamp'])

    #     # Извлеките дату из Timestamp
    #     trades_df['Date'] = trades_df['Timestamp'].dt.date

    #     # Подсчитайте количество сделок за каждый день
    #     daily_trades = trades_df.groupby('Date').size()

    #     # Найдите среднее количество сделок в день
    #     average_trades_per_day = np.round(daily_trades.mean(), 1)
    #     return average_trades_per_day
    
    # def _get_vb_backtest(self, symbol, lot=0.1, freq='1h'):
    #     entries = self.get_action_memory_df()[symbol] > 0
    #     exits = self.get_action_memory_df()[symbol] <= 0

    #     short_entries = self.get_action_memory_df()[symbol] < 0
    #     short_exits = self.get_action_memory_df()[symbol] >= 0

    #     try:
    #         pf = vbt.Portfolio.from_signals(
    #             close = self.get_benchmark_df()[symbol], 
    #             entries = entries, 
    #             exits = exits, 
    #             short_entries = short_entries,
    #             short_exits = short_exits,
    #             fees = self.env.buy_commission/100, 
    #             freq = freq, 
    #             init_cash = self.env.init_balance,
    #             size = lot,  # 10% of current equity
    #             size_type = 'percent',  # Use percent of equity for sizing
    #             direction = 'both', 
    #             cash_sharing=False,
    #             )
    #     except:
    #         print(f'Error! Try use fix lot size {symbol}')
    #         try:
    #             pf = vbt.Portfolio.from_signals(
    #             close = self.get_benchmark_df()[symbol], 
    #             entries = entries, 
    #             exits = exits, 
    #             short_entries = short_entries,
    #             short_exits = short_exits,
    #             fees = self.env.buy_commission/100, 
    #             freq = freq, 
    #             init_cash = self.env.init_balance,
    #             size = self.env.init_balance*lot,  # 10% of init_cash
    #             #size_type = 0,
    #             direction = 'both', 
    #             cash_sharing=False,
    #             )
    #         except:
    #             print(f'No stat Error {symbol}')
    #             pf = None
    #     return pf

    # def get_stat_by_symbol_df(self, lot=0.1, freq='1h') -> pd.DataFrame:
    #     select_metrics = [
    #         'End Value', 
    #         'Total Return [%]', 
    #         'Benchmark Return [%]', 
    #         'Max Drawdown [%]', 
    #         'Max Drawdown Duration', 
    #         'Total Trades', 
    #         'Avg Trades by Day',
    #         'Win Rate [%]', 
    #         'Best Trade [%]', 
    #         'Worst Trade [%]', 
    #         'Avg Winning Trade [%]', 
    #         'Avg Losing Trade [%]', 
    #         'Avg Winning Trade Duration', 
    #         'Avg Losing Trade Duration', 
    #         'Profit Factor', 
    #         'Expectancy', 
    #         'Sharpe Ratio', 
    #         'Calmar Ratio', 
    #         #'Omega Ratio', 
    #         'Sortino Ratio'
    #     ]

    #     total_stat = {}

    #     for symbol in self.env.symbols:
    #         pf = self._get_vb_backtest(symbol=symbol, lot=lot, freq=freq)
    #         stats = pf.stats()
    #         # Average number of transactions per day
    #         stats['Avg Trades by Day'] = self._get_avg_trades_per_day(pf.orders.records_readable)
    #         total_stat[symbol] = stats.to_dict()

    #     bench_metrics_symbols = pd.DataFrame(total_stat).T.sort_values(by='Total Return [%]', ascending=False)[select_metrics]
    #     # Выбираем столбцы с типом float
    #     float_columns = bench_metrics_symbols.T.select_dtypes(include=['float64'])
    #     float_columns_ls = list(float_columns.index)

    #     # Заполняем пропуски нулями и округляем до 2 знаков после запятой
    #     bench_metrics_symbols = bench_metrics_symbols[float_columns_ls].fillna(0).round(2)
    #     return bench_metrics_symbols
    
    # def get_plot_trades_by_symbol(self, symbol, lot=0.1, freq='1h', template=None) -> plotly.graph_objs.Figure:
    #     pf = self._get_vb_backtest(symbol=symbol, lot=lot, freq=freq)
    #     fig = pf.plot(subplots=['cum_returns', 'orders', 'trades', 'trade_pnl'])
    #     if template:
    #         fig.update_layout(template=template)
    #     #fig = pf.plot().update_layout(template=template)
    #     return fig