import streamlit as st
from typing import Callable, Any, Optional
from functools import wraps

class LoadingHandler:
    @staticmethod
    def with_loading(message: str = "Processing..."):
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                with st.spinner(message):
                    try:
                        result = func(*args, **kwargs)
                        return result
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        return None
            return wrapper
        return decorator

    @staticmethod
    def loading_button(
        label: str,
        key: str,
        callback: Callable,
        loading_text: str = "Processing...",
        success_text: str = "Done!",
        args: tuple = (),
        kwargs: dict = {}
    ) -> Optional[Any]:
        if st.button(label, key=key):
            with st.spinner(loading_text):
                try:
                    result = callback(*args, **kwargs)
                    st.success(success_text)
                    return result
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    return None
        return None