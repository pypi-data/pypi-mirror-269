import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

#Child Class
class Binomial(Distribution):
    """ Binomial distribution class for calculating and 
    visualizing a Binomial distribution. 
    
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats*) a list of floats* to be extracted from the data file
        *likely to be a whole number e.g. 1 or 0 for a binomial distribution
        p (float) representing the probability of an event occurring
        n (int) number of trials
                     
    """
    
    
    def __init__(self, prob=.5, size=20):
                
        self.n = size #number of data points
        self.p = prob #probability
        
        Distribution.__init__(self, self.calculate_mean(), self.calculate_stdev())
    
                        
    
    def calculate_mean(self):
    
        """Function to calculate the mean from p and n
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """
        
        self.mean = self.p * self.n
                
        return self.mean



    def calculate_stdev(self):

        """Function to calculate the standard deviation from p and n.
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set
    
        """
        
        self.stdev = math.sqrt(self.n * self.p * (1 - self.p))
        
        return self.stdev
        
        
    def replace_stats_with_data(self):

        """Function to calculate p and n from the data set
        This method is a common way to estimate the probability p 
        from a given set of data in a binomial distribution scenario. It is based 
        on the fundamental relationship between the probability of success in each 
        trial and the overall distribution of outcomes in a binomial experiment

        Calculates the value of p by summing up all the values in the data set and 
        dividing by the length of the data set. Multiplying sum(self.data) by 1.0, 
        is using 1.0 to ensure that the division is carried out as a floating point 
        division rather than an integer division.
        
        Args: 
            None
        
        Returns: 
            float: the p value
            float: the n value
    
        """
   
        if len(self.data) == 0:
            raise ValueError("Please invoke the read_data_file method of the binomial object, passing in your .txt file name as an argument, cannot calculate parameters otherwise.")
    
        self.n = len(self.data)
   
        self.p = 1.0 * sum(self.data) / len(self.data)

        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
    
        return self.p, self.n
       
    def plot_bar(self):
        """Function to output a bar chart of the data outcomes using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """
                
        plt.bar(x = ['0', '1'], height = [(1 - self.p) * self.n, self.p * self.n])
        plt.title('Bar Chart of Data')
        plt.xlabel('Outcome')
        plt.ylabel('Count')
        
        
        
    def pmf(self, k):
        """Probability density function calculator for the binomial distribution.
        
        Args:
            x (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """
        
        a = math.factorial(self.n) / (math.factorial(k) * (math.factorial(self.n - k)))
        b = (self.p ** k) * (1 - self.p) ** (self.n - k)
        
        return a * b
        

    def plot_bar_pmf(self):

        """Function to plot the pmf of the binomial distribution
        
        Args:
            None
        
        Returns:
            list: x values for the pmf plot
            list: y values for the pmf plot
            
        """
        
        x = []
        y = []
        
        # calculate the x values to visualize
        for i in range(self.n + 1):
            x.append(i)
            y.append(self.pmf(i))

        # make the plots
        plt.bar(x, y)
        plt.title('Distribution of Outcomes')
        plt.ylabel('Probability')
        plt.xlabel('Outcome')

        plt.show()

        return x, y
        
    def __add__(self, other):
        #function takes another Binomial instance other as an argument
        """Function to add together two Binomial distributions with equal p ONLY
        
        Args:
            other (Binomial): Binomial instance
            
        Returns:
            Binomial: Binomial distribution
            
        Use the + operator between the two binomial instances. 
        This will create a new Binomial instance with the combined n 
        values, mean, std dev and the same p value.    
        """
        
        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise

        result = Binomial()

        result.n = self.n + other.n

        result.p = self.p

        result.calculate_mean()
        result.calculate_stdev()
        
        return result
        
        
    def __repr__(self):
    
        """Function to output the characteristics of the Binomial instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Gaussian
        
        """
        mean = round(self.mean, 2)
        stdev = round(self.stdev, 2)
        return "mean {}, standard deviation {}, p {}, n {}".\
        format(mean, stdev, self.p, self.n)