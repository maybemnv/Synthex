from streamlit.testing.v1 import AppTest
import pytest
from unittest.mock import patch, MagicMock
import streamlit as st

class TestFrontend:
    @pytest.fixture
    def app(self):
        if 'history' not in st.session_state:
            st.session_state.history = []
        return AppTest.from_file("app.py")

    @pytest.fixture
    def mock_api(self):
        with patch('requests.post') as mock_post:
            yield mock_post

    def test_home_page_load(self, app):
        app.run()
        markdown_texts = [m.value for m in app.markdown]
        assert any('Synthex' in text for text in markdown_texts)
        assert app.sidebar is not None

    def test_generate_page(self, app, mock_api):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {"generated_code": "def hello():\n    print('Hello World')"}
        }
        mock_api.return_value = mock_response

        app.run()
        app.sidebar.selectbox("Mode").select("Generate").run()
        app.text_area("What would you like me to create?").input("Create hello world").run()
        app.selectbox("Programming Language").select("Python").run()
        app.form_submit_button("Generate Code").click().run()
        mock_api.assert_called_once()
        assert any("Hello World" in c.value for c in app.code)

    def test_explain_page(self, app, mock_api):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {"explanation": "This code prints Hello World"}
        }
        mock_api.return_value = mock_response

        app.run()
        app.sidebar.selectbox("Mode").select("Explain").run()
        app.text_area("Enter your code").input("print('Hello World')").run()
        app.select_slider("Explanation Detail Level").set_value("Intermediate").run()
        app.form_submit_button("Explain Code").click().run()
        mock_api.assert_called_once()
        markdown_texts = [m.value for m in app.markdown]
        assert any("This code prints" in text for text in markdown_texts)

    def test_learn_page(self, app, mock_api):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "data": {"content": "Learning content here"}
        }
        mock_api.return_value = mock_response

        app.run()
        app.sidebar.selectbox("Mode").select("Learn").run()
        app.selectbox("Main Topic").select("Data Structures").run()
        mock_api.assert_called_once()
        markdown_texts = [m.value for m in app.markdown]
        assert any("Learning content" in text for text in markdown_texts)

    def test_error_handling(self, app, mock_api):
        mock_api.side_effect = Exception("API Error")
        app.run()
        app.sidebar.selectbox("Mode").select("Generate").run()
        app.text_area("What would you like me to create?").input("Test").run()
        app.form_submit_button("Generate Code").click().run()
        assert any("Error" in e.value for e in app.error)

    def test_session_state(self, app):
        st.session_state.history = [{
            "mode": "Generate",
            "timestamp": "2024-05-11 10:00:00",
            "language": "Python",
            "code": "print('test')"
        }]
        app.run()
        markdown_texts = [m.value for m in app.markdown]
        assert any("Generate" in text for text in markdown_texts)

    def test_ui_components(self, app):
        app.run()
        css_texts = [m.value for m in app.markdown]
        assert any("--primary" in text for text in css_texts)
        assert any("--secondary" in text for text in css_texts)
        assert app.sidebar is not None

    def test_form_validation(self, app):
        app.run()
        app.sidebar.selectbox("Mode").select("Generate").run()
        app.text_area("What would you like me to create?").input("").run()
        app.form_submit_button("Generate Code").click().run()
        assert any("Please provide" in w.value for w in app.warning)

    def test_all_modes(self, app):
        app.run()
        # Replace with your actual sidebar label!
        mode_label = "Select a mode:"  # <-- update this to match your app.py
        for mode in ["Home", "Generate", "Explain", "Learn"]:
            app.sidebar.selectbox(mode_label).select(mode).run()
            markdown_texts = [m.value for m in app.markdown]
            assert any(mode.lower() in text.lower() for text in markdown_texts)