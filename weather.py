from configparser import ConfigParser

# Starting a function with _ indicates that it should be non-public

def _get_api_key():
    '''
    Fetch the api key from section [openweather] in secrets.ini file
    
    OBS: API KEY FILE SHOULD NEVER BE COMMITED FOR SAFETY
    '''

    config = ConfigParser()
    config.read('secrets.ini')
    return config['openweather']['api_key']

