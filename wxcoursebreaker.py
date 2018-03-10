from flask import Flask,request
import ssl
import coursespy


app = Flask(__name__)
@app.route('/')
def hello():
    return 'Hello World! 你好'
@app.route('/test')
def test():
    return 'Hello World! 你好'

@app.route('/w')
def coursebreak():
    ID=request.args.get('ID')
    pwd=request.args.get('passwd')
    if((len(ID)>5)&(len(pwd)>5)):
           result =str(coursespy.startspy(ID,pwd)).replace("'",'"')
           return result
    else:
           return "error"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10066)
