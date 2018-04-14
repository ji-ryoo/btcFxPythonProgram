#coding: UTF-8
import pinbaralert as pb
import requests
import yaml



def line(Me):

    yaml_dict = yaml.load(open('./etc.yaml').read())
    token= yaml_dict['line_notify_token']
    line_notify_token = token #先程発行したコードを貼ります
    line_notify_api = 'https://notify-api.line.me/api/notify'
    message = '\n' + Me
    #変数messageに文字列をいれて送信します トークン名の隣に文字が来てしまうので最初に改行しました
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}
    line_notify = requests.post(line_notify_api, data=payload, headers=headers)



pinbar = pb.Pinbar(3600)
pinbar.printAllOhlcs()
if(pinbar.pinbarJudge()==True):
    print("pinbar!!")
    line(str(pinbar.outJudgeTime())+"\n[bfBTCFX-1時間足]\nピンバー出現！")
else:
    print("no!")

print(pinbar.outJudgeTime())
