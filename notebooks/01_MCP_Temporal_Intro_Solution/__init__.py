import os
from pathlib import Path
from IPython.display import display, Code

def load_solution(filename: str):
    """Load and display a solution file, then execute it in the global namespace."""
    solution_path = Path(__file__).parent / filename

    if not solution_path.exists():
        print(f"❌ Solution file not found: {filename}")
        return

    code = solution_path.read_text()

    # Display the code with syntax highlighting
    print("📝 Solution loaded:")
    display(Code(code, language='python'))

    # Execute the code in the caller's namespace
    import inspect
    frame = inspect.currentframe().f_back
    exec(code, frame.f_globals)

    print("✅ Solution executed successfully!")
