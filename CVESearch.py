import sys
import requests
import pandas as pd

def DownloadCVEData():
    url = "https://cve.mitre.org/data/downloads/allitems.csv"
    file_name = "cve.csv"
    with open(file_name, "wb") as f:
        
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')
        print(f"Downloading {file_name} ({int(total_length)/1000000} Mo)")

        if total_length is None:
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                sys.stdout.flush()
    return file_name

def SearchCvePandas(file_name):
    df = pd.read_csv(file_name, header=None, encoding='latin1', usecols=[0,1,2,3])
    keyword = input('\n\nWhat would you like to search ? : \n')
    df.columns = ['CVE','Author', 'Description', 'Link']
    df_result = df[df.CVE.str.contains(keyword) | df.Author.str.contains(keyword) | df.Description.str.contains(keyword)]
    print(df_result)
    print(f'\nFound {len(df_result.index)} results.')
    return df_result

def OutputToCsv(dataframe):
    output = input('\nDo you want to output result to csv ? (y/n) :\n')
    if output == 'y':
        dataframe.to_csv('search.csv', index=False)
        print("\n'search.csv' has been created.\n")
    else: 
        return

def startProgram():
    file = DownloadCVEData()
    dataframe = SearchCvePandas(file)
    OutputToCsv(dataframe)