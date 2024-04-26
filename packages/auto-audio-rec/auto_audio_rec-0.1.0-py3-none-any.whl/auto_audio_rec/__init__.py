from pathlib import Path
from typing import Optional

import streamlit as st
import streamlit.components.v1 as components

# Tell streamlit that there is a component called auto_audio_rec,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
	"auto_audio_rec", path=str(frontend_dir)
)

# Create the python function that will be called
def auto_audio_rec(
    label: str,
    value: Optional[str] = "",
    key: Optional[str] = None,
):
    """
    Create a Streamlit text input that returns the value whenever a key is pressed.
    """
    component_value = _component_func(
        label=label,
        value=value,
        key=key,
        default=value
    )


    return component_value


def main():
    st.write("## Example")
    value = auto_audio_rec("This is a label!")

    st.write(value)


if __name__ == "__main__":
    main()
