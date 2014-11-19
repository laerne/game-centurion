#import collections
import os.path
    
def path_relative_to_file_directory( origin, path ):
    if os.path.isabs(path):
        return path
    return os.path.join( os.path.dirname(origin), path )
