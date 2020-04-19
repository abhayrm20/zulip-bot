import pprint
import zulip
import sys

from storeloc import Storeloc
from chatterbot import ChatBot
from covid import Covid


p = pprint.PrettyPrinter()
BOT_MAIL = "GoKhareedo-bot@nullcrew.zulipchat.com"


class ZulipBot(object):
    def __init__(self):
        self.client = zulip.Client(site="https://nullcrew.zulipchat.com/api/")
        self.storeloc = Storeloc()
        self.covid = Covid()
        self.chatbot = ChatBot("GoKhareedo", trainer='chatterbot.trainers.ChatterBotCorpusTrainer')

        #Uncommented only for the first run!
        #self.chatbot.train("chatterbot.corpus.english")


        print("Initialisation Completed")
        self.subkeys = ["help", "loc", "covid"]

    def subscribe_all(self):
        json = self.client.get_streams()["streams"]
        streams = [{"name": stream["name"]} for stream in json]
        self.client.add_subscriptions(streams)

    def process(self, msg):
        content = msg["content"].split()
        sender_email = msg["sender_email"]
        ttype = msg["type"]
        stream_name = msg['display_recipient']
        stream_topic = msg['subject']

        print(content)

        if sender_email == BOT_MAIL:
            return

        print("Sucessfully heard.")

        if content[0] == "Gokhareedo" or content[0] == "@**GoKhareedo**":
            try:
                if content[1].lower() == "help":
                    self.client.send_message({
                        "type": "stream",
                        "subject": msg["subject"],
                        "to": msg["display_recipient"],
                        "content": "Hey there! How are you doing?\n"
                                   "Do you need help?\n"
                                   "We have three features:\n"
                                   "1. Nearby Store: It will show the nearby store to choose from for the grocery!\nUsage: @Gokhareedo loc <any location>\nExample: @GoKhareedo loc Bangalore\n"
                                   "2. Live Covid Cases: It will show the latest nCovid stats from MoH!\nUsage: @GoKhareedo covid <State-Name>\nExample: @GoKhareedo covid goa\n"
                                   "3. NLP chat with bot-assistant!\n Usage: @GoKhareedo <your-expression>\nExample: @GoKhareedo Hi"

                    })

                elif content[1].lower() == 'loc':
                    x = content[2:]
                    x = " ".join(x)

                    quote_data = self.storeloc.storeloc(x)
                    self.client.send_message({
                        "type": "stream",
                        "to": stream_name,
                        "subject": stream_topic,
                        "content": quote_data
                    })

                elif content[1].lower() == 'covid':
                    x = content[2:]
                    x = " ".join(x)
                    print(x)
                    quote_data = self.covid.covid(x)
                    self.client.send_message({
                        "type": "stream",
                        "to": stream_name,
                        "subject": stream_topic,
                        "content": quote_data
                    })



                elif content[1] not in self.subkeys:
                    ip = content[1:]
                    ip = " ".join(ip)
                    message = self.chatbot.get_response(ip).text
                    self.client.send_message({
                        "type": "stream",
                        "subject": msg["subject"],
                        "to": msg["display_recipient"],
                        "content": message
                    })

                else:
                    self.client.send_message({
                        "type": "stream",
                        "subject": msg["subject"],
                        "to": msg["display_recipient"],
                        "content": "Please don't leave the parameter blank!"
                    })

            except:
                self.client.send_message({
                    "type": "stream",
                    "subject": msg["subject"],
                    "to": msg["display_recipient"],
                    "content": "Please don't leave the parameter blank!"
                })
                main()



        elif "GoKhareedo" in content and content[0] != "GoKhareedo":
            self.client.send_message({
                "type": "stream",
                "subject": msg["subject"],
                "to": msg["display_recipient"],
                "content": "Hey there! :blush:"
            })

        else:
            return


def main():
    bot = ZulipBot()
    bot.client.call_on_each_message(bot.process)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nThanks for using GoKhareedo Assistant Bot.\n Stay Safe!")
        sys.exit(0)
