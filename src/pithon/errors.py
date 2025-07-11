
class PiRuntimeError(Exception):
    """Exception pour les erreurs d'exécution dans le langage Pithon."""
    pass

class ReturnException(Exception):
    """Exception pour retourner une valeur depuis une fonction."""
    def __init__(self, value):
        self.value = value

class BreakException(Exception):
    """Exception pour sortir d'une boucle (break)."""
    pass

class ContinueException(Exception):
    """Exception pour passer à l'itération suivante (continue)."""
    pass

class PiArgumentError(Exception):
    """Exception pour les erreurs d'arguments dans les fonctions."""
    pass
