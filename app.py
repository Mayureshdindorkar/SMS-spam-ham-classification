from flask import Flask, render_template, request
import pickle

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
		if len(message) == 0:
			return render_template('<h2>!!!! Please enter valid SMS !!!!<h2>')
		else:
			sample_message = re.sub(pattern='[^a-zA-Z]',repl=' ', string = message)
			sample_message = sample_message.lower()
			sample_message_words = sample_message.split()
			sample_message_words = [word for word in sample_message_words if not word in set(stopwords.words('english'))]
			final_message = [wnl.lemmatize(word) for word in sample_message_words]
			final_message = ' '.join(final_message)

			temp = tfidf.transform([final_message]).toarray()
			my_prediction = rf.predict(temp)
    		return render_template('result.html', prediction=my_prediction)

if __name__ == '__main__':
	app.run(debug=True)
