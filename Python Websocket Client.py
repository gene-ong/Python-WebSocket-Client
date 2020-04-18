import websocket
 
ws = websocket.WebSocket()
ws.connect("ws://192.168.1.103/test")
#ws.send('hello')
ws.send_binary([100, 100, 100])

ws.close()
