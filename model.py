import json
import uuid
import requests
import time

streaming_result = {
    "choices": [
        {
            "delta": {
                "content": "",
            }
        }
    ]
}

def find_existing_library(api_key, document_url):
    res = requests.get('https://aiproxy.io/api/library/list', headers={"Api-Key": api_key})
    libraries = res.json().get('data', {}).get('records', [])
    for library in libraries:
        library_id = library['id']
        res = requests.get('https://aiproxy.io/api/library/listDocument', headers={"Api-Key": api_key},
                           params={'libraryId': library_id})
        documents = res.json().get('data', {}).get('records', [])
        for doc in documents:
            if doc['url'] == document_url:
                return library_id
    return None

def chat_completions(api_key, question, document_url):
    yield f'data: {json.dumps(streaming_result)}\n\n'
    library_id = find_existing_library(api_key, document_url)
    if library_id:
        yield f'data: {json.dumps(streaming_result)}\n\n'
        print(f"Existing library {library_id} found.")
        print(f"Document {document_url} already in library {library_id}.")
    else:
        yield f'data: {json.dumps(streaming_result)}\n\n'
        res = requests.post('https://aiproxy.io/api/library/create', headers={"Api-Key": api_key},
                            json={'libraryName': str(uuid.uuid4()), 'description': document_url})
        library_id = res.json().get('data')
        print(f"New library {library_id} has been created.")
        requests.post('https://aiproxy.io/api/library/document/createByUrl', headers={"Api-Key": api_key},
                      json={'refresh': True, 'libraryId': library_id, 'urls': [document_url]})
        print(f"Document {document_url} has been added to library {library_id}.")

        while True:
            res = requests.get('https://aiproxy.io/api/library/listDocument', headers={"Api-Key": api_key},
                               params={'libraryId': library_id})
            if res.json()['data']['records'][0]['statusCode'] == 'Completed':
                break
            yield f'data: {json.dumps(streaming_result)}\n\n'
            time.sleep(0.5)

    res = requests.post('https://api.aiproxy.io/api/library/ask', headers={'Authorization': f'Bearer {api_key}'},
                        json={'model': 'gpt-3.5-turbo', 'query': question, 'libraryId': library_id, 'stream': True})
    print(streaming_result)
    parsed_data = {}
    for R in res.iter_lines():
        if R:
            rep = R
            parsed_data = json.loads(rep[5:])
            try:
                content = parsed_data['content']
            except:
                streaming_result["choices"][0]["delta"]["content"] = ""
                break
            streaming_result["choices"][0]["delta"]["content"] = content
            print(streaming_result)
            yield f'data: {json.dumps(streaming_result)}\n\n'

