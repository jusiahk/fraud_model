import logging
import azure.functions as func
import pandas as pd
import joblib
import json


#Load from file
rfc = joblib.load('fraud_model.sav')

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    data = req.get_json()
    data = json.loads(data)

    if data is not None:

        response = []
        for i in range(len(data)):

            data_row = data[i]
            pred_df = pd.DataFrame([data_row])
            pred_label = rfc.predict(pred_df)[0]
            pred_probs = rfc.predict_proba(pred_df)[0]

            results_dict = {
                'pred_label': int(pred_label),
                'pred_prob_0': pred_probs[0],
                'pred_prob_1': pred_probs[1]
            }

            response.append(results_dict)

        return json.dumps(response)

    import MySQLdb

def dbconnect():
    try:
        db = MySQLdb.connect(
            host='localhost',
            user='root',
            passwd='password',
            db='Fraud'
        )
    except Exception as e:
        sys.exit("Can't connect to database")
    return db

def insertDb():
    try:
        db = dbconnect()
        cursor = db.cursor()
        cursor.execute("""
        INSERT INTO Results(FraudResult) \
        VALUES (%s) """, (data))
        cursor.close()
 
    else:
        return func.HttpResponse(
             "Please pass a properly formatted JSON object to the API",
             status_code=400
        )