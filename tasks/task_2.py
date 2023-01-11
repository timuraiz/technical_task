from fastapi import FastAPI
from urllib import parse

app = FastAPI()


@app.post('/encode')
def encode_url(decoded_url: str):
    params = {'q': 'Python URL encoding', 'as_sitesearch': decoded_url}
    return {'result': parse.urlencode(params)}


