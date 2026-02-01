"""
Function registry for managing formula functions.
"""

from typing import Callable, Any


class FunctionRegistry:
    """Registry for formula functions.

    Functions are stored as attributes so they can be passed to df.eval()
    via local_dict=self.__dict__.
    """

    def __init__(self):
        self._function_docs: dict[str, str] = {}

    def register(self, name: str, func: Callable, doc: str = "") -> "FunctionRegistry":
        """Register a function with the given name.

        Args:
            name: Function name (will be called as @name in formulas)
            func: The function implementation
            doc: Optional documentation string

        Returns:
            self for method chaining
        """
        setattr(self, name, func)
        if doc:
            self._function_docs[name] = doc
        return self

    def unregister(self, name: str) -> "FunctionRegistry":
        """Remove a function from the registry.

        Args:
            name: Function name to remove

        Returns:
            self for method chaining
        """
        if hasattr(self, name):
            delattr(self, name)
        self._function_docs.pop(name, None)
        return self

    def has(self, name: str) -> bool:
        """Check if a function is registered."""
        return hasattr(self, name) and name != "_function_docs"

    def get(self, name: str) -> Callable:
        """Get a function by name.

        Raises:
            KeyError: If function is not registered
        """
        if not self.has(name):
            raise KeyError(f"Function '{name}' not registered")
        return getattr(self, name)

    def list_functions(self) -> list[str]:
        """List all registered function names."""
        return [
            k for k in self.__dict__.keys()
            if not k.startswith("_") and callable(getattr(self, k))
        ]

    def get_doc(self, name: str) -> str:
        """Get documentation for a function."""
        return self._function_docs.get(name, "")

    def as_dict(self) -> dict[str, Any]:
        """Return registry as dict for df.eval() local_dict parameter."""
        return self.__dict__
