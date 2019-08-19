import json
from sklearn.externals import joblib

model_name = 'Model_1566096478.5759013.joblib'
model = joblib.load(model_name)

def predict(event, context):
    body = {
        "message": "OK",
    }

    params = event['queryStringParameters']

    medInc = float(params['medInc']) / 100000
    houseAge = float(params['houseAge'])
    aveRooms = float(params['aveRooms'])
    aveBedrms = float(params['aveBedrms'])
    population = float(params['population'])
    aveOccup = float(params['aveOccup'])
    latitude = float(params['latitude'])
    longitude = float(params['longitude'])

    inputVector = [medInc, houseAge, aveRooms, aveBedrms, population, aveOccup,
            latitude, longitude]
    data = [inputVector]

    predictedPrice = model.predict(data)[0] * 100000 #1 usd
    predictedPrice = round(predictedPrice, 2)
    body['predictedPrice'] = predictedPrice

    response = {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers" : {
            "Access-Control-Allow-Origin": '*'
            }
    }

    return response

def do_main():
    event = {
        'queryStringParameters': {
            'medInc' : 2000000,
            'houseAge' : 10,
            'aveRooms' : 4,
            'aveBedrms' : 1,
            'population' : 800,
            'aveOccup' : 3,
            'latitude' : 37.54,
            'longitude' : -121.72
            }
        }

    response = predict(event, None)
    body = json.loads(response['body'])
    print('Price:', body['predictedPrice'])

    with open('event.json','w') as event_file:
        event_file.write(json.dumps(event))

#do_main()


