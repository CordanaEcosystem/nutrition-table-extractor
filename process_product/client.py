import typesense
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
                "host": "13.232.135.140",
              
                "port": "8108",  # For Typesense Cloud use 443
                "protocol": "http",  # For Typesense Cloud use https
            }
        ],
        "api_key": "fQqH5u29cQZPHUYQ8FeVp8FIOVWfKmHiH368hImsqTdfScwS",
     
        "connection_timeout_seconds": 200,
    }
)


