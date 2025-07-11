"""Définitions des valeurs pour l'évaluateur Pithon."""

from typing import Union,  Callable
from dataclasses import dataclass
from pithon.syntax import ( PiFunctionDef,
)
from pithon.evaluator.envframe import EnvFrame

PrimitiveFunction = Callable[..., 'EnvValue']

@dataclass
class VFunctionClosure:
    """Représente une fermeture de fonction avec son environnement."""
    funcdef: PiFunctionDef
    closure_env: EnvFrame

    def __str__(self) -> str:
        return f"<function {self.funcdef.name} at {id(self)}>"
@dataclass
class VList:
    """Représente une liste de valeurs."""
    value: list['EnvValue']

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return repr(self.value)


@dataclass
class VTuple:
    """Représente un tuple de valeurs."""
    value: tuple['EnvValue', ...]

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return repr(self.value)


@dataclass
class VNumber:
    """Représente un nombre (float)."""
    value: float

    def __str__(self) -> str:
        return str(self.value)


    def __repr__(self) -> str:
        return repr(self.value)


@dataclass
class VBool:
    """Représente une valeur booléenne."""
    value: bool

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return repr(self.value)


@dataclass
class VNone:
    """Représente la valeur None."""
    value: None = None

    def __str__(self) -> str:
        return str(None)

    def __repr__(self) -> str:
        return repr(self.value)


@dataclass
class VString:
    """Représente une chaîne de caractères."""
    value: str

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return repr(self.value)


@dataclass
class VClassDef:
    """Représente une définition de classe avec ses méthodes."""
    name: str
    methods: dict[str, VFunctionClosure]

    def __str__(self) -> str:
        return f"<class {self.name} at {id(self)}>"
    
    def call(self, args, env: EnvFrame):
        from pithon.evaluator.evaluator import evaluate_stmt  

        """Instancie la classe et appelle __init__ si présent."""
        instance = VObject(self)
        init = self.methods.get("__init__")
        if init:
            call_env = EnvFrame(parent=init.closure_env)
            call_env.insert("self", instance)
            for i, arg_name in enumerate(init.funcdef.arg_names[1:]):
                call_env.insert(arg_name, args[i])
            for stmt in init.funcdef.body:
                evaluate_stmt(stmt, call_env)
        return instance
    
@dataclass
class VObject:
    """Représente une instance d'une classe avec ses attributs."""
    class_def: VClassDef
    attributes: dict[str, 'EnvValue']
    def __init__(self, cls: VClassDef):
        self.cls = cls
        self.attributes = {}

    def get(self, name: str) -> 'EnvValue':
        """Retourne un attribut ou une méthode liée (bound method)."""
        if name in self.attributes:
            return self.attributes[name]
        elif name in self.cls.methods:
            return VMethodClosure(self.cls.methods[name], self)
        else:
            raise AttributeError(f"Attribut ou méthode '{name}' introuvable dans {self.cls.name}")

    def __str__(self) -> str:
        return f"<{self.class_def.name} object at {id(self)}>"

    def __repr__(self) -> str:
        return self.__str__()
    

@dataclass
class VMethodClosure:
    """Représente une méthode liée à une instance."""
    function: VFunctionClosure
    instance: VObject

    def __str__(self) -> str:
        return f"<method {self.function.funcdef.name} of {self.instance.class_def.name} at {id(self)}>"

    def __repr__(self) -> str:
        return self.__str__()

    def call(self, args, env: EnvFrame):
        """Appelle la méthode avec `self`."""
        from pithon.evaluator.evaluator import evaluate_stmt

        call_env = EnvFrame(parent=self.function.closure_env)
        call_env.insert("self", self.instance)

        for i, arg_name in enumerate(self.function.funcdef.arg_names[1:]):
            call_env.insert(arg_name, args[i])

        try:
            for stmt in self.function.funcdef.body:
                evaluate_stmt(stmt, call_env)
        except ReturnException as e:
            return e.value

        return VNone(value=None)
EnvValue = Union[
    VNumber,
    VBool,
    VNone,
    VString,
    VList,
    VTuple,
    VObject,
    VFunctionClosure,
    VMethodClosure,
    VClassDef,
    PrimitiveFunction
]
