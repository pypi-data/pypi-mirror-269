import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

#Child Class
class Gaussian(Distribution):
    """ Gaussian distribution class for calculating and 
    visualizing a Gaussian distribution.
    
    Attributes:
        mean (float) representing the mean value of a number set 
        (SAMPLE or POPULATION - calc is the same)
        
        stdev (float) representing the SAMPLE (subset of population data, estimate)
        or POPULATION (access to all data points, true variability) standard deviation 
        of a number set
        
        data_list (list of floats*) a list of floats* extracted from the data file
        *likely to be either a whole number or decimal for a gaussian distribution    
    """
    def __init__(self, mu=0, sigma=1):
        
        Distribution.__init__(self, mu, sigma)
    
        
    
    def calculate_mean(self):
    
        """Function to calculate the mean of the data set.
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
        
        The expression 1.0 * sum(self.data) / len(self.data) is using 1.0 to ensure 
        that the division is carried out as a floating point division rather than an 
        integer division
    
        """
                    
        avg = 1.0 * sum(self.data) / len(self.data)
        
        self.mean = avg
        
        return self.mean


    def calculate_stdev(self, sample=True):

        """Function to calculate the standard deviation of the data set.
        
        Args: 
            sample (bool): whether the data represents a sample or population. 
            Default/True is for SAMPLE std dev
        
        Returns: 
            float: standard deviation of the data set
    
        """

        if sample:
            n = len(self.data) - 1 #when sample=TRUE for SAMPLE std dev the divisor formula is n-1
        else:
            n = len(self.data)  #when sample=FALSE for POPULATION std dev n is length|total data points
    
        mean = self.calculate_mean()
    
        sigma = 0
    
        for d in self.data:
            sigma += (d - mean) ** 2
        
        sigma = math.sqrt(sigma / n)
    
        self.stdev = sigma
        
        return self.stdev
        
        
        
    def plot_histogram(self):
        """Function to output a histogram of the data instances/frequency against data distribution 
        using the matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """
        plt.hist(self.data)
        plt.title('Histogram of Data')
        plt.xlabel('Data Distribution')
        plt.ylabel('Frequency')
        
        
        
    def pdf(self, x):
        """Probability density function calculator for the gaussian distribution.
        
        Args:
            x (float): point for calculating the probability density function
        
        Returns:
            float: probability density function output

        (1.0 / (self.stdev * math.sqrt(2*math.pi))): This part calculates the normalization 
        factor for the Gaussian distribution, ensuring that the area under the curve sums to 1. 
        It involves dividing 1 by the product of the standard deviation (self.stdev) and the 
        square root of 2 * pi

        math.exp(-0.5*((x - self.mean) / self.stdev) ** 2): This part calculates the exponential 
        term of the Gaussian distribution. It involves taking the negative exponent of 0.5 times 
        the square of the standardized value ((x - self.mean) / self.stdev)
        
        By multiplying the normalization factor with the exponential term, the method returns the 
        value of the Gaussian distribution's PDF at the point x
        """
        
        return (1.0 / (self.stdev * math.sqrt(2*math.pi))) * math.exp(-0.5*((x - self.mean) / self.stdev) ** 2)
        

    def plot_histogram_pdf(self, n_spaces = 50):

        """Function to plot the normalised histogram of the data and a plot of the 
        probability density function along the same range
        
        Args:
            n_spaces (int): number of data points 
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
            
        """
        
        mu = self.mean
        sigma = self.stdev

        min_range = min(self.data)
        max_range = max(self.data)
        
         # calculates the interval between x values
        interval = 1.0 * (max_range - min_range) / n_spaces

        x = []
        y = []
        
        # calculate the x values to visualize
        for i in range(n_spaces):
            tmp = min_range + interval*i
            x.append(tmp)
            y.append(self.pdf(tmp))

        # make the plots
        fig, axes = plt.subplots(2,sharex=True)
        fig.subplots_adjust(hspace=1)
        axes[0].hist(self.data, density=True)
        axes[0].set_title('Normalised Histogram of Data')
        axes[0].set_ylabel('Probability Density / Δx')
        axes[0].set_xlabel('Values')  

        axes[1].plot(x, y)
        axes[1].set_title('Gaussian Distrubution Curve\n (Expected Normal Distribution based on \n Mean and Standard Deviation)')
        axes[1].set_ylabel('Probability Density')
        axes[1].set_xlabel('Values')
        plt.show()

        return x, y
        
    def __add__(self, other):
        
        """Function to add together two Gaussian distributions
        
        Args:
            other (Gaussian): Gaussian instance
            
        Returns:
            Gaussian: Gaussian distribution
        
        Use the + operator between the two binomial instances. 
        This will create a new Gaussian instance with combined mean and std dev.   
        """
        
        result = Gaussian()
        result.mean = self.mean + other.mean
        result.stdev = math.sqrt(self.stdev ** 2 + other.stdev ** 2)
        
        return result
        
        
    def __repr__(self):
    
        """Function to output the characteristics of the Gaussian instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Gaussian
        
        """
        mean = round(self.mean, 2)
        stdev = round(self.stdev, 2)
        return "mean {}, standard deviation {}".format(mean, stdev)
