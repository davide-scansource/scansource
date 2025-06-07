import json
import http.client
import urllib
import datetime

def get_data(url):
  parsed_url = urllib.parse.urlparse(url)
  hostname = parsed_url.netloc
  path = parsed_url.path
  if parsed_url.scheme == 'https':
      conn = http.client.HTTPSConnection(hostname)
  else:
      conn = http.client.HTTPConnection(hostname)
  conn.request("GET", path)
  response = conn.getresponse()

  if response.status == 200:
      data = response.read()
      conn.close()
      return data

  conn.close()

  raise Exception("Data cannot be retrieved")
    

def handler(event, context):
  try:
    print('Lambda2 called. Version 1.0.0')
    current_datetime = datetime.datetime.now()
    url = f"https://byabbe.se/on-this-day/{current_datetime.month}/{current_datetime.day}/events.json"
    data = get_data(url)

    return {
      'headers': { 
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
      'statusCode': 200,
      'body': data,
    }
  except Exception as e:
    # Log error for later debugging
    print(e)
    return {
      'headers': { "Content-Type": "application/json" },
      'statusCode': 502,
      'body': json.dumps({ "error": "Data cannot be retrieved" }),
    }
