from openai import OpenAI
import time
from utils import load_json_file
from gtts import gTTS

assJson = load_json_file("config/assistanceConfig.json")
mediaJson = load_json_file("config/mediaPath.json")

class ai:
    def __init__(self):
        self.client_ai = OpenAI(api_key=assJson["apikey"])
        self.name = 'mary'
        self.ass_id = assJson["ai"][self.name]["id"]
        self.voice = assJson["ai"][self.name]["voice"]


    def change_ai(self, new_ai_name):
        self.name = new_ai_name
        self.ass_id = assJson["ai"][new_ai_name]["id"]
        self.voice = assJson["ai"][new_ai_name]["voice"]

    def gpt(self,input, thread=False):

        if thread is False:
            thread = self.client_ai.beta.threads.create()
                
        self.client_ai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=input)

        run = self.client_ai.beta.threads.runs.create(
            thread_id=thread.id,
            #assistant_id="asst_QK68lW9w7EZtGEawePquMC0U",
            assistant_id=self.ass_id,
            )

        while 1:
            run = self.client_ai.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
                )
            if run.completed_at is not None:
                messages = self.client_ai.beta.threads.messages.list(
                    thread_id=thread.id
                    )
                return messages.data[0].content[0].text.value,thread
            time.sleep(2)


    def answer(self, message):
        #tts = gTTS(text=message, lang="th")
        #tts.save(self.media_json["answer_voice"])

        response = self.client_ai.audio.speech.create(
            model="tts-1",
            voice=self.voice,
            input=message,
        )
        response.stream_to_file(mediaJson["answer"])


       

    