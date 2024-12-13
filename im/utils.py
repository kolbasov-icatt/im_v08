import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

    
class DemandGenerator:
    def __init__(self, generator_agrs: dict):
        self.distribution = generator_agrs['distribution']
        self.mean = generator_agrs['mean']
        self.std = generator_agrs['std']
        self.variance = self.std ** 2
        self.n_samples = generator_agrs['period_length']
        
        # Ensure valid input
        if self.mean < 0 or self.std < 0 or self.n_samples <= 0:
            raise ValueError("Mean, standard deviation, and period length must be positive values.")

    def simulate_demand(self, random_state=None) -> np.ndarray:
        if self.mean > 0:
            if self.distribution == "negative_binomial":
                demand = self._negative_binomial(random_state=random_state)
            elif self.distribution == "poisson":
                demand = self._poisson(random_state=random_state) 
            elif self.distribution == "normal":
                demand = self._normal(random_state=random_state)            
            else:
                raise NotImplementedError(f"Distribution {self.distribution} not supported. Try 'negative_binomial' or 'poisson'.")
        elif self.mean == 0:
            demand = np.zeros(self.n_samples)
        return demand

    def _negative_binomial(self, random_state=None) -> np.ndarray:
        # Calculate Negative Binomial parameters from mean and variance
        if self.variance <= self.mean:
            raise ValueError("Variance must be greater than the mean for Negative Binomial distribution")
        p = self.mean / self.variance  # Success probability
        n = self.mean**2 / (self.variance - self.mean)  # Number of failures
        
        # Generate negative binomial demand
        demand = stats.nbinom.rvs(n, p, size=self.n_samples, random_state=random_state)
        return demand
    
    def _poisson(self, random_state=None) -> np.ndarray:
        # Generate Poisson demand
        demand = stats.poisson.rvs(self.mean, size=self.n_samples, random_state=random_state)
        return demand
    
    def _normal(self, random_state=None) -> np.ndarray:
        # Generate Normal demand
        demand = stats.norm.rvs(self.mean, self.std, size=self.n_samples, random_state=random_state)
        return demand
    
    def plot_demand_histogram(self, demand):
        plt.figure(figsize=(10, 6))
        plt.hist(demand, alpha=0.6, color='orange', density=True)
        plt.title(f'Histogram of Stochastic Demand\nMean: {demand.mean():.2f}. Std: {demand.std():.2f}')
        plt.xlabel('Demand')
        plt.ylabel('Density')
        plt.show()

    def plot_demand(self, demand):
        plt.figure(figsize=(10, 6))
        plt.plot(demand, alpha=0.8, color='blue')
        plt.title(f'Generated Stochastic Demand\nMean: {demand.mean():.2f}. Std: {demand.std():.2f}')
        plt.xlabel('Period')
        plt.ylabel('Quantity')
        plt.show()
    

