import textwrap
import pkgutil
import importlib

DEFAULT_MODEL_CLASS = "edsl.language_models.LanguageModelOpenAIFour"

from edsl.language_models.LanguageModel import RegisterLanguageModelsMeta
from edsl.exceptions.language_models import LanguageModelNotFound

import edsl.language_models.model_interfaces as model_interfaces

# Dynamically import all modules in the model_interfaces package
for loader, module_name, is_pkg in pkgutil.iter_modules(model_interfaces.__path__):
    full_module_name = f"{model_interfaces.__name__}.{module_name}"
    if not is_pkg:
        module = importlib.import_module(full_module_name)
        globals().update(
            {
                name: getattr(module, name)
                for name in dir(module)
                if not name.startswith("_")
            }
        )

meta_class_registry = RegisterLanguageModelsMeta.get_registered_classes()

# For compatibility with older versions of EDSL
get_model_class = (
    lambda model_name: RegisterLanguageModelsMeta.model_names_to_classes().get(
        model_name
    )
)


class Meta(type):
    def __repr__(cls):
        return textwrap.dedent(
            f"""\
        Available models: {cls.available()}
        
        To create an instance, you can do: 
        >>> m = Model('gpt-4-1106-preview', temperature=0.5, ...)
        
        To get the default model, you can leave out the model name. 
        To see the available models, you can do:
        >>> Model.available()
        """
        )


class Model(metaclass=Meta):
    default_model = "gpt-4-1106-preview"

    def __new__(cls, model_name=None, *args, **kwargs):
        # Map index to the respective subclass
        get_model_classes = RegisterLanguageModelsMeta.model_names_to_classes()

        if cls.default_model not in get_model_classes:
            raise ValueError(f"Default model {cls.default_model} not found")

        if model_name is None:
            model_name = cls.default_model

        subclass = get_model_classes.get(model_name, None)
        if subclass is None:
            raise LanguageModelNotFound(model_name)

        # Create an instance of the selected subclass
        instance = object.__new__(subclass)
        instance.__init__(*args, **kwargs)
        return instance

    @classmethod
    def available(cls):
        return sorted(list(RegisterLanguageModelsMeta.model_names_to_classes().keys()))

    @classmethod
    def check_models(cls, verbose=False):
        print("Checking all available models...\n")
        for model in cls.available():
            print(f"Now checking: {model}")
            try:
                m = cls(model)
            except Exception as e:
                print(f"Error creating instance of {model}: {e}")
                continue
            try:
                results = m.hello(verbose)
                if verbose:
                    print(f"Results from model call: {results}")
            except Exception as e:
                print(f"Error calling 'hello' on {model}: {e}")
                continue
            print("OK!")
            print("\n")


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)

    available = Model.available()
    m = Model("gpt-4-1106-preview")
    results = m.execute_model_call("Hello world")
    print(results)
