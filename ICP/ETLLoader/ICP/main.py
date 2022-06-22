import sys
sys.path.append('../..')
import XdmLib
log = XdmLib.logging.getLogger()
config = XdmLib.config
import Parsing

folder = 'D:\_Work\_Owen\Loader_New_Demo\ETLLoader\file2db\Data\Archive'
result, filelist = Parsing.convertallfiletodfinlist(folder)
print(result,filelist)