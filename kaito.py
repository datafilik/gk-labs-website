########################################################################################
# KAITO - Utility for sourcing knowledge using AI.
#         Base functions and utlities for AI assistant KAITO.
########################################################################################
import os
import openai
from pygpt4all import GPT4All
# from pygpt4all.models.gpt4all import GPT4All
from gtts import gTTS
from dotenv import load_dotenv

# load environment variable from .env file
load_dotenv()

# get OpenAI API key
openai.api_key = os.environ['OPENAI_API_KEY']
# get eleven labs API key
elevenlabs_api_key = os.environ['ELEVENLABS_API_KEY']
# get fastsppech API token from huggingface
hf_api_token = os.environ['HF_API_TOKEN']

# configure system response context and keep track of conversation thread
msg_thread = [
  {
    "role":
    "system",
    "content":
    "You are a very knowlegable assistant called Kaito. Explain concepts from first principles."
  },
]


#------------------------------------------------------------------------------------
# function for transcribing sound from file to text
#------------------------------------------------------------------------------------
# OpenAI ASR
def whisper_transcribe(file_name):
  audio_data = open(file_name, "rb")
  transcript = openai.Audio.transcribe("whisper-1", audio_data)
  return transcript["text"]


#------------------------------------------------------------------------------------
# functions using OpenAI API to generate reponse to user query
#------------------------------------------------------------------------------------
def get_prompt_response(prompt):
  response = openai.Completion.create(engine="text-davinci-003",
                                      prompt=prompt,
                                      max_tokens=4000,
                                      n=1,
                                      stop=None,
                                      temperature=0.5)
  return response["choices"][0]["text"]


def get_chat_response(messages):
  response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                          messages=messages)
  return response["choices"][0]["message"]["content"]


# fetches updated transcript for each session
def get_transcript(msg_thread):
  # format message thread
  chat_transcript = ""
  for message in msg_thread:
    if message["role"] != "system":
      if message["role"] == "user":
        message["role"].replace("user", "You")

      if message["role"] == "assistant":
        message["role"].replace("user", "Kaito")

      chat_transcript += message["role"] + \
          ": " + message["content"] + "\n\n"

  # return formatted_chat_transcript
  return chat_transcript


#------------------------------------------------------------------------------------
#functions using PyGPT4All API to generate reponse to user query
#------------------------------------------------------------------------------------
def get_gpt4all_response(prompt):
  model = GPT4All(
    'http://gpt4all.io/models/ggml-gpt4all-l13b-snoozy.bin',  #'/static/ggml-gpt4all-l13b-snoozy.bin',
    prompt_context=
    "You are a very knowlegable assistant called Kaito. Explain concepts from first principles.",
    prompt_prefix="\nYou: ",
    prompt_suffix="\nKaito: ")

  response = ""
  for resp_token in model.generate(prompt):
    #print(resp_token, end='', flush=True)
    response += resp_token
  return response


#------------------------------------------------------------------------------------
# functions for text-to-speech synthesis
#------------------------------------------------------------------------------------
# Google translate TTS. TODO issues with incomplete and slow text read out
def gTranslate_tts(text, audio_out_path):
  gtts_eng = gTTS(text, lang="en", tld="co.uk")
  gtts_eng.save(audio_out_path)


#------------------------------------------------------------------------------------------
# main KAITO routine for processing user input query
#------------------------------------------------------------------------------------------
def process_prompt(audio_in, text_in, audio_out):
  global msg_thread
  transcript = ''

  # transcribe audio prompt to text using whisper
  if bool(audio_in) == True:
    transcript = whisper_transcribe(audio_in)
  # collect text prompt
  if bool(text_in) == True:
    transcript = text_in[0]

  if transcript != '':
    # add transcribed query to conversation thread
    msg_thread.append({"role": "user", "content": transcript})

    # get GPT-3 response
    latest_resp = get_chat_response(msg_thread)

    # read out response
    gTranslate_tts(latest_resp, audio_out)

    # add GPTS-3 response  to thread
    msg_thread.append({"role": "assistant", "content": latest_resp})

  # show latest transcript
  return get_transcript(msg_thread)  #audio_out_name
