import os
import openai
import tiktoken


from flask import request

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


sentry_sdk.init(
    dsn=os.environ['SENTRY_DSN'], integrations=[FlaskIntegration()]
)


app = Flask(__name__)

openai.organization = os.environ['open_ai_organization']
openai.api_key = os.environ['open_ai_api_key']

model_summary = os.environ['model_summary']
static_text_summary = os.environ['static_text_summary']

model_loop = os.environ['model_loop']
static_text_loop = os.environ['static_text_loop']


def calculate_tokens(text, model):
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))

@app.route('/')
def home():
    return 'Hello, World!'

@app.route("/summary", methods = ['POST'])
def extract_summary():

    contract_text = request.form.get('contract_text', None)

    if contract_text is None:
        return 'Error 101'

    completion_text = contract_text + static_text_summary
    
    total_tokens = 4096
    response_tokens = total_tokens - calculate_tokens(completion_text, model_summary)
    

    r = openai.Completion.create(
      model=model_summary,
      prompt=completion_text,
      max_tokens=response_tokens,
      temperature=0
    )
    
    choices = r.get('choices', [])
    
    if len(choices) > 0:
        summary_text = choices[0].get('text', '')

    return summary_text


@app.route("/loop_holes", methods = ['POST'])
def extract_summary():

    contract_text = request.form.get('contract_text', None)

    if contract_text is None:
        return 'Error 101'

    completion_text = contract_text + static_text_loop
    
    total_tokens = 4096
    response_tokens = total_tokens - calculate_tokens(completion_text, model_loop)
    

    r = openai.Completion.create(
      model=model_loop,
      prompt=completion_text,
      max_tokens=response_tokens,
      temperature=0
    )
    
    choices = r.get('choices', [])
    
    if len(choices) > 0:
        summary_text = choices[0].get('text', '')

    return summary_text
