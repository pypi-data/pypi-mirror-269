#########################################################################################

# Import necessary modules for authentication and working with SharePoint files
from office365.sharepoint.files.file import File
from io import BytesIO
import pandas as pd
import io

#########################################################################################

def combine_files_into_dataframe(ctx, folder_url, sheet_name = 0):
    """
    Combine files from a SharePoint folder into a single pandas DataFrame.
    
    :param ctx: ClientContext object authenticated with SharePoint.
    :param folder_url: Server-relative URL of the SharePoint folder containing files.
    :return: Combined pandas DataFrame if successful, None otherwise.
    """
    try:
        # Get the folder object using the provided folder URL
        folder = ctx.web.get_folder_by_server_relative_url(folder_url)
        # Get the collection of files in the folder
        files = folder.files
        # Load the files collection
        ctx.load(files)
        # Execute the query to retrieve the files
        ctx.execute_query()
        # Initialize an empty list to store individual DataFrames
        all_data_frames = []
        # Iterate through each file in the folder
        for file in files:
            # Get the name of the file
            file_name = file.properties["Name"]
            # Open the file and get its content
            response = File.open_binary(ctx, file.serverRelativeUrl)
            file_content = response.content
            # Check the file extension to determine the file type
            if file_name.lower().endswith('.csv'):
                # Read CSV file content into a pandas DataFrame using BytesIO
                df = pd.read_csv(io.BytesIO(file_content))
            elif file_name.lower().endswith('.xlsx'):
                # Read XLSX file content into a pandas DataFrame
                df = pd.read_excel(io.BytesIO(file_content),sheet_name=sheet_name)
            else:
                # Skip files with unsupported extensions
                continue
            # Append the DataFrame to the list
            all_data_frames.append(df)
        # Concatenate all individual DataFrames into a single DataFrame
        combined_df = pd.concat(all_data_frames, ignore_index=True)
        # Return the combined DataFrame
        return combined_df
    # Handle any exceptions that may occur during file reading
    except Exception as e:
        print('Problem reading files: ', e)
        return None

#########################################################################################

def get_folder_urls(ctx, document_library_relative_url: str):
    """
    Function to return a list of URLs of folders present in a given path in SharePoint.

    Parameters:
        - ctx: SharePoint context object.
        - document_library_relative_url (str): Relative URL of the document library.

    Returns:
        - List[str]: List of URLs of folders present in the given path.
    """
    # Getting the root folder of the document library
    root_folder = ctx.web.get_folder_by_server_relative_path(document_library_relative_url)
    ctx.load(root_folder, ["Folders"])
    ctx.execute_query()

    # Extracting the paths of Level 1 folders within the root folder
    folder_urls = [f'{document_library_relative_url}/{folder.name}' for folder in root_folder.folders]
    
    return folder_urls

# Example usage:
# Assuming you have ctx already defined
# ctx = get_sharepoint_context()  # Get SharePoint context

#########################################################################################

def get_file_paths(ctx, subfolder_urls_files: str):
    """
    Function to return a list of paths of files present in a given subfolder in SharePoint.

    Parameters:
        - ctx: SharePoint context object.
        - subfolder_urls_files (str): Relative URL of the subfolder containing files.

    Returns:
        - List[str]: List of paths of files present in the given subfolder.
    """
    # Get the root folder of the Level 2 folder
    root_folder_level2 = ctx.web.get_folder_by_server_relative_path(subfolder_urls_files)
    ctx.load(root_folder_level2, ["Files"])
    ctx.execute_query()

    # Initialize a list to store file paths
    file_paths = []

    # Iterate over files within the Level 2 folder
    for file in root_folder_level2.files:
        # Append the path of each file to the list
        file_paths.append(f'{subfolder_urls_files}/{file.name}')

    return file_paths

# Example usage:
# Assuming you have ctx already defined
# ctx = get_sharepoint_context()  # Get SharePoint context

#########################################################################################

def read_file_from_sharepoint(ctx, file_url, sheet_name=0):
    """
    Function to read a file from SharePoint and return its content as a pandas DataFrame.

    Parameters:
        - file_url (str): URL of the file in SharePoint.
        - ctx: SharePoint context object.
        - sheet_name (str or int, optional): Name or index of the sheet to read (for Excel files). Defaults to 0.

    Returns:
        - pd.DataFrame: DataFrame containing the content of the file.
    """
    # Get the file from SharePoint
    file = File.open_binary(ctx, file_url)
    # Check the file extension to determine the file type
    if file_url.lower().endswith('.csv'):
        # Read CSV file content into a pandas DataFrame using BytesIO
        df = pd.read_csv(BytesIO(file.content))
    elif file_url.lower().endswith('.xlsx'):
        # Read XLSX file content into a pandas DataFrame
        df = pd.read_excel(BytesIO(file.content), sheet_name=sheet_name, engine='openpyxl')
    else:
        # Skip files with unsupported extensions
        print("Unsupported file extension. Please use .csv or .xlsx files.")
        return None
    return df

#########################################################################################
