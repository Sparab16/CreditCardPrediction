from flask import Flask, request, render_template, Response
from flask_cors import CORS, cross_origin
from TrainValidation.train_validation import Train_Validation
from PredictionValidation.prediction_validation import PredictionValidation
from training_model import TrainModel
from predict import Predict

app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
@cross_origin()
def index():
    """
    Description: This method is responsible for showing the home page to the user
    :return: Index HTML template
    :failure: Error Response
    """

    try:
        return render_template('index.html')
    except Exception as e:
        return Response('Error Occurred {}'.format(e))


@app.route('/train', methods=['POST'])
@cross_origin()
def train():
    """
    Description: This method is responsible for training the data
    :return: Success Message
    :failure: Error Response
    """
    try:
        if request.json and request.json['filepath'] is not None:
            path = request.json['filepath']

            # Initializing the training object
            train_obj = Train_Validation(path)

            # Calling the training validation function
            train_obj.train_validation()

            # Initializing the training model object
            model_train = TrainModel()

            # Training the models for the files in the table
            model_train.trainingModel()

            return Response('<h1>Training is Successful</h1>')

        else:
            return Response('<h1>Training is not successful</h1>')

    except Exception as e:
        return Response("Error Occurred {}".format(str(e)))


@app.route('/predict', methods=['POST'])
@cross_origin()
def predict():
    """
    Description: This method is used to prediction
    :return: Response of file created
    :failure: Error Response
    """
    try:
        if request.json and request.json is not None:
            path = request.json['filepath']

            # Initializing the validation object for prediction
            pred_val = PredictionValidation(path)

            # Validating the prediction dataset
            pred_val.prediction_validation()

            # Initializing the prediction object
            pred = Predict(path)

            # Predicting for dataset present in the database
            path = pred.predictionFromModel()

            return Response('Prediction file is created at {}'.format(path))

    except Exception as e:
        return Response('Error Occurred {}'.format(e))


if __name__ == "__main__":
    app.run(debug=True)
