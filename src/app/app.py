from modules.create_sidebar import create_sidebar
from modules.load_backtests import load_backtests
from modules.display_results import display_results
import warnings
warnings.filterwarnings("ignore")


create_sidebar()
load_backtests()
display_results()
