class KfileClient:

    def __init__(self):
        pass

    '''
    Copys a file of a given path from the vizy to google drive in the requested directory and returns the id
    '''
    def copy_to(self, location, destination, create=False): 
        pass

    '''
    Copys a file from the desired location in google drive to the correct path on the vizy
    '''
    def copy_from(self, location, destination):
        pass

    '''
    returns a list of files at a specific path in google drive
    '''
    def list(self, path):
        pass

    '''
    returns the url in google drive of a file or folder at the provided path
    '''
    def get_url(self, path):
        pass