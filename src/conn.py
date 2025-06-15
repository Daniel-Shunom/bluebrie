import streamlit as st
import requests

class LentilConnection:
    def __init__(self, url: str, db_url: str):
        self.url: str = url
        self.db_url = db_url
        self.lntl_conn = st.connection(url)
        self.db_conn = st.connection(db_url, type="sql")

    def start_session(self) -> str | requests.Response: 
        payload: dict[str, str] = {
            "username": f"",
            "password": f"",
        }
        response: requests.Response = requests.post(self.url, json=payload)
        
        match response.status_code:
            case 200 | 202: return response
            case 400: return "bad request"
            case 500: return "server error"
            case _: return "something went wrong"
    
    def fetch_profile(self) -> str | requests.Response:
        payload = {
            "username": f"",
            "password": f"",
        }
        response: requests.Response = requests.get(self.url %"", json=payload)
        
        match response.status_code:
            case 200 | 202: return response
            case 400: return "bad request"
            case _: return "something went wrong"
    
    def send_message(self, msg: str) -> str | requests.Response:
        payload = {"": "", "": ""}
    

