import websocket
import time
 
ws = websocket.WebSocket()
ws.connect("ws://192.168.4.1/")
 
i = 0
nrOfMessages = 30
 
while i<nrOfMessages:
    ws.send("Soft AP mode: message nr " + str(i))
    result = ws.recv()
    print(result)
    i=i+1
    #time.sleep(1)
 
ws.close()
