try:
    from . import agent
except (ImportError, ModuleNotFoundError):
    # Optional dependency missing (e.g. `google.adk`).
    # Avoid raising on package import so consumers can import submodules explicitly.
    pass
