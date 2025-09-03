
from flask import Flask, jsonify, request
import json
app = Flask(__name__)

# Een eenvoudige route die 'Hallo, Wereld!' retourneert


# Een route die een som van twee getallen retourneert
@app.route('/get_chat', methods=['GET'])
def retrun_chat():
    data = request.get_json()
    sender_id = data.get("id", 0)
    
    with open('testfile.json', 'r') as file:
        json_c = json.load(file)
        
    if sender_id not in json_c["permissions"]["allowed_ids"]:
               return jsonify({'result': {'chat':{'messages':['\033[31mAction NOT allowed\033[0m'],'senders':['\033[31m\033[0m']}}})

    # messages_and_senders = {
    #     "chat":{
    #         "messages": data["chat"]["messages"],
    #         "senders": data["chat"]["senders"]
    #     },
    #     "color": {}
    # }
    return jsonify({'result': json_c})

@app.route("/send_message", methods=["POST"])
def receive_message():
   data = request.get_json()
   message = data.get("message", 0)
   if message == "":
       return jsonify({'result': '\033[31m  ! Empty message NOT send\033[0m', "corr":True})
       
   sender_id = data.get("id", 0)


   with open('testfile.json', 'r') as file:
        content_json = json.load(file)

   if sender_id not in content_json["permissions"]["allowed_ids"]:
       return jsonify({'result': '\033[31m  ! Action NOT allowed\033[0m', "corr":False})
   # # content_json["messages"].append("message")
   # # content_json["senders"].append("sender_id")
   content_json["chat"]["messages"].append(message)
   content_json["chat"]["senders"].append(sender_id)
   #
   with open('testfile.json', 'w') as file:
       json.dump(content_json, file,indent=4)

   
   return jsonify({'result':'\033[32mSuccess\033[0m', "corr":True})






if __name__ == '__main__':
    app.run(debug=True)
