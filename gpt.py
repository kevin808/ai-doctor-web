import os
import openai

# openai.api_type = "azure"
# openai.api_base = os.getenv("AZURE_OPENAI_API_HOST")
# openai.api_version = "2023-03-15-preview"
# openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")
from urllib import parse
import requests, json

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

def get_ocr_result(file_base64):
        
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/medical_report_detection?access_token=" + get_access_token()
    
    payload='image=' + parse.quote(file_base64)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    try:
        result = simplify_info(response.text)
    except Exception as e:
        result = str(e)
    return result
    

def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))

def simplify_info(info):
    data_dict = json.loads(info)
    result_dict = {}
    for item in data_dict['words_result']['Item']:
        for sub_item in item:
            if sub_item['word_name'] == '项目名称':
                key = sub_item['word']
            elif sub_item['word_name'] == '结果':
                value = sub_item['word']
        result_dict[key] = value
    return str(result_dict)

def get_bot_response(message):
    response_text = 'No result'
    try:
        completion = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {'role': 'system', 'content': 'You are a professional general practitioner, skilled in diagnosing various diseases. When encountering uncertain problems, you must indicate your uncertainty. Based on the information provided, you give your diagnostic opinion, and each response must be within 50 words.'},
            {'role': 'user', 'content': message}
        ],
        temperature = 0  
        )
        response_text = completion['choices'][0]['message']['content']

    except Exception as e:
        response_text = str(e)

    return response_text

# For Azure
# def get_bot_response(message):
# #Note: The openai-python library support for Azure OpenAI is in preview.
#     response_text = 'No result'
#     try:
#         response = openai.ChatCompletion.create(
#             engine="gpt-35-turbo",
#             messages = message,
#             temperature=1.0,
#             max_tokens=100,
#             top_p=0.95,
#             frequency_penalty=0,
#             presence_penalty=0,
#             stop=None)
#         response_text = response['choices'][0]['message']['content']
#     except Exception as e:
#         response_text = str(e)
#     # Return the formatted response text
#     return response_text
