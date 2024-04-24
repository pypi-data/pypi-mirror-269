#                                                                       Modules
# =============================================================================

# Standard
from dataclasses import dataclass

# Third-party
import optax

# Local
from .adapters.optax_implementations import OptaxOptimizer
from .optimizer import OptimizerParameters

#                                                          Authorship & Credits
# =============================================================================
__author__ = 'Martin van der Schelling (M.P.vanderSchelling@tudelft.nl)'
__credits__ = ['Martin van der Schelling']
__status__ = 'Stable'
# =============================================================================
#
# =============================================================================


@dataclass
class Adam_Hyperparameters(OptimizerParameters):
    """Hyperparameters for Adam Optax optimizer"""

    learning_rate: float = 0.001
    beta_1: float = 0.9
    beta_2: float = 0.999
    epsilon: float = 1e-07
    eps_root: float = 0.0


class Adam(OptaxOptimizer):
    require_gradients: bool = True
    hyperparameters: Adam_Hyperparameters = Adam_Hyperparameters()

    def set_algorithm(self):
        self.algorithm = optax.adam(
            learning_rate=self.hyperparameters.learning_rate,
            b1=self.hyperparameters.beta_1,
            b2=self.hyperparameters.beta_2,
            eps=self.hyperparameters.epsilon,
            eps_root=self.hyperparameters.eps_root
        )


# =============================================================================


@dataclass
class SGDOptax_Hyperparameters(OptimizerParameters):
    """Hyperparameters for SGD Optax optimizer"""

    learning_rate: float = 0.01
    momentum: float = 0.0
    nesterov: bool = False


class SGDOptax(OptaxOptimizer):
    require_gradients: bool = True
    hyperparameters: SGDOptax_Hyperparameters = SGDOptax_Hyperparameters()

    def set_algorithm(self):
        self.algorithm = optax.sgd(
            learning_rate=self.hyperparameters.learning_rate,
            momentum=self.hyperparameters.momentum,
            nesterov=self.hyperparameters.nesterov
        )


# =============================================================================
