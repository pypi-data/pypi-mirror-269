import requests


def bloom_ans(prompt, api='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'):
    question = ('Someone just said ' + str(prompt) + ". Here's my answer to that: ")

    API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom"
    headers = {"Authorization": f"Bearer {api}"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    output = query({
        "inputs": str(question),
    })

    output = str(output)

    output = output.replace("[{'generated_text': ", '')
    output = output.replace('"', '')
    output = output.replace('}]', '')

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    output = query({
        "inputs": str(output),
    })

    output = [output[0]]
    output = str(output)
    output = output.replace("[{'generated_text': ", '')
    output = output.replace('"', '')
    output = output.replace('}]', '')
    output = str(output.replace(str(question), ''))
    output = str(output.split('.', 1))
    output = output.replace("[' ", '')
    output = output.replace("', '']", '')
    output = (str(output) + '.')
    output = output.replace("'", '')
    output = output.replace('"', '')
    output = output.replace("[", '')
    output = output.replace("]", '')
    output = output.replace(".", '')
    output = output.replace('fuck', 'frick')
    output = output.replace('Fuck', 'Frick')
    return output


def bloom_gen(prompt, api='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'):
    question = prompt

    API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom"
    headers = {"Authorization": f"Bearer {api}"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    output = query({
        "inputs": str(question),
    })

    output = str(output)

    output = output.replace("[{'generated_text': ", '')
    output = output.replace('"', '')
    output = output.replace('}]', '')

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    output = query({
        "inputs": str(output),
    })

    output = [output[0]]
    output = str(output)
    output = output.replace("[{'generated_text': ", '')
    output = output.replace('"', '')
    output = output.replace('}]', '')
    output = str(output.replace(str(question), ''))
    output = str(output.split('.', 1))
    output = output.replace("[' ", '')
    output = output.replace("', '']", '')
    output = (str(output) + '.')
    output = output.replace("'", '')
    output = output.replace('"', '')
    output = output.replace("[", '')
    output = output.replace("]", '')
    output = output.replace(".", '')
    output = output.replace('fuck', 'frick')
    output = output.replace('Fuck', 'Frick')
    return output
