import ollama

from .instrument import metrics

@metrics.track
def llama3_text(prompt, system='', temperature=0.0, topP=1.0, model='llama3'):
    response = ollama.generate(model=model, prompt=prompt, system=system, 
                               options={
                                   "temperature": temperature,
                                   "top_p": topP
                               })
    return response['response']

@metrics.track
def llama2_text(prompt, system='', temperature=0.0, topP=1.0, model='llama2'):
    response = ollama.generate(model=model, prompt=prompt, system=system, 
                               options={
                                   "temperature": temperature,
                                   "top_p": topP
                               })
    return response['response']

@metrics.track
def mistral_text(prompt, system='', temperature=0.0, topP=1.0, model='mistral'):
    response = ollama.generate(model=model, prompt=prompt, system=system, 
                               options={
                                   "temperature": temperature,
                                   "top_p": topP
                               })
    return response['response']

@metrics.track
def codellama_text(prompt, system='', temperature=0.0, topP=1.0, model='codellama'):
    response = ollama.generate(model=model, prompt=prompt, system=system, 
                               options={
                                   "temperature": temperature,
                                   "top_p": topP
                               })
    return response['response']

@metrics.track
def gemma_text(prompt, system='', temperature=0.0, topP=1.0, model='gemma'):
    response = ollama.generate(model=model, prompt=prompt, system=system, 
                               options={
                                   "temperature": temperature,
                                   "top_p": topP
                               })
    return response['response']

def text(prompt, system='', temperature=0.0, topP=1.0, model='llama3'):
    match model:
        case 'gemma':
            return gemma_text(prompt, system, temperature, topP)
        case 'llama3':
            return llama3_text(prompt, system, temperature, topP)
        case 'llama2':
            return llama2_text(prompt, system, temperature, topP)
        case 'codellama':
            return codellama_text(prompt, system, temperature, topP)
        case 'mistral':
            return mistral_text(prompt, system, temperature, topP)
        case _:
            return 'Please specify a valid model name'
