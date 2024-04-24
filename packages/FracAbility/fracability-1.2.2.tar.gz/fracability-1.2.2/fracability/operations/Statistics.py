import numpy as np

from numpy import exp
import pandas as pd
from pandas import DataFrame
import scipy.stats as ss
from scipy.optimize import minimize
import ast

from fracability.utils.general_use import KM


class NetworkData:

    """ Class used to represent fracture or fracture network data.
    It acts as a wrapper for the scipy CensoredData class
    """

    def __init__(self, obj=None, use_survival=True, complete_only=True):
        """

        :param obj: fracture/fracture network object
        :param use_survival: Use survival analysis to get the distribution. If false the whole dataset is used considering all fractures complete
        :param complete_only: When not using survival, use only the complete length values
        """

        self._obj = obj  # fracture/fracture network object

        self._data = None  # the data
        self._lengths: np.ndarray  # array of all the lengths (both complete and censored)
        self._non_censored_lengths: np.ndarray  # array of only complete lengths
        self._censored_lengths: np.ndarray  # array of only censored lengths

        self._function_list: list = ['pdf', 'cdf', 'sf', 'hf', 'chf']  # list of possible functions

        self.use_survival = use_survival
        self.complete_only = complete_only

        if obj is not None:
            if self._obj.name == 'FractureNetwork':
                frac_obj = self._obj.fractures
            else:
                frac_obj = self._obj

            entity_df = frac_obj.entity_df
            entity_df = entity_df.sort_values(by='length')

            self.delta = 1-entity_df['censored'].values
            self._lengths = entity_df['length'].values
            self._non_censored_lengths = entity_df.loc[entity_df['censored'] == 0, 'length'].values
            self._censored_lengths = entity_df.loc[entity_df['censored'] == 1, 'length'].values

            if self.use_survival:
                self.data = ss.CensoredData(uncensored=self._non_censored_lengths, right=self._censored_lengths)
            else:
                if self.complete_only:
                    self.data = self.non_censored_lengths
                else:
                    self.data = self.lengths

    @property
    def data(self):
        """
        Property that returns or sets the CensoredData class of the fracture network
        :return:
        """
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def lengths(self) -> np.ndarray:

        """
        This property returns or sets the complete list of length data (censored and uncesored) for the fracture network

        :getter: Return the complete list of lengths
        :setter: Set the complete list of lengths
        """

        return self._lengths

    @property
    def non_censored_lengths(self) -> np.ndarray:

        """
        This property returns or sets the list of non-censored length data of the fracture network

        :getter: Return the list of non-censored data
        :setter: Set the list of non-censored data
        """

        return self._non_censored_lengths

    @property
    def censored_lengths(self) -> np.ndarray:

        """
        This property returns or sets the list of censored length data of the fracture network

        :getter: Return the list of censored data
        :setter: Set the list of censored data
        :return:
        """

        return self._censored_lengths

    @property
    def function_list(self) -> list:
        """
        Property that returns the list of available probability functions (pdf, cdf etc)
        :return:
        """
        return self._function_list

    @property
    def mean(self) -> np.ndarray:
        return np.mean(self.lengths)

    @property
    def std(self) -> np.ndarray:
        return np.std(self.lengths)

    @property
    def var(self) -> np.ndarray:
        return np.var(self.lengths)

    @property
    def median(self) -> np.ndarray:
        return np.median(self.lengths)

    @property
    def mode(self) -> tuple:
        return ss.mode(self.lengths)

    @property
    def b5(self) -> np.ndarray:
        return np.percentile(self.lengths, 5)

    @property
    def b95(self) -> np.ndarray:
        return np.percentile(self.lengths, 95)

    @property
    def ecdf(self) -> np.ndarray:
        """
        Property that returns the empirical cdf of the data using Kaplan-Meier
        :return:
        """
        return KM(self.lengths, self.lengths, self.delta)

    @property
    def esf(self) -> np.ndarray:
        """
        Property that returns the empirical sf of the data
        :return:
        """
        return 1-self.ecdf

    @property
    def total_n_fractures(self) -> int:
        return len(self.lengths)

    @property
    def censoring_percentage(self) -> float:
        return (len(self.censored_lengths)/self.total_n_fractures)*100


class NetworkDistribution:
    """
    Class used to represent a fracture or fracture network length distribution. It is essentially a wrapper for the
    scipy rv distributions.
    """

    def __init__(self, obj: ss.rv_continuous = None, parameters: tuple = None, fit_data: NetworkData = None):

        self._distribution = obj.freeze(*parameters)
        self.fit_data = fit_data

    @property
    def distribution(self) -> ss.rv_continuous:
        """
        Property that returns or sets a *frozen* ss.rv_continuous class
        :return:
        """
        return self._distribution

    @distribution.setter
    def distribution(self, distribution: ss.rv_continuous = None):
        self._distribution = distribution

    @property
    def distribution_name(self) -> str:
        """
        Property that returns the name of the given distribution
        :return:
        """
        return self.distribution.dist.name

    @property
    def distribution_parameters(self) -> tuple:
        """
        Property that returns the parameters of the frozen distribution
        :return:
        """
        return self.distribution.args

    @property
    def n_distribution_parameters(self) -> int:
        """
        Property that returns the number of parameters of the frozen distribution. the args method returns the
        shape parameters. This means that except for normal and logistic the loc counts as a parameter. To fix this we
        subtract -1 to all except normal and logistic.
        :return:
        """
        if self.distribution_name == 'norm' or self.distribution_name == 'logistic':

            return len(self.distribution_parameters)
        else:
            return len(self.distribution_parameters)-1

    @property
    def mean(self) -> float:
        """
        Property that returns the mean of the frozen distribution
        :return:
        """
        return self.distribution.mean()

    @property
    def mode(self) -> list:
        """
        Property that returns the mode(s) of the pdf of the given distribution
        :return:
        """
        return minimize(lambda x: -self.distribution.pdf(x), np.ceil(self.distribution_parameters[-1])).x

    @property
    def median(self) -> float:
        """
        Property that returns the median of the distribution
        :return:
        """
        return self.distribution.median()

    @property
    def var(self) -> float:
        """
        Property that returns the variance of the distribution
        :return:
        """
        return self.distribution.var()

    @property
    def std(self) -> float:
        """
        Property that returns the standard deviation of the distribution
        :return:
        """
        return self.distribution.std()

    @property
    def b5(self) -> float:
        """
        Property that returns the 5th percentile of the distribution
        :return:
        """
        return self.distribution.ppf(0.05)

    @property
    def b95(self) -> float:
        """
        Property that returns the 95th percentile of the distribution
        :return:
        """
        return self.distribution.ppf(0.95)

    @property
    def max_log_likelihood(self) -> float:
        """
        Property that returns the log likelihood of the distribution. The likelihood is calculated by adding
        the cumulative sum of the log pdf and log sf of the fitted distribution.
        :return:
        """
        if self.fit_data.use_survival:
            log_f = self.log_pdf(self.fit_data.non_censored_lengths)
            print(len(self.fit_data.non_censored_lengths))
            log_r = self.log_sf(self.fit_data.censored_lengths)
        else:
            if self.fit_data.complete_only:
                sample = self.fit_data.non_censored_lengths
            else:
                sample = self.fit_data.lengths
            log_f = self.log_pdf(sample)
            log_r = np.array([0])

        LL_f = log_f.sum()
        LL_rc = log_r.sum()

        return LL_f + LL_rc


    @property
    def AIC(self) -> float:
        """
        Property that returns the classic Akaike Information Criterion (1974) of the distribution
        :return:
        """
        max_log_likelihood = self.max_log_likelihood

        k = self.n_distribution_parameters

        AIC = (-2 * max_log_likelihood) + (2 * k)

        return AIC

    @property
    def AICc(self) -> float:
        """
        Property that returns the Akaike Information Criterion (for small number of values) of the distribution
        :return:
        """

        LL2 = -2 * self.max_log_likelihood

        k = self.n_distribution_parameters
        n = self.fit_data.total_n_fractures

        if (n - k - 1) == 0: # if n parameters + 1 = n of total fractures then the akaike is invalid i.e. the total fractures must be > than the n_parameters+1
            return -1
        else:
            AICc = 2 * k + LL2 + (2 * k ** 2 + 2 * k) / (n - k - 1)
            return AICc

    @property
    def BIC(self) -> float:
        """
        Property that returns the Bayesian Information Criterion of the distribution
        :return:
        """
        LL2 = -2 * self.max_log_likelihood

        k = len(self.distribution_parameters)
        n = len(self.fit_data.non_censored_lengths) + len(self.fit_data.censored_lengths)

        BIC = np.log(n)*k + LL2
        return BIC

    def log_pdf(self, x_values: np.array = None) -> np.array:
        """
        Property that returns the logpdf calculated on the data
        :return:
        """

        if x_values.any():
            return self.distribution.logpdf(x_values)
        else:
            return np.array([0])

    def log_sf(self, x_values: np.array = None) -> np.array:
        """
        Property that returns the logsf calculated on the data
        :return:
        """
        if x_values.any():
            return self.distribution.logsf(x_values)
        else:
            return np.array([0])

    def cdf(self, x_values: np.array = None):
        if x_values:
            return self.distribution.cdf(x_values)
        else:
            return self.distribution.cdf(self.fit_data.lengths)


class NetworkFitter:

    """
    Class used to fit a Fracture or Fracture network object

    Add bool to:
        + Consider censored lengths as non-censored
        + Do not consider censored lengths at all

    """
    def __init__(self, obj=None, use_survival=True, complete_only=True, use_AIC=True):
        """

        :param obj: fracture/fracture network object
        :param use_survival: Bool flag to set to use survival analysis approach or not. Default is True
        :param complete_only: Bool flag to set to use only complete values. Default is False
        :param use_AIC: Bool flag to set to use AIC or AICc. If True use AIC if False AICc. Default is True. The
        column name in the dataframe will remain the same (Akaike).
        """

        self._net_data: NetworkData
        self._accepted_fit: list = []
        self._rejected_fit: list = []
        self._AIC_flag: bool = use_AIC
        self._fit_dataframe: DataFrame = DataFrame(columns=['name', 'Akaike', 'delta_i', 'w_i',
                                                            'max_log_likelihood', 'distribution', 'params'])

        self.net_data = NetworkData(obj, use_survival, complete_only)

    @property
    def net_data(self) -> NetworkData:
        """
        Property that returns or sets a NetworkData object
        :return:
        """
        return self._net_data

    @property
    def fit_records(self) -> DataFrame:

        """ Return the sorted fit dataframe"""

        return self._fit_dataframe.sort_values(by='Akaike', ignore_index=True)

    @net_data.setter
    def net_data(self, data: NetworkData):
        self._net_data = data

    def fit(self, distribution_name: str):

        """
        Fit the data of the entity_df using scipy available distributions
        :param distribution_name: Name of the distribution to fit
        :return:
        """

        distribution = getattr(ss, distribution_name)

        if distribution_name == 'norm' or distribution_name == 'logistic':
            params = distribution.fit(self.net_data.data)
        else:
            params = distribution.fit(self.net_data.data, floc=0)

        distribution = NetworkDistribution(distribution, params, self.net_data)

        if self._AIC_flag:
            akaike = distribution.AIC
        else:
            akaike = distribution.AICc
        log_likelihood = distribution.max_log_likelihood

        self._fit_dataframe.loc[len(self._fit_dataframe)] = [distribution_name,
                                                             akaike, 0.0, 0.0,
                                                             log_likelihood, distribution, str(params)]

        for i, AIC_val in enumerate(self._fit_dataframe['Akaike']):
            d_i = AIC_val - min(self._fit_dataframe['Akaike'])
            self._fit_dataframe.loc[i, 'delta_i'] = d_i

        total = exp(-self._fit_dataframe['delta_i'].values/2).sum()

        for d, delta_i in enumerate(self._fit_dataframe['delta_i']):
            w_i = np.round(exp(-delta_i/2)/total, 5)
            self._fit_dataframe.loc[d, 'w_i'] = w_i

    def get_fitted_parameters(self, distribution_name: str) -> tuple:
        """
        Get the fitted distributions parameters in the fit records df
        :param distribution_name: Name of the distribution
        """
        parameters = self.fit_records.loc[self.fit_records['name'] == distribution_name, 'params'].values[0]
        return ast.literal_eval(parameters)

    def get_fitted_distribution(self, distribution_name: str) -> NetworkDistribution:

        """
        get the fitted NetworkDistribution object
        :param distribution_name: name of the distribution
        :return:
        """

        distribution = self.fit_records.loc[self.fit_records['name'] == distribution_name, 'distribution'].values[0]

        return distribution

    def get_fitted_distribution_names(self) -> list:

        """
        get the names of the fitted NetworkDistribution object
        :param distribution_name: name of the distribution
        :return:
        """

        return self.fit_records['name'].values

    def get_fitted_parameters_list(self, distribution_names: list = None) -> list:

        """
        Get the parameters of the computed fit(s)
        :return: Pandas DataFrame
        """
        if distribution_names is None:
            distribution_names = self.fit_records['name'].tolist()

        parameter_list = []

        for name in distribution_names:
            parameters = self.fit_records.loc[self.fit_records['name'] == name, 'params'].values[0]
            parameter_list.append(ast.literal_eval(parameters))

        return parameter_list

    def get_fitted_distribution_list(self, distribution_names: list = None) -> list:
        """
        Get a list of NetworkDistribution objects  fot the given distribution name
        :param distribution_names:
        :return:
        """

        if distribution_names is None:
            distribution_names = self.fit_records['name'].tolist()

        distribution_list = []

        for name in distribution_names:
            distribution = self.fit_records.loc[self.fit_records['name'] == name, 'distribution'].values[0]
            distribution_list.append(distribution)

        return distribution_list

    def best_fit(self) -> pd.Series:

        """
        Return the best fit in the fit records dataframe
        :return:
        """

        df = self.fit_records

        return df.loc[0]

    def rejected_fit(self) -> pd.DataFrame:

        """
        Return the fit records dataframe without the best fit
        :return:
        """

        df = self.fit_records

        return df.loc[1:]

    def find_best_distribution(self, distribution_list: list = None) -> pd.Series:
        """
        Method used to find the best distribution using BIC ranking
        :param distribution_list: list of distribution to test
        :return:
        """

        if distribution_list is None:

            distribution_list = ['lognorm',
                                 'norm',
                                 'expon',
                                 'burr12',
                                 'gamma',
                                 'logistic']

        for distribution in distribution_list:
            self.fit(distribution)

        return self.best_fit()

        # fig1 = plt.figure(num='CDF plots', figsize=(13, 7))
        # fig2 = plt.figure(num='Histograms', figsize=(13, 7))
        # for i in sorted.index:
        #
        #     distr = sorted.loc[i, 'distr']
        #     params = ast.literal_eval(sorted.loc[i, 'params'])
        #     fitter_name = sorted.loc[i, 'name']
        #     aicc = sorted.loc[i, 'AICc']
        #
        #     cdf = distr.cdf(ecdf.quantiles, *params)
        #     pdf = distr.pdf(ecdf.quantiles, *params)
        #
        #     plt.figure(num='CDF plots')
        #     plt.tight_layout()
        #     plt.subplot(2, 3, i + 1)
        #     # if i//3 < 1:
        #     #     plt.tick_params(labelbottom=False)
        #     # if i%3 > 0:
        #     #     plt.tick_params(labelleft=False)
        #     plt.title(f'{fitter_name}   AICc: {np.round(aicc, 3)}')
        #     plt.plot(ecdf.quantiles, ecdf.probabilities, 'b-', label='Empirical CDF')
        #     plt.plot(ecdf.quantiles, cdf, 'r-', label=f'{fitter_name} CDF')
        #     plt.legend()
        #
        #     plt.figure('Histograms')
        #     plt.subplot(2, 3, i + 1)
        #     plt.title(f'{fitter_name}   AICc: {np.round(aicc, 3)}')
        #     sns.histplot(lengths, stat='density', bins=50)
        #     sns.lineplot(x=ecdf.quantiles, y=pdf, label=f'{fitter_name} PDF', color='r')
        #     plt.legend()
        #
        # plt.show()


    # def summary_plot(self, x_min: float = 0.0, x_max: float = None, res: int = 200):
        #
        #     """
        #     Summarize PDF, CDF and SF functions and display mean, std, var, median, mode, 5th and 95th percentile all
        #     in a single plot.
        #     A range of values and the resolution can be defined with the x_min, x_max and res parameters.
        #
        #     Parameters
        #     -------
        #     x_min: Lower value of the range. By default is set to 0
        #
        #     x_max: Higher value of the range. If None the maximum length of the dataset is used. None by default
        #
        #     res: Point resolution between x_min and x_max. By default is set to 1000
        #     """
        #
        #     if x_max is None:
        #         x_max = max(self._obj.entity_df['length'])
        #
        #     x_vals = np.linspace(x_min, x_max, res)
        #
        #     fig = plt.figure(num='Summary plot', figsize=(13, 7))
        #     fig.text(0.5, 0.02, 'Length [m]', ha='center')
        #     fig.text(0.5, 0.95, self.dist.name2, ha='center')
        #     fig.text(0.04, 0.5, 'Density', va='center', rotation='vertical')
        #
        #     for i, name in enumerate(self._function_list[:3]):
        #         func = getattr(self.dist, name)
        #
        #         y_vals = func(xvals=x_vals, show_plot=False)
        #         plt.subplot(2, 2, i+1)
        #         plt.plot(x_vals, y_vals)
        #         if name == 'CDF':
        #             xvals, ecdf = statistics.ecdf(self.non_censored_lengths, self.censored_lengths)
        #             plt.step(xvals, ecdf, 'r-')
        #         plt.title(name)
        #         plt.grid(True)
        #
        #     plt.subplot(2, 2, i+2)
        #     plt.axis("off")
        #     plt.ylim([0, 8])
        #     plt.xlim([0, 10])
        #     dec = 4
        #
        #     text_mean = f'Mean = {round_and_string(self.dist.mean, dec)}'
        #     text_std = f'Std = {round_and_string(self.dist.standard_deviation, dec)}'
        #     text_var = f'Var = {round_and_string(self.dist.variance, dec)}'
        #     text_median = f'Median = {round_and_string(self.dist.median, dec)}'
        #     text_mode = f'Mode = {round_and_string(self.dist.mode, dec)}'
        #     text_b5 = f'5th Percentile = {round_and_string(self.dist.b5, dec)}'
        #     text_b95 = f'95th Percentile = {round_and_string(self.dist.b95, dec)}'
        #
        #     plt.text(0, 7.5, 'Summary table')
        #     plt.text(0, 6.5, text_mean)
        #     plt.text(0, 5.5, text_median)
        #     plt.text(0, 4.5, text_mode)
        #     plt.text(0, 3.5, text_b5)
        #     plt.text(0, 2.5, text_b95)
        #     plt.text(0, 1.5, text_std)
        #     plt.text(0, 0.5, text_var)
        #
        #     plt.text(6, 7.5, 'Test results:')
        #
        #     if self.test_parameters:
        #
        #         text_result = self.test_parameters['Result']
        #         text_crit_val = f'KS critical value = {round_and_string(self.test_parameters["crit_val"])}'
        #         text_ks_val = f'KS statistic = {round_and_string(self.test_parameters["KS_stat"])}'
        #
        #         plt.text(8.5, 7.5, text_result)
        #         plt.text(6, 6.5, text_crit_val)
        #         plt.text(6, 5.5, text_ks_val)
        #
        #     else:
        #         plt.text(6, 6.5, 'No test has been executed')
        #
        #     plt.show()

    # def plot_function(self,
    #                   func_name: str,
    #                   x_min: float = 0.0,
    #                   x_max: float = None,
    #                   res: int = 200):
    #
    #     """
    #     Plot PDF, CDF or SF functions in a range of x values and with a given resolution.
    #
    #     Parameters
    #     -------
    #     func_name: Name of the function to plot. Use the fitter_list method to display the available methods.
    #
    #     x_min: Lower value of the range. By default it is set to 0
    #
    #     x_max: Higher value of the range. If None the maximum length of the dataset is used. None by default
    #
    #     res: Point resolution between x_min and x_max. By default is set to 1000
    #
    #     Notes
    #     -------
    #     Each plot is created in a separate figure with the name associated to the given funtion
    #     """
    #
    #     if x_max is None:
    #         x_max = self._lengths.max()*10
    #
    #     x_vals = np.linspace(x_min, x_max, res)
    #
    #     func = getattr(self.dist, func_name) # get the specific function (PDF, CDF, SF)
    #     y_vals = func(xvals=x_vals, show_plot=False)
    #
    #
    #     fig = plt.figure(num=func_name)
    #     plt.plot(x_vals, y_vals, 'b-', label='Theoretical cdf')
    #
    #     if func_name == 'CDF':
    #         xval, ecdf = statistics.ecdf(self.non_censored_lengths,self.censored_lengths)
    #         plt.step(xval, ecdf, 'r-', label='Empirical cdf')
    #     plt.title(func_name)
    #     plt.xlabel('Length [m]')
    #     plt.ylabel('Function response')
    #     plt.grid(True)
    #     plt.legend()
    #     plt.show()

    # def plot_kde(self, n_bins: int = 25, x_min: float = 0.0, x_max: float = None, res: int = 1000):
    #
    #     """
    #     Plot the Kernel Density Estimation PDF function togather with the data histogram
    #
    #     Parameters
    #     -------
    #     n_bins: Number of histogram bins
    #
    #     x_min: Lower value of the range. By default is set to 0
    #
    #     x_max: Higher value of the range. If None the maximum length of the dataset is used. None by default
    #
    #     res: Point resolution between x_min and x_max. By default is set to 1000
    #
    #     """
    #
    #     data = self._lengths
    #
    #     if x_max is None:
    #         x_max = self._lengths.max()
    #
    #     x_vals = np.linspace(x_min, x_max, res)
    #
    #     pdf_kde = gaussian_kde(data).evaluate(x_vals)
    #
    #     fig = plt.figure(num='Gaussian KDE estimation')
    #     plt.hist(data, density=True, bins=15,label='Data')
    #     plt.plot(x_vals, pdf_kde, label='Gaussian KDE')
    #
    #     plt.title('Gaussian KDE estimation')
    #     plt.xlabel('Length [m]')
    #     plt.ylabel('Function response')
    #     plt.grid(True)
    #     plt.show()