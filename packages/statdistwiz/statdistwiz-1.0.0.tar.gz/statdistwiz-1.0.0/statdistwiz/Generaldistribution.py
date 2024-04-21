#Parent class
class Distribution:
    def __init__(self, mu=0, sigma=1):
        """ Generic distribution class for calculating and 
        visualizing a probability distribution.
        Attributes:
            mean (float) representing the mean value of the distribution
            stdev (float) representing the standard deviation of the distribution
            data_list (list of floats*) a list of floats* extracted from the data file
            *likely to be a whole number e.g. 1 or 0 for a binomial distribution and either
            a whole number or decimal for a gaussian distribution
        """
        self.mean = mu #mu is mean default value is set to 0
        self.stdev = sigma # #sigma is std dev default value is set to 1
        self.data = []


    def read_data_file(self, file_name):
        """Function to read in data from a txt file. The txt file should have
        one number (float or int) per line. The numbers are stored in the data attribute.

        Args:
            file_name (string): name of a file to read from

        Returns:
            None

        """

        with open(file_name) as file:
            data_list = []
            line = file.readline()
            while line:
                try:
                    data_list.append(float(line))
                except ValueError:
                    data_list.append(int(line))
                line = file.readline()
    # No need to explicitly close file when using with statement.
        self.data = data_list

