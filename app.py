from flask import Flask, render_template, request
import pickle
import nltk
import re
from sklearn.feature_extraction.text import TfidfVectorizer
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

rf_clf = pickle.load(open('randomforest_model.pkl', 'rb'))
tfidf = pickle.load(open('tfidffile.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():
	if request.method == 'POST':
		message = request.form['message']
		# validations for messages
		#my_prediction = pipe_clf.predict([message])
		if len(message) < 1:
			return render_template('error.html', error_msg = 'SMS Cannot be Empty !!')
		elif len(message)>500:
			return render_template('error.html',error_msg = 'SMS is too long! (Max SMS char limit : 500 characters)')
		else:
			sample_message = re.sub(pattern='[^a-zA-Z]',repl=' ', string = message)
			sample_message = sample_message.lower()
			sample_message_words = sample_message.split()

			if len(sample_message_words) == 0:
				return render_template('error.html', error_msg = 'You entered all special characters !!')

			wnl = WordNetLemmatizer()
			sample_message_words = [word for word in sample_message_words if not word in set(stopwords.words('english'))]
			final_message = [wnl.lemmatize(word) for word in sample_message_words]
			
			if len(final_message) == 0:
				return render_template('error.html', error_msg = 'Kindly enter gramatically correct SMS (It contains all Stopwords!)')

			final_message = ' '.join(final_message)
			temp = tfidf.transform([final_message]).toarray()
			my_prediction = rf_clf.predict(temp)

			if (my_prediction == 1):
				return render_template('result.html', prediction='spam')
			else:
				return render_template('result.html', prediction='ham')
			

if __name__ == '__main__':
	app.run(debug=True)
