from client import server_client
id="0"
print(server_client.collections["WaitlistProducts"].documents[id].delete())