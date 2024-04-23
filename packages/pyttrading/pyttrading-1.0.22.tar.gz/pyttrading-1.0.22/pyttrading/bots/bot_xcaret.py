# Xcaret
# Nombre de origen azteca que significa "la que escucha"
from ..models import TradingConfig, Broker, ExperimentMessage, get_datetime_now_trade
from .status_bot import get_status_bot
from ..utils.logs import log
from ..experiments import execute_multi_experiment
from ..stop_loss import optimize_stop_loss_simple
from ..models import save_best_model_mlflow
from ..brokers import alpaca_open_long, alpaca_close_long
from ..utils.eval_mlflow_model_strategy import eval_mlflow_model_strategy

class BotXcaret:
    # TODO 

    def __init__(self, trading_config :TradingConfig, debug_mode :bool = False, mlflow_connection=None):
        self.trading_config = trading_config

        #! True: Run only two experiments
        self.debug_mode = debug_mode
        self.mlflow_connection = mlflow_connection
      
        self.min_profit_factor_allowed = 1.2
    

    def get_status(self):

        status_bot  = get_status_bot(
            trading_config=self.trading_config,
            mlflow_connection=self.mlflow_connection
            )
        
        self.status_bot = status_bot
        return status_bot

    
    def run_mlflow_experiments(self):

        start_date_ny, end_date_ny, _ = get_datetime_now_trade()
        print('------------------------------------------------------------')
        print('------------------------------------------------------------')
        print('------------------------------------------------------------')
        print(f"---------STRAT_DATE {start_date_ny} END_DATE: {end_date_ny}")
        print('------------------------------------------------------------')
        print('------------------------------------------------------------')
        print('------------------------------------------------------------')


        experiment_name = f"{self.trading_config.trading.symbol}_{self.trading_config.model.tag}_{self.trading_config.model.version}"
        self.experiment_name = experiment_name

        experiments= ExperimentMessage(
            experiment_name=experiment_name,
            symbol=self.trading_config.trading.symbol,
            start_date=start_date_ny,
            end_date=end_date_ny,
            is_crypto=self.trading_config.trading.is_crypto
        )
        self.experiments = experiments

        best_results, experiments_result = execute_multi_experiment(
            experiment=experiments, 
            debug_mode=self.debug_mode, 
            mlflow_connection=self.mlflow_connection
        )

        self.best_results = best_results
        self.status_bot.experiment_profit_factor = best_results.get('stats_json').get('Profit Factor')
        df_actions = best_results.get('df_actions')


        self.df_actions = df_actions

        self.status_bot.experiment_best_return = best_results.get('best_return')

        if len(df_actions[df_actions['actions'] == 2]) < 2 or  len(df_actions[df_actions['actions'] == 1]) < 2:
            log.info("Best df_actions not have the lot predictions") 
            return float('-inf')


        experiment_return = best_results.get('best_return')
        log.info(f"[EXPERIMENT: {self.experiments.experiment_name}] best_return:  {experiment_return}")
        self.status_bot.experiment_return = experiment_return

        if self.trading_config.calculate_best_stop_loss:
            log.info("Calculate the optimize stop_loss")
            log.info("Start to Calculate The StopLoss")

            best_sl, best_return_sl = optimize_stop_loss_simple(df_actions, st_from=-0.1, st_to=-0.01)
            self.trading_config.trading.stop_loss = best_sl

            self.status_bot.experiment_best_return_stop_loss = best_return_sl
            self.status_bot.experiment_best_stop_loss =  best_sl
            self.status_bot.experiment_profit_factor_sl = best_return_sl
            log.info(f"[EXPERIMENT SL: {self.experiments.experiment_name}] best_return:  {best_return_sl} SL {best_sl}")

            return best_return_sl
        
        return experiment_return
    
    def save_model_mlflow_best(self):

        save_model = False
        if self.trading_config.calculate_best_stop_loss and self.status_bot.experiment_profit_factor_sl > self.min_profit_factor_allowed:
            save_model = True 
            self.best_results['best_return'] = self.status_bot.experiment_profit_factor_sl
        elif not self.trading_config.calculate_best_stop_loss and self.status_bot.experiment_profit_factor > self.min_profit_factor_allowed:
            save_model = True
        
        self.model_name = f"{self.trading_config.trading.symbol}_{self.trading_config.model.tag}"
        if save_model:
            save_best_model_mlflow(
                best_results=self.best_results,
                model_name=self.model_name,
                stage=self.trading_config.model.stage
            )



    def operate(self, force_action :str = None):
        # If not exist order/position run experiments 
        status_bot = self.get_status()

        action = None 
        case = None
        if status_bot.is_registred_model:
            # Get Profit Historical Orders 
            if not status_bot.is_winner:
                best_retrurn = self.run_mlflow_experiments()
                if best_retrurn >= self.min_profit_factor_allowed:
                    log.info("Start Experiment")
                    profit_factor = self.run_mlflow_experiments()
                    if profit_factor > self.min_profit_factor_allowed:
                        log.info("Registring new models")
                        self.save_model_mlflow_best()
                        log.info("Model saved")
            
            log.info("EVAL MODEL")
            action  = eval_mlflow_model_strategy(
                symbol=self.trading_config.trading.symbol, 
                stage=self.trading_config.model.stage, 
                tag=self.trading_config.model.tag, 
                mlflow_connection=self.mlflow_connection, 
                get_action_latest=False
            )

            client_order_id = None
            if action == "open-long" or force_action == "open-long":
                log.info(f"Action: open-long {self.trading_config.trading.symbol}")
                client_order_id = alpaca_open_long(
                                     api_key=self.trading_config.broker.api_key, 
                                     api_secret=self.trading_config.broker.api_secret, 
                                     trading=self.trading_config.trading
                                )
            elif action == "close-long" or force_action == "close-long":
                client_order_id = alpaca_close_long(
                                     api_key=self.trading_config.broker.api_key, 
                                     api_secret=self.trading_config.broker.api_secret, 
                                     symbol=self.trading_config.trading.symbol,
                                     tag=self.trading_config.model.tag
                                )
                
            log.info(f"Action: {action} {self.trading_config.trading.symbol} {client_order_id}")

            case = "case_1"
            
                        
        elif not status_bot.is_registred_model:
            if not status_bot.is_open_order:
                if not status_bot.is_open_positions:
                    profit_factor = self.run_mlflow_experiments()
                    if profit_factor > self.min_profit_factor_allowed:
                        log.info("Registring new models")
                        self.save_model_mlflow_best()
                        log.info("Model saved")

                        if self.trading_config.replicate_latest_open_long_signal:
                            log.info("Replicate latest open-long signal")

                            action  = eval_mlflow_model_strategy(
                                            symbol=self.trading_config.trading.symbol, 
                                            stage=self.trading_config.model.stage, 
                                            tag=self.trading_config.model.tag, 
                                            mlflow_connection=self.mlflow_connection, 
                                            get_action_latest=True
                                        )
                            
                            if action == "open-long" or self.debug_mode==True:
                                 client_order_id = alpaca_open_long(
                                     api_key=self.trading_config.broker.api_key, 
                                     api_secret=self.trading_config.broker.api_secret, 
                                     trading=self.trading_config.trading
                                )
                            case = "case_2"
            

        return action, case
