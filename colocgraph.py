#!/usr/bin/env python3
# Modules
try:
    import os
    import pandas as pd
    import matplotlib.pyplot as plt
    import argparse
except ImportError:
    print("Some required modules are not installed. Required are:\n os\n pandas\n matplotlib\n argparse")

# Functions
def get_txt_files( 
        dir: str,
)-> list:
    '''
    Finds all .txt files in the specified directory.
    :param dir: string of the directory
    :return: list of paths to .txt files in the directory
    '''
    txt_files = []

    try:
        for root, _, files in os.walk( dir ):
            for file in files:
                if file.endswith( '.txt' ):
                    txt_files.append( os.path.join( root, file ) )
                    
    except Exception as e:
        print( f"An error occurred while accessing the directory: { e }" )
    
    return txt_files

def load_txt(
        file_path: str,
        # column_names: list = [ "Distance [µm]", "Intensity Ch2-T1", "Intensity Ch1-T2", "Intensity Ch1-T3" ],
) -> pd.DataFrame:
    '''
    Load .txt file as pd.DataFrame.
    :param file_path: string, file path
    :return: pd.DataFrame with data
    '''
    try:
        df = pd.read_csv( file_path, sep= '\t', skiprows= 1, encoding='ISO-8859-1' )
        return df.dropna()
    
    except FileNotFoundError:
        print( f"File '{ file_path }' not found." )
        return None
    
    except Exception as e:
        print( f"An error occurred while loading the file: {e}" )
        return None

def plot_df(
        df: pd.DataFrame,
        image_file_name,
        image_data_type: str = "svg",
        width: float = 10.0,
        height: float = 6.0,
        x_label: str = None,
        y_label: str = None,
        font_size: int = 14,
        colors: list = [ "red", "green", "blue" ],
        column_order: str = "312",
        legend: bool = False,
):
    '''
    Plots data from a DataFrame with the first column as the x-axis and the remaining columns as y-values in a specified order and a specified color.

    Necessary
    :param df: pd.DataFrame
    :param image_file_name: string, file name of image

    Optional
    :param image_data_type: string, mage data type
    :param width: float, image width
    :param height: float, image height
    :param x_label: str, x-axis label
    :param y_label: str, y-axis label
    :param font_size: int, font size
    :param colors: list, colors
    :param column_order: str, specifies column order e.g., "312"
    :param legend: bool, legend printed

    :return: saves a file
    '''

    # Initial settings
    column_indices = [ int( i ) for i in column_order ] # Turn order into iterable list
    plt.rcParams.update( { 'font.size': font_size } ) # Update font size
    plt.figure( figsize= ( width, height ) ) # Initialize plot
    
    # Plotting
    for col_idx in column_indices: # Iterate through column_indices

        if col_idx <= len( df.columns ) - 1: # Ensure column index can be used

            plt.plot( 
                df.iloc[ :, 0 ], # First column as x-axis
                df.iloc[ :, col_idx ],
                color= colors[ col_idx - 1 ], # Use specified color 
                label= df.columns[ col_idx - 1 ],
            )

    # Post settings
    plt.xlabel( x_label ) # Add x label
    plt.ylabel( y_label ) # Add y label
    if legend: # Add legend if desired
        plt.legend()
    plt.tight_layout()
    
    # Saving
    plt.savefig( f"{ image_file_name }.{ image_data_type }", format= image_data_type )
    plt.close()

def main(
        dir: str,
        image_data_type: str = "svg",
        width: float = 10.0,
        height: float = 6.0,
        x_label: str = None,
        y_label: str = None,
        font_size: int = 20,
        colors: list = [ "red", "green", "blue" ],
        column_order: str = "312",
        legend: bool = False,
):
    '''
    Main function.
    - receives a directory
    - extracts all .txt files from this directory
    - plots the data according to optional image settings

    Necessary
    :param dir: string, directory path

    Optional
    :param df: pd.DataFrame
    :param image_file_name: string, file name of image
    :param image_data_type: string, mage data type
    :param width: float, image width
    :param height: float, image height
    :param x_label: str, x-axis label
    :param y_label: str, y-axis label
    :param font_size: int, font size
    :param colors: list, colors
    :param column_order: str, specifies column order e.g., "312"
    :param legend: bool, legend printed

    :return: saves a file
    '''
    
    txt_files = get_txt_files( dir= dir ) # extract paths to txt files from directory

    for tf in txt_files: # iterate through each .txt file
        
        df = load_txt( file_path= tf ) # load .txt file as pd.DataFrame

        plot_df(
            df= df,
            image_file_name= os.path.basename( tf ),
            image_data_type= image_data_type,
            width = width,
            height= height,
            x_label= x_label,
            y_label= y_label,
            font_size= font_size,
            colors= colors,
            column_order= column_order,
            legend= legend,
        ) # Plot data, use adjustments

# Code
if __name__ == "__main__":

    # Receive Arguments
    parser = argparse.ArgumentParser(description="colocgraph.py: Process and Plot Immunofluorescence Data." )
    parser.add_argument( "input_dir", help="Path to Input Directory" )
    parser.add_argument( "--image_data_type", help= "Data Type of Output Images" )
    parser.add_argument( "--order", type = str, default= "312", help= "Order of Printing Columns e.g., 312" )
    parser.add_argument( "--width", type=int, default= 4, help= "Width of the Plot" )
    parser.add_argument( "--height", type=int, default= 2, help= "Height of the Plot" )
    parser.add_argument( "--font_size", type=int, default= 9, help= "Font Size within the Plot" )
    parser.add_argument( "--legend", type= bool, default= False, help= "Print Legend True/False" )
    parser.add_argument( "--x_label", type = str, default= None, help= "X Label" )
    parser.add_argument( "--y_label", type = str, default= None, help= "Y Label" )
    args = parser.parse_args()

    # Parse Argumnets into main()
    main(
        dir= args.input_dir,
        width= args.width,
        height= args.height,
        font_size= args.font_size,
        legend = args.legend,
        column_order= args.order,
    )
