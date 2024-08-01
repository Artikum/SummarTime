from Forbiden_Topics_Detector import check_forbidden_words
import eel
@eel.expose
def cfw_py(text : str, forbidden_words:dict)->bool:
    return cfw(text, forbidden_words)
