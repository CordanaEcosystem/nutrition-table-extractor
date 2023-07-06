import typesense

from dotenv import load_dotenv
import os

load_dotenv()
TYPESENSE_API_KEY = os.getenv("TYPESENSE_API_KEY")
schema = {
    "name": "WaitlistProducts",
    "fields": [
        {"name": "fdcId", "type": "string"},
         {"name": "addedBy", "type": "string"},
        {"name": "topThree", "type": "string[]"},
        {"name": "dataType", "type": "string","sort":True},
        {"name": "description", "type": "string", "token_separators": [",", "."]},

        
        {"name": ".*", "type": "auto"},
    ],
}
local_client = typesense.Client(
    {
        "nodes": [
            {
                
                'host': 'localhost',  # For Typesense Cloud use xxx.a1.typesense.net
                "port": "8108",  # For Typesense Cloud use 443
                "protocol": "http",  # For Typesense Cloud use https
            }
        ],
   
          'api_key': 'xyz',
        "connection_timeout_seconds": 200,
    }
)
server_client = typesense.Client(
    {
        "nodes": [
            {
                
                'host': 'localhost',  # For Typesense Cloud use xxx.a1.typesense.net
                "port": "8108",  # For Typesense Cloud use 443
                "protocol": "http",  # For Typesense Cloud use https
            }
        ],
   
          'api_key': TYPESENSE_API_KEY,
        "connection_timeout_seconds": 200,
    }
)


