
def chatgpt_basic_conversation(
        api_key: str, prompts: list,
        model: str = 'gpt-3.5-turbo', base_url: str = None
) -> str:
    """chatgpt最基本的对话，如果需要使用别的服务提供商，注意修改base_url

    Args:
        api_key (str): _description_
        prompts (list): e.g [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Hello!"}]
        model (str, optional): _description_. Defaults to 'gpt-3.5-turbo'.
        base_url (str, optional): _description_. Defaults to None.

    Returns:
        str: _description_
    """

    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(model=model, messages=prompts)
    return completion.choices[0].message.content


def text_2_audio_openai(
        api_key: str, text: str, audio_file_path: str = 'speech.mp3',
        voice: str = 'echo', model: str = 'tts-1', base_url: str = None
) -> None:
    """使用openai api从文字生成语音，如果需要使用别的服务提供商，注意修改base_url

    Args:
        api_key (str): _description_
        text (str): _description_
        audio_file_path (str, optional): _description_. Defaults to 'speech.mp3'.
        voice (str, optional): [alloy, echo, fable, onyx, nova, shimmer]. Defaults to 'echo'.
        model (str, optional): _description_. Defaults to 'tts-1'.
        base_url (str, optional): _description_. Defaults to None.
    """
    from openai import OpenAI
    client = OpenAI(api_key=api_key, base_url=base_url)
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text
    )

    # response.stream_to_file(speech_file_path)
    response.write_to_file(audio_file_path)


def audio_2_text_openai(
        api_key: str, audio_file_path: str,
        model: str = 'whisper-1', base_url: str = None
) -> str:
    """使用openai api从语音生成文字，如果需要使用别的服务提供商，注意修改base_url

    Args:
        api_key (str): _description_
        audio_file_path (str): _description_
        model (str, optional): _description_. Defaults to 'whisper-1'.
        base_url (str, optional): _description_. Defaults to None.

    Returns:
        str: _description_
    """
    from openai import OpenAI
    client = OpenAI(api_key=api_key, base_url=base_url)

    audio_file = open(audio_file_path, "rb")
    transcription = client.audio.transcriptions.create(
        model=model,
        file=audio_file
    )
    return transcription.text


def get_pandasai_agent(data, openapi_key: str = None, config: dict = None):
    """获得pandas-ai库中的Agent对象: https://docs.pandas-ai.com/en/latest/
        Agent.chat("XXX") or 
        Agent.clarification_question("XXX") or 
        Agent.explain() or 
        Agent.rephrase_query("XXX")


    Args:
        openapi_key (str): 如果不传，使用pandasbi的免费key
        data (_type_): Dataframe or [Dataframe1, Dataframe2, ...]
        config (dict, optional): https://docs.pandas-ai.com/en/latest/getting-started/#config. Defaults to None.

    Returns:
        _type_: pandasai.Agent
    """
    import os

    from pandasai import Agent
    from pandasai.llm import OpenAI

    if not openapi_key:
        os.environ["PANDASAI_API_KEY"] = "$2a$10$AjBzJYa7M.AV8wRfcUisme4ARgSUVF.ooDDIn4MS4S52Umd7N6O12"
        if not config:
            config = {
                "save_logs": False,
                "save_charts": False,
                "verbose": False,
                "enable_cache": False,
                "open_charts": True
            }
    else:
        llm = OpenAI(api_token=openapi_key)
        if not config:
            config = {
                "llm": llm,
                "save_logs": False,
                "save_charts": False,
                "verbose": False,
                "enable_cache": False,
                "open_charts": True
            }
    agent = Agent(data, config)
    return agent
