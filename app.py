
from flask import Flask, render_template, request
from predict import *
from tts import *

app = Flask(__name__, template_folder='./public')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
predicted_text = ''

# Initialize the model
model = init_model()

# Home endpoint, render html file


@app.route('/')
def render():
    return render_template('index.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    global model, predicted_text
    file = request.files['file1']
    file.save('./static/file.jpg')

    predicted_caption = predict_caption(model, './static/file.jpg')
    predicted_text = predicted_caption
    text_to_speech(predicted_caption, "Male")
    predicted_caption = "Generated caption:\n" + predicted_caption
    return render_template('predicted.html', predicted_caption=predicted_caption)


@app.route('/speak', methods=['GET', 'POST'])
def speak():
    print(predict_caption)
    if predicted_text == '':
        text_to_speech('Sorry! Invalid Request', "Male")
        return
    text_to_speech(predicted_text, "Male")
    temp = "Generated caption:\n" + predicted_text
    return render_template('predicted.html', predicted_caption=temp)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run('0.0.0.0', port=port)
