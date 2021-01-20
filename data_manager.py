#! python3

import csv

class Data_manager (): 
    """
    Manage data in csv files
    """

    def __init__ (self, file_csv_path):
        """
        Constructor of class
        """

        # Save in instance the csv file path with all data
        self.csv_file_path = file_csv_path
    
    def get_data (self): 
        """
        return all data from the csv file
        """

        # open file to read
        csv_file = open (self.csv_file_path, "r")
        
        # Use csv module to read data of file
        csv_reader = csv.reader (csv_file)

        # Save data as list 
        data = list (csv_reader)

        # Close file
        csv_file.close ()

        # Return data
        return data
    
    def add_row (self, data_row): 
        """
        Add new register to csv file
        """

        # open file to add lines
        csv_file = open (self.csv_file_path, "a", newline="")
        
        # Use csv module to add row to the file
        csv_writer = csv.writer (csv_file)

        # Write q new row in the file
        csv_writer.writerow (data_row)

        # Close file
        csv_file.close ()
    
    def compare_data (self, external_data):
        """
        Compare the local locally stored information with all data, 
        If new register is detected, return it
        """ 

        # get all data in the local file
        local_data = self.get_data ()

        # List to save the new detected rows
        new_rows = []

        # loop for each register of new information
        for row in external_data: 

            # If row is not in the local data, add to list
            if row not in local_data: 
                new_rows.append (row)

        # Return new rows list
        return new_rows


