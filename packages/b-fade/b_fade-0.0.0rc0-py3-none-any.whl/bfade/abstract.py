from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Any

import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.stats import norm, multivariate_normal
from scipy.optimize import minimize_scalar, minimize
from numdifftools import Hessian

from bfade.util import grid_factory, logger_factory
from bfade.util import identity, printer, dummy_translator
from bfade.statistics import Distribution, uniform

_log = logger_factory(name=__name__, level="DEBUG")

MINIMZER_LO_BOUND = 0
MINIMZER_UP_BOUND = 1e20

class AbstractCurve(ABC):
    """Abstract curve to instantiate curves to perform MAP over.

    Contains:

        - representation

        - inspection

        - computation of its distance to a given dataset.

    """

    def __init__(self, metrics: callable = identity, **pars: Dict[str, Any]) -> None:
        """
        Initialise curve.
        
        Parameters
        ----------
        metrics : callable
            identity, logarithm, for instance. Default is identity. This determines\
            whether minimum distance points are sought over the lin-lin or log-log space.
            
        pars: Dict[str, Any]
            name : Dict[str, str]
                name of the instance.
            remainder of arguments : Dict[str, float]
                parameters of the curve
        Returns
        -------
        None

        """
        try:
            self.name = pars.pop("name")
        except KeyError:
            self.name = "Untitled"
            
        try:
            self.metrics = pars.pop("metrics")
        except KeyError:
            self.metrics = identity
        
        [setattr(self, p, pars[p]) for p in pars]
        self.pars = [k for k in pars.keys()]
        self.metrics = metrics
        self.config()

    def config(self, save: bool = False, folder: str = "./", fmt: str = "png", dpi: int = 300) -> None:
        """
        Configure settings for saving plots.

        Parameters
        ----------
        save : bool, optional
            Flag indicating whether to save plots. The default is False.
        folder : str, optional
            Folder path where plots will be saved. The default is "./".
        fmt : str, optional
            Format for saving plots. The default is "png".
        dpi : int, optional
            Dots per inch for saving plots. The default is 300.

        Returns
        -------
        None

        """
        self.save = save
        self.folder = folder
        self.fmt = fmt
        self.dpi = dpi

    @abstractmethod
    def equation(self) -> np.ndarray:
        """
        Abstract representation of a mathematical equation.
        """
        ...

    def squared_distance(self, t: float, X: np.ndarray) -> float:
        """
        Calculate the squared distance between two points over the feature plane.

        This is just an auxiliary function, which ought not to be used directly,
        rather it must be used in conjunction with signed_distance_to_dataset.

        .. math::
            d^2 = (\mathcal{M}(x1) - \mathcal{M}(t))^2 + (\mathcal{M}(x2) - \mathcal{M}(f(t)))^2

        where :math:`\mathcal{M}` is the metrics whereby the optimal distance will
        be computed.
        
        Parameters
        ----------
        t : float
            Dummy parameter. Abscissa along the equation.
        X : np.ndarray
            An array representing a point belonging to the feature space [X[0], X[1]].
        
        Returns
        -------
        float
            The squared distance between the metric values of points [t, equation(t)] and X.

        """
        return (self.metrics(X[0]) - self.metrics(t))**2 +\
               (self.metrics(X[1]) - self.metrics(self.equation(t)))**2
    
    def signed_distance_to_dataset(self, D) -> Tuple[np.ndarray]:
        """
        Minimises squared_distance to compute the minimum squared distance of
        each point of the dataset to the target curve.

        .. math::

            \min_{\\theta} d^2

        where :math:`\\theta` gather the parameters of the target curve.

        D : Dataset
            Dataset instance containing attributes X and y as features and output, respectively.

        """
        x_opt = []
        y_opt = []        
        l_dis = []
        dd = []
        signa = []
        
        for x in D.X:
            res = minimize_scalar(self.squared_distance, args=(x),
                                  method="bounded",
                                  bounds=(MINIMZER_LO_BOUND, MINIMZER_UP_BOUND),
                                  )
            
            if res.success:
                x_opt.append(res.x)
                l_dis.append(res.fun)
            # else:
            #     raise Exception("Error while minimising.")
        
        x_opt = np.array(x_opt)
        y_opt = self.equation(x_opt)
        
        for x, xo, yo in zip(D.X, x_opt, y_opt):
            d = np.array([x[0]-xo, x[1]-yo]).T
            dd.append(np.inner(d, d)**0.5)
            
            if x[1] > yo:
                signa.append(1)
            else:
                signa.append(-1)
        
        l_dis = np.array(l_dis)
        dd = np.array(dd)
        signa = np.array(signa)
        
        return dd*signa, x_opt, y_opt

    @printer
    def inspect(self, x: np.ndarray, scale: str = "linear", **data: Dict[str, Any]) -> None:
        """
        Plot the equation of the curve and optionally the provided dataset.

        Parameters
        ----------
        x : np.ndarray
            Array of x-values for plotting the equation curve.
        scale : str, optional
            The scale of the plot. The default is "linear".
        data : Dict[str, Any]
            Additional data for scatter points. Expected keys: "X", "y".

        Returns
        -------
        None
        """
        _log.warning(f"{self.__class__.__name__}.{self.inspect.__name__}")
        fig, ax = plt.subplots(dpi=300)
        plt.plot(x, self.equation(x), "k")

        try:
            plt.scatter(data["X"][:,0], data["X"][:,1], c=data["y"], s=10)
        except:
            pass
        plt.title(f"{self.__class__.__name__} -- {self.pars} = {[getattr(self, p) for p in self.pars]}")
        plt.xscale(scale)
        plt.yscale(scale)
        return fig, self.name + "_curve"

    @printer  
    def inspect_signed_distance(self, x: np.ndarray, x_opt: np.ndarray, y_opt: np.ndarray, dis: np.ndarray,
                                X: np.ndarray = None, y: np.ndarray = None, scale: str = "linear") -> None:
        """
        Visualize the signed distance of data points to a minimum-distance
        (optimal) point along the curve.

        Parameters
        ----------
        x : np.ndarray
            Input values for the optimal point.
        x_opt : np.ndarray
            x-coordinate of the optimal point.
        y_opt : np.ndarray
            y-coordinate of the optimal point.
        dis : np.ndarray
            Signed distance values for each data point.
        X : np.ndarray, optional
            Input features of the synthetic dataset.
        y : np.ndarray, optional
            Target values of the synthetic dataset.
        scale : str, optional
            Scale for both x and y axes. Options are "linear" (default) or "log".

        Returns
        -------
        None
            Displays a plot visualizing the signed distance of data points to the optimal point.

        """
        fig, ax = plt.subplots(dpi=300)
        
        if X is not None:
            plt.scatter(X[:,0], X[:,1], c=y)
        
        plt.scatter(x_opt, y_opt)
        
        for x, xo, yo, d in zip(X, x_opt, y_opt, dis):
            if d > 0:
                ax.plot([x[0], xo], [x[1], yo], '-b')
            else:
                ax.plot([x[0], xo], [x[1], yo], '-.r')
                
        ax.axis("equal")
        plt.xscale(scale)
        plt.yscale(scale)
        return fig, self.name + "_sig_dist"
        
    def get_curve(self) -> Tuple:
        """
        Get curve parameters and its equation

        Returns
        -------
        Tuple

        """
        return self.pars, self.equation

    def __repr__(self):
        attributes_str = ',\n '.join(f'{key} = {value}' for key, value in vars(self).items())
        return f"{self.__class__.__name__}({attributes_str})"


class AbstractBayes(ABC):
    """Bayesian framework to perform Maximum a Posterior Estimation and predictions.
    
    Contains:

        - core method to perform map

        - abstract predictor

        - methods to instantiate priors, log-likelihood, and log-posterior

        - Variational (Laplace) approximation of the posterior

        - computation of the predictive posterior.

    """
    
    def __init__(self, *pars: List[str], **args: Dict[str, Any]) -> None:
        """
        Initialize the instance.
        
        Parameters
        ----------
        pars : List[str]
            List of the names of the trainable parameters.

        args: Dict[str, Any]

            - theta_hat : np.ndarray
                expected value of the parameter (if available).

            - ihess : np.ndarray
                Inverse Hessian matrix of the log-posterior (if available).

            - name : str
                Name of the instance.

            - other parameters : float
                Deterministic parameters, if any.
        
        Returns
        -------
        None

        """
        try:
            self.name = args.pop("name")
        except:
            self.name = "Untitled"
        
        self.pars = pars
        [setattr(self, "prior_" + p, Distribution(uniform, unif_value=1)) for p in self.pars]
        _log.debug(f"{self.__class__.__name__}.{self.__init__.__name__} -- {self}")
        
        try:
            self.theta_hat = args.pop("theta_hat")
            self.ihess = args.pop("ihess")
            self.laplace_posterior()
            _log.warning(f"{self.__class__.__name__}.{self.MAP.__name__}"+\
                          f" -- Optimal values known -- theta_hat = {self.theta_hat}" +\
                          f"ihess = {self.ihess}")
        except:
            self.theta_hat = None
            self.ihess = None
            _log.warning(f"{self.__class__.__name__}.{self.MAP.__name__} -- Optimal values unknown. Must run MAP.")
        
        try:
            self.deterministic = args
            _log.info(f"{self.__class__.__name__}.{self.__init__.__name__} -- Deterministic parameter(s) {self.deterministic}")
        except KeyError:
            self.deterministic = None
            _log.info(f"{self.__class__.__name__}.{self.__init__.__name__} -- No deterministic parameter(s)")

    def load_prior(self, par: str, dist: callable, **args: Dict) -> None:
        """
        Load a prior distribution for a specified parameter.
    
        Parameters
        ----------
        par : str
            The name of the parameter.
        dist : callable
            The distribution function or class.
        args : Dict[str]
            Additional arguments to be passed to the distribution function.
    
        Returns
        -------
        None

        """
        _log.info(f"{self.__class__.__name__}.{self.load_prior.__name__} for {par}")
        setattr(self, "prior_" + par, Distribution(dist, **args))
        
    def load_log_likelihood(self, log_loss_fn: callable, **args: Dict[str, Any]) -> None:
        """
        Load a likelihood loss function.

        Parameters
        ----------
        log_loss_fn : callable
            Log-likelihood function.
        args : Dict[str, Any]
            Arguments of the log-likelihood function.

        Returns
        -------
        None

        """
        _log.info(f"{self.__class__.__name__}.{self.load_log_likelihood.__name__} -- {log_loss_fn}")
        self.log_likelihood_args = args
        self.log_likelihood_loss = log_loss_fn
    
    @abstractmethod
    def predictor(self, D, *P: Dict[str, float]) -> None:
        """
        Abstract method for making predictions using a model.
         
        Parameters
        ----------
        D : Dataset
            Training dataset.
        P : Dict[str, float]
            Value of the parameters of the target curve.
         
        Returns
        -------
        np.ndarray
            The result of the prediction.
    
        """
        ...

    def predict(self, D) -> np.ndarray:
        """
        Wraps predictor to predict via the trained model.

        Parameters
        ----------
        D : Dataset
            Data for prediction.

        Returns
        -------
        np.ndarray
            Predictions.

        Raises
        ------
        TypeError
            If the optimal value is not available. Must run MAP.
        """
        try:
            return self.predictor(D, *self.theta_hat)
        except (AttributeError, TypeError):
            raise TypeError("Optimal value not available. Must run MAP.")
    
    def log_prior(self, *P: Dict[str, Any]) -> float:
        """
        Calculate the log-prior probability hypothesising initially independent distributions.

        .. math::

            \log P[\\theta] = \sum \log P[\\theta_i]

        Parameters
        ----------
        P : Dict[str, Any]
            Distribution and related arguments to be prescribed over the parameter.
    
        Returns
        -------
        float
            The log-prior probability.

        """
        return np.array([getattr(self, "prior_" + p).logpdf(P[(self.pars.index(p))]) for p in self.pars]).sum()
    
    def log_likelihood(self, D, *P: Dict[str, Any]) -> float:
        """
        Calculate the log-likelihood.

        .. math::

            \log P[D | \\theta]
    
        Parameters
        ----------
        D : Dataset
            Input dataset.
        P : Dict[str, float]
            Value of trainable parameters for the target curve.
    
        Returns
        -------
        float
            The log-posterior probability.

        """
        return -self.log_likelihood_loss(D.y, self.predictor(D, *P), **self.log_likelihood_args)
    
    def log_posterior(self, D, *P: Dict[str, Any]) -> float:
        """
        Calculate the log-posterior.

        .. math::

            \log P[\\theta] = \log P[D | \\theta] + \log P[\\theta]
    
        Parameters
        ----------
        D : Dataset
            Input dataset.
        P : Dict[str, Any]
            Trainable parameters.
    
        Returns
        -------
        float
            The log-posterior probability.

        """
        return self.log_prior(*P) + self.log_likelihood(D, *P)
    
    def MAP(self, D, x0=[1,1], solver: Dict[str, Any] = None) -> None:
        """
        Find the Maximum A Posteriori (MAP) estimate for the parameters.

        .. math::

            \min_{\\theta} -\log P[\\theta | D]

        If MAP succeeds, the optimal parameters are stored in theta_hat. Whilst
        the Hessian Matrix is stored in ihess.

        Parameters
        ----------
        D : Dataset
            Training dataset.
        x0 : list, optional
            Initial guess for the parameters, by default [1, 1].
        solver : str, optional
            The optimization solver to use, by default "Nelder-Mead".

        Raises
        ------
        Exception
            Raised if MAP optimization does not succeed.

        Returns
        -------
        None

        """
        def callback(X):
            """
            Callback function for optimization.

            Parameters
            ----------
            X : array-like
                Current parameter values.

            Returns
            -------
            None

            """
            current_min = -self.log_posterior(D, *X)
            _log.info(f"Iter: {self.n_eval:d} -- Params: {X} -- Min {current_min:.3f}")
            self.n_eval += 1
        try:
            method = solver.pop("method")
            solver = solver
            _log.info(f"{self.__class__.__name__}.{self.MAP.__name__} -- User defined solver {method}, {solver}")
        except (KeyError, AttributeError):
            method = "Nelder-Mead"
            solver = {'disp': True, 'maxiter': 1e10}
            _log.info(f"{self.__class__.__name__}.{self.MAP.__name__} -- Default solver {method}, {solver}")

        if self.theta_hat is not None and self.ihess is not None:
            _log.warning(f"{self.__class__.__name__}.{self.MAP.__name__} -- Optimal value known. Skipping MAP.")
        else:
            _log.warning(f"{self.__class__.__name__}.{self.MAP.__name__} -- Run MAP.")
            self.n_eval = 0
            result = minimize(lambda t: -self.log_posterior(D, *t), x0=x0,
                              method=method, callback=callback,
                              options=solver)

            if result.success:
                _log.warning(f"{self.__class__.__name__}.{self.MAP.__name__} -- MAP succeeded.")
                self.theta_hat = result.x
                hessfun = Hessian(lambda t: -self.log_posterior(D, *t))
                _log.info(f"{self.__class__.__name__}.{self.MAP.__name__} -- Compute inverse Hessian Matrix.")
                self.ihess = np.linalg.inv(hessfun(self.theta_hat))
                self.laplace_posterior()
                _log.warning(f"{self.__class__.__name__}.{self.MAP.__name__} -- theta_hat {self.theta_hat}")
                _log.warning(f"{self.__class__.__name__}.{self.MAP.__name__} -- ihess {self.ihess}")
            else:
                raise Exception("MAP did not succeede.")
            
    def laplace_posterior(self) -> None:
        """
        Load Laplace approximation.

        .. math::
            P[\\theta | D] \sim \mathcal{N}(\hat{\\theta}, \mathbf{H}^{-1})

        and its marginal distributions, where :math:`\hat{\\theta}` is the optimal value from MAP,\
            and :math:`\mathbf{H}^{-1}` is the inverse Hessian matrix of :math:`-\log P[\\theta | D]`

        Returns
        -------
        None.

        """
        _log.debug(f"{self.__class__.__name__}.{self.laplace_posterior.__name__} -- Load distributions.")
        self.joint = multivariate_normal(mean = self.theta_hat, cov=self.ihess)
        for idx in range(self.theta_hat.shape[0]):
            setattr(self, "marginal_" + self.pars[idx], norm(loc=self.theta_hat[idx], scale=self.ihess[idx][idx]**0.5))
      
    def predictive_posterior(self, posterior_samples: int, D, post_op: callable = None, random_state: int = 0) -> np.ndarray:
        """
        Evaluate the predictive posterior using the specified number of samples.

        Parameters
        ----------
        posterior_samples : int
            The number of posterior samples to generate.
        D : Dataset
            The dataset supplied for predicting the corresponding output.
        post_op : Callable[..., Any], optional
            Posterior operation function. Default is None.
        random_state: int
            Random state for numpy to sample the posterior. The default is 0.

        Returns
        -------
        np.ndarray
            Predictive posterior samples processed via post_op, if provided.

        """
        np.random.seed(0)
        _log.debug(f"{self.__class__.__name__}.{self.predictive_posterior.__name__}")
        self.posterior_samples = posterior_samples
        predictions = []
        
        for k in range(0,self.posterior_samples):
            predictions.append(self.predictor(D, *self.joint.rvs(1)))
        predictions = np.array(predictions)

        if post_op is not None:
            _log.debug(f"{self.__class__.__name__}.{self.predictive_posterior.__name__} -- Return {post_op.__name__}")
            return post_op(predictions, axis=0)
        else:
            _log.debug(f"{self.__class__.__name__}.{self.predictive_posterior.__name__} -- Return prediction stack")
            return predictions
    
    def __repr__(self) -> str:
        # attributes_str = ',\n '.join(f'{key} = {vars(self)[key]}' for key in vars(self).keys())
        return f"{self.__class__.__name__}({vars(self)})"

class AbstractMAPViewer(ABC):
    """
    Abstract viewer for inspecting MAP elements and Laplace's Variational approximation
    of the posterior.
    """
    
    def __init__(self, p1: str, b1: list, n1: int, p2: str, b2: list, n2: int, spacing: float = "lin", **kwargs: Dict[str, float]) -> None:
        """
        Initialize the AbstractMAPViewer.

        Parameters
        ----------
        p1 : str
            Name of the first parameter.
        b1 : list
            Bounds for the first parameter.
        n1 : int
            Number of grid points for the first parameter.
        p2 : str
            Name of the second parameter.
        b2 : list
            Bounds for the second parameter.
        n2 : int
            Number of grid points for the second parameter.
        spacing : float
            Spacing between grid points, linear of logarithmic.
        kwargs: Dict[str, Any]

            - name: str
                name of the instance.

        Returns
        -------
        None

        """
        try:
            self.name = kwargs.pop("name")
        except KeyError:
            self.name = "Untitled"

        self.pars = (p1, p2)
        self.p1 = p1
        self.p2 = p2
        self.n1 = n1
        self.n2 = n2
        self.b1 = b1
        self.b2 = b2
        self.spacing = spacing
        setattr(self, "bounds_" + p1, b1)
        setattr(self, "bounds_" + p2, b2)
        _log.debug(f"{self.__class__.__name__}.{self.__init__.__name__} -- {self}")
        
        X1, X2 = grid_factory(getattr(self, "bounds_" + p1),
                              getattr(self, "bounds_" + p2),
                              self.n1, self.n2, spacing)
        setattr(self, p1, X1)
        setattr(self, p2, X2)

    @abstractmethod
    def contour(self):
        """
        Display the contour of the Bayes elements log-prior, -likelihood, and -posterior.
        """
        ...
    
    def config(self, save: bool = False, folder: str = "./", fmt: str = "png", dpi: int = 300) -> None:
        """
        Configure settings for saving plots.

        Parameters
        ----------
        save : bool, optional
            Flag indicating whether to save plots. The default is False.
        folder : str, optional
            Folder path where plots will be saved. The default is "./".
        fmt : str, optional
            Format for saving plots. The default is "png".
        dpi : int, optional
            Dots per inch for saving plots. The default is 300.

        Returns
        -------
        None

        """
        _log.debug(f"{self.__class__.__name__}.{self.config.__name__}")
        self.save = save
        self.folder = folder
        self.fmt = fmt
        self.dpi = dpi

    def config_contour(self, levels: int = 21, clevels: int = 11,  cmap: str = "viridis",
                       xlim = None, ylim = None,
                       translator: Dict = dummy_translator) -> None:
        """
        Configure contour plot settings.

        Parameters
        ----------
        levels : int, optional
            The number of contour levels for the main plot. The default is 21.
        clevels : int, optional
            The number of contour levels for the colorbar. The default is 11.
        cmap : str, optional
            The colormap to use for the plot. The default is "viridis".
        translator: Dict or callable
            Mapper for labels.

        Returns
        -------
        None
        """
        _log.debug(f"{self.__class__.__name__}.{self.config_contour.__name__}")
        self.levels = levels
        self.clevels = clevels
        self.cmap = cmap

        self.xlabel = translator[self.p1]
        self.ylabel = translator[self.p2]

        if xlim is not None and xlim is not None:
            self.b1 = xlim
            self.b2 = ylim
    
    def __repr__(self):
        attributes_str = ',\n '.join(f'{key} = {value}' for key, value in vars(self).items())
        return f"{self.__class__.__name__}({attributes_str})"
