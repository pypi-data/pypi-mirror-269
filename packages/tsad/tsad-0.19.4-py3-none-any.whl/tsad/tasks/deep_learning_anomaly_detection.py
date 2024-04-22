from ..base.task import Task, TaskResult


import numpy as np
import pandas as pd
import torch
from torch import nn
import matplotlib.pyplot as plt
import pickle
from IPython import display


from .eda import HighLevelDatasetAnalysisResult


class ResidualAnomalyDetectionResult(TaskResult):

    def show(self) -> None:

        pass


class ResidualAnomalyDetectionTask(Task):
    """        
    Pipeline Time Series Anomaly Detection based on 
    SOTA deep learning forecasting algorithms.

    
    This task allows us:\n
     1) forecast time series, including multivariate ones. \n
     2) calculate the residuals between the forecast and real values \n
     3) compare the residuals and, thaks to to it, make the anomaly labelling \n
    """


    def __init__(self,
                 name: str | None = None,
                ):
        super().__init__(name) 


    def _get_anomaly_timestamps(self,dfs):
        """
        Computes the residuals of a deep learning model's predictions on a dataset, and returns them as a pandas DataFrame.
        Helper function to reduce code duplication.

        Parameters:
        ----------
            dfs : tuple of pandas.DataFrame
                A tuple containing four pandas DataFrames: X, X_val, y_true, y_val. 
                Only the first two are used.

        Returns:
        ----------
            df_residuals : pandas.DataFrame
                A pandas DataFrame containing the residuals of the model's predictions on the dataset. 
        """

        X, _, y_true, _ = dfs

        all_data_iterator = self.Loader(X, y_true, self.batch_size, shuffle=False)
        y_pred = self.model.run_epoch( all_data_iterator,     
                                None, None, phase='forecast', points_ahead=self.points_ahead,
                                      device=self.device)
        residuals = self.generate_res_func(y_pred, np.array(y_true))
        point_ahead_for_residuals = 0  # We sometimes forecast 10 points ahead, but we’re still interested in one point forward
        res_indices = [y_true[i].index[point_ahead_for_residuals] for i in range(len(y_true))]
        df_residuals = pd.DataFrame(residuals[:, point_ahead_for_residuals, :], columns=self.columns,
                                    index=res_indices).sort_index()
        return df_residuals


    def fit_predict(self,
            dfs,
            result_base_eda: HighLevelDatasetAnalysisResult,
            model=None,
            optimiser = None,
            criterion = None,
            generate_res_func=None,
            res_analys_alg=None,
            Loader = None,
            points_ahead = 1,
            n_epochs = 5, 
            len_seq = 10, 
            batch_size = 128, 
            encod_decode_model = False, 
            random_state=None,
            shuffle=False,
            show_progress=True,
            show_figures=True,
            best_model_file='./best_model.pt',
            ):
        """
        Fit Anomaly Detection Algorithm based on Deep Learning and residual analysis.

        Parameters
        ----------
        dfs : {{df*,ts*}, list of {df*,ts*}}
            df*,ts* are pd.core.series.Series or pd.core.frame.DataFrame data type.
            Initial data. The data should not contain np.nan at all, but have a constant
            and the same frequency of df.index and at the same time have no gaps. The problem with
            skipping solves splitting one df into list of dff.       

        result_base_eda : HighLevelDatasetAnalysisResult
            Result of HighLevelDatasetAnalysisTask.
        
        model : object of torch.nn.Module class, default=models.SimpleLSTM()
            Used neural network model. 
        
        optimiser : tuple = (torch.optim class ,default = torch.optim.Adam,
            dict  (dict of arguments without params models) , default=default)
            Example of optimiser : optimiser=(torch.optim.Adam,{'lr':0.001})
            Neural network optimization method and its parameters specified in
            documentation to torch.

        criterion : object of torch.nn class, default=nn.MSELoss()
            Error calculation criterion for optimization 

        generate_res_func : function, default=absoluteResidual
            Function for calculating the residuals between the forecast and real values.
        
        res_analys_alg : object of class, default=Hotelling()
            Statistical method for analyzing residuals and detecting anomalies.

        Loader : class, default=ufesul.iterators.Loader.
            The type of loader that will be used as an iterator in the future,
            thanks to which, it is possible to hit the bachi .
            
        batch_size :  int, default=64
            Batch size (Number of samples over which the gradient is averaged)
        
        len_seq : int, default=10
            Window size (number of consecutive points in a row) on which
            the model really works. Essentially an analogue of order in autoregression.
        
        points_ahead : int, default=5
            Horizon forecasting 
        
        n_epochs :  int, default=100 
            Quantity epochs
            
            
        shuffle : bool, default=True
            Whether or not to shuffle the data before splitting. If shuffle=False
        
        show_progress : bool, default=True
            Whether or not to show learning progress with detail by epoch. 

        
        show_figures : bool, default=True
            Show or not show train and validation curve by epoch. 
        
        
        best_model_file : string, './best_model.pt'
            Path to the file where the best model weights will be stored
        


        Returns 
        ----------
        y_pred : torch.tensor
            Tensor of predictions.
        result : DeepLeaningTimeSeriesForecastingResult
            Result of DeepLeaningTimeSeriesForecastingTask.

        """

        
        self.columns = result_base_eda.columns 

        if model is None:
            from ..utils.ml_models.deeplearning_regressors import SimpleLSTM
            model = SimpleLSTM(len(self.columns), len(self.columns), seed=random_state)
        self.model = model
        
        if optimiser is None:
            optimiser = torch.optim.Adam
            optimiser = optimiser(self.model.parameters())
        else:
            args = optimiser[1]
            args['params'] = self.model.parameters()
            optimiser = optimiser[0](**args)
        

        if generate_res_func is None:
            from ..utils.ResidualAnomalyDetectionUtils.generateResidual import absoluteResidual
            self.generate_res_func = absoluteResidual

        if res_analys_alg is None:
            from ..utils.ResidualAnomalyDetectionUtils.stastics import Hotelling
            self.res_analys_alg = Hotelling()

        if Loader is None:
            from ..utils.iterators import Loader
        self.Loader = Loader

        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        if criterion is None:
            criterion = nn.MSELoss()

        self.points_ahead = points_ahead
        self.n_epochs = n_epochs
        self.len_seq = len_seq
        self.batch_size = batch_size
        self.encod_decode_model = encod_decode_model
        self.random_state = random_state
        self.shuffle = shuffle
        self.show_progress = show_progress
        self.show_figures = show_figures
        self.best_model_file = best_model_file
        

        if show_progress:
            show_progress_text = ""

        # -----------------------------------------------------------------------------------------
        #     Формирование train_iterator и val_iteraror
        # -----------------------------------------------------------------------------------------
        X_train, X_test, y_train, y_test = dfs

        train_iterator = self.Loader(X_train, y_train, batch_size, shuffle=shuffle)
        val_iterator = self.Loader(X_test, y_test, batch_size, shuffle=shuffle)

        # -----------------------------------------------------------------------------------------
        #     Обучение моделей
        # -----------------------------------------------------------------------------------------

        



        history_train = []
        history_val = []
        best_val_loss = float('+inf')
        for epoch in range(n_epochs):
            train_loss = self.model.run_epoch(train_iterator, optimiser, criterion, phase='train',
                                              points_ahead=points_ahead, encod_decode_model=self.encod_decode_model,
                                              device=self.device)  # , writer=writer)
            val_loss = self.model.run_epoch(val_iterator, None, criterion, phase='val', points_ahead=points_ahead,
                                            encod_decode_model=self.encod_decode_model,
                                            device=self.device)  # , writer=writer)

            history_train.append(train_loss)
            history_val.append(val_loss)

            if val_loss < best_val_loss:
                best_val_loss = val_loss
                torch.save(self.model.state_dict(), self.best_model_file)

            if show_figures:
                display.clear_output(wait=True)
                plt.figure()
                plt.plot(history_train, label='Train')
                plt.plot(history_val, label='Val')
                plt.xlabel('Epoch')
                plt.ylabel('MSE')
                plt.legend()
                plt.show()

            if show_progress:
                show_progress_text = f'Epoch: {epoch + 1:02} \n' + \
                                     f'\tTrain Loss: {train_loss:.3f} \n' + \
                                     f'\t Val. Loss: {val_loss:.3f} \n\n' +  \
                                     show_progress_text
                print(show_progress_text)




        self.model.load_state_dict(torch.load(self.best_model_file))

        if show_progress:
            print("After choosing the best model:")
            try:
                test_iterator = self.Loader(X_test, y_test, len(X_test), shuffle=False)
                test_loss = self.model.run_epoch(test_iterator, None, criterion, phase='val',
                                                 encod_decode_model=self.encod_decode_model, device=self.device)
                print(f'Test Loss: {test_loss:.3f}')
            except:
                print('Весь X_test не помещается в память, тестим усреднением по батчам')
                test_iterator = self.Loader(X_test, y_test, batch_size, shuffle=False)
                test_loss = []
                for epoch in range(n_epochs):
                    test_loss.append(self.model.run_epoch(test_iterator, None, criterion, phase='val',
                                                          encod_decode_model=self.encod_decode_model, device=self.device))
                print(f'Test Loss: {np.mean(test_loss):.3f}')


        # -----------------------------------------------------------------------------------------
        #     Генерация остатков
        # -----------------------------------------------------------------------------------------
        print('asdasdas',len(dfs))
        df_residuals = self._get_anomaly_timestamps(dfs=dfs)
        self.anomaly_timestamps = self.res_analys_alg.fit_predict(df_residuals, show_figure=show_figures)
        self.statistic = self.res_analys_alg.statistic
        self.ucl = self.res_analys_alg.ucl
        self.lcl = self.res_analys_alg.lcl

        at = pd.Series(self.anomaly_timestamps).to_frame()
        result = ResidualAnomalyDetectionResult()

        return at, result

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # накосячил тут с прогнозом на одну точку вперед. Могут быть проблемы если ahead !=1
    def predict(self,
                dfs,
                result:ResidualAnomalyDetectionResult,
                batch_size = None, 
                show_progress = None, 
                show_figures = None, 
                best_model_file = None,
                 device=None,):

        """Predict by ResidualAnomalyDetectionTask.
        
        Parameters:
        ----------
        dfs : tuple
            Tuple of train and test data.
        result : ResidualAnomalyDetectionResult
            Result of ResidualAnomalyDetectionResult.
        batch_size : int, default=None
            Batch size (Number of samples over which the gradient is averaged)
        device : str, default=None
            Device to use for prediction.


        Returns:
        ----------
        y_pred : torch.tensor
            Tensor of predictions.
        result : ResidualAnomalyDetectionResult
            Result of ResidualAnomalyDetectionResult.
        
        """
        
        self.batch_size = batch_size if batch_size is not None else self.batch_size
        self.device  = device if device is not None else self.device
        self.show_progress = show_progress if show_progress is not None else self.show_progress
        self.show_figures = show_figures if show_figures is not None else self.show_figures
        self.best_model_file = best_model_file if best_model_file is not None else self.best_model_file



        len_seq = self.len_seq
        # -----------------------------------------------------------------------------------------
        #     Генерация остатков
        # -----------------------------------------------------------------------------------------
        df_residuals = self._get_anomaly_timestamps(dfs=dfs)
        self.anomaly_timestamps = self.res_analys_alg.predict(df_residuals, show_figure=self.show_progress)
        self.statistic = self.res_analys_alg.statistic

        
        at = pd.Series(self.anomaly_timestamps).to_frame()
        result = ResidualAnomalyDetectionResult()

        return at, result


    # def save(self, path='./pipeline.pcl'):
    #     """
    #     Method for saving pipeline.
    #     It may be required for example after training.
    #     CPU.
        
    #     Parameters
    #     ----------
    #         path : str
    #     Путь до файла, для сохранения пайплайна. 
    #     Пайлайн сохраняется в формате pickle
    #     """

    #     self.model.run_epoch(self.Loader(torch.zeros((1, self.len_seq, self.model.in_features), dtype=float),
    #                                     torch.zeros((1, self.len_seq, self.model.in_features), dtype=float),
    #                                     batch_size=1),
    #                          None, None, phase='forecast', points_ahead=1, device=self.device)
    #     with open(path, 'wb') as f:
    #         pickle.dump(self, f)

    # def load(self, path='./pipeline.pcl'):
    #     """
    #     Method for loading pipeline.
    #     It may be required for example after training.
        
    #     Parameters
    #     ----------
    #         path : str
    #     Путь до сохраненного файла пайплайна. 
    #     Пайлайн должен быть в формате pickle
    #     """
    #     with open(path, 'rb') as f:
    #         pipeline = pickle.load(f)
    #     self.__dict__.update(pipeline.__dict__)
