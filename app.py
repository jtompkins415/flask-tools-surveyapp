
from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret-survey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES_KEY = 'responses'

@app.route('/')
def show_survey_start():
    '''Show start page with survey title and instructions'''

    
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template('survey-start.html', title=title, instructions=instructions)

@app.route('/begin', methods=['POST'])
def start_session():
    '''Go to question 1 and start the session'''
    
    session[RESPONSES_KEY] = []

    return redirect('/questions/0')


@app.route('/questions/<int:quest_id>')
def show_survey_question(quest_id):
    '''Show question from survey'''
    responses = session.get(RESPONSES_KEY)
    
    if responses is None:
        #If there are no answer in the response list return to home page
        return redirect('/')
    
    if len(responses) == len(satisfaction_survey.questions):
        #If all questions have been answered go to congrats page
        return redirect('/congrats')
    
    if (len(responses) != quest_id):
        #If user tries to jump ahead questions, return user to previous question
        flash(f'Invalid question: {quest_id}')
        return redirect(f'/questions/{len(responses)}')
   
    question = satisfaction_survey.questions[quest_id]
    return render_template('question.html', question=question,quest_id=quest_id)

@app.route('/answer', methods =['POST'])
def append_choice():
    '''Append answer to question to the response list and redirect to next question'''

    choice = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/congrats')
    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/congrats')
def end_survey():
    '''Congratulates user upon completion of survey'''

    return render_template('congrats.html')