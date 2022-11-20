import os
import joblib
from flask import Flask, jsonify, render_template, request, url_for

model = joblib.load('model/engine_model.pkl')
app = Flask(__name__)

@app.route('/')
def load():
    return render_template('Manual_predict.html')

@app.route('/result',methods=['POST'])
def result():
    pred_vals = [[float(x) for x in request.form.values()]]
    print(pred_vals)
    pred = model.predict(pred_vals)
    if(pred==0):
        pred_text = "No failure expected within 30 days"
        return render_template('Predicton_no_failure.html',prediction_text_no_failure = pred_text)
    else:
        pred_text = "Maintenance Required! Expected a failure within 30 days"
        return render_template('Prediction_failure.html',prediction_text_failure = pred_text)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__== '__main__':
    app.run(debug=True)