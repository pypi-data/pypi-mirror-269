class Message(object):
    """
    Representa un missatge intercanviable entre dos processos diferents.
    És la classe pare i s'aconsella que no fer-la servir. Per enviar un
    missatge genèric utilitzeu la classe ``GenericMessage()``.
    """
    def __init__(self,msg:str) -> None:
        """
        Inicialitzador de la classe Message
        """
        self.msg:str = msg

    def __str__(self) -> str:
        """
        Retorna el text del missatge.
        """
        return self.msg

    def get(self) -> str:
        """
        Obté el text del missatge.
        """
        return self.msg



class GenericMessage(Message):
    """
    Conté un missatge genèric.
    """
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


    
class StatusMessage(Message):
    """
    Conté un missatge d'estat. Un exemple pot ser l'estat d'una resposta o funció avaluada i el seu codi de retorn.
    """
    def __init__(self, msgtype:str, msg: str, return_code:int, nline:int=None) -> None:
        super().__init__(msg)
        self.return_code = return_code
        self.msgtype = msgtype
        self.nline = nline


    def get(self) -> str:
        """
        Obté el text del missatge.
        """
        return f"[({self.return_code}) {self.msgtype}] {self.msg}" if self.nline is None else f"[({self.return_code}) {self.msgtype} <on Line {self.nline}>] {self.msg}"
    
    def __str__(self) -> str:
        """
        Retorna el text del missatge.
        """
        return f"[({self.return_code}) {self.msgtype}] {self.msg}" if self.nline is None else f"[({self.return_code}) {self.msgtype} <on Line {self.nline}>] {self.msg}"


class ProcessMessage(Message):
    def __init__(self, currentCycle:int, totalCycle:int, msg:str) -> None:
        super().__init__(msg)
        self.currentCycle = currentCycle
        self.totalCycle = totalCycle


    def get(self) -> str:
        """
        Obté el text del missatge.
        """
        return f"({round(self.currentCycle/self.totalCycle,1)*100}%) {self.msg}"
    

class EOPMessage(Message):
    """
    Conté un missatge de final de procés (EOP).
    """
    def __init__(self, msg:str = None) -> None:
        super().__init__(msg)