from flask import Flask, render_template, copy_current_request_context, request, flash, session, redirect, url_for, make_response, jsonify
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_mail import Mail, Message

from config import DevelopmentConfig
from models import db, UserEmail

from multiprocessing import Process

import threading
import forms
import json
import ijson

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()
mail=Mail()

matches=[]

@app.errorhandler(404)
def page_not_found(e): #recibe como parametro el error
  return render_template('404.html'),404 #return respuesta,numError

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
  session.clear()
  return render_template('CSRFError.html')

@app.route('/query', methods=['GET','POST'])
def query():
    try:
        articles=None
        query_form = forms.Query(request.form)

        f  = ijson.parse(open('db3.json', 'r'))
        objects = ijson.items(f, 'dog_tags.item')
        articles = (o for o in objects if o['JM'] != None)
    except BaseException as e:
        print(e)
        flash('Data is loading! Try again later!')
        return redirect(url_for('query'))
    
    if articles is not None:
        if request.method == 'POST' and query_form.validate():
            session['autor'] = query_form.autor.data 
            session['title'] = query_form.title.data 
            session['year'] = query_form.year.data 
        
        if ('autor' and 'title' and 'year') in session:
            @copy_current_request_context
            def send_message():
                matches.clear()
                for a in articles:
                    if session['autor'].strip() in a['ref'] and session['title'].strip() in a['ref'] and session['year'].strip() in a['ref']:
                        matches.append(a)
                session.clear()
            sender = threading.Thread(target = send_message)
            sender.start()
            sender.join()
            sender._stop()
            sender._delete()
            return redirect(url_for('query'))
    return render_template('query.html',query_form=query_form,matches=matches)

@app.route('/', methods=['GET','POST'])
@app.route('/<scroll>', methods=['GET','POST'])
@app.route('/<scroll>/<donation>', methods=['GET','POST'])
def impact(scroll=None, donation=None):
    subscribe_form = forms.Subscribe(request.form)
    try:
        oos=[]
        with open('oos.json') as json_file:
            oos = json.load(json_file)["out_of_scope"]
    except:
        flash('Out of scope do not loaded yet try later!')
    if request.method == 'GET' and scroll=='donate' and (donation=='1.00' or donation=='25.00' or donation=='50.00' or donation=='100.00'):
        return render_template('impact.html',subscribe_form=subscribe_form, oos=oos, scroll=scroll, donation=donation)
    if request.method == 'POST' and subscribe_form.validate():
        email = subscribe_form.email.data
        us = UserEmail(email)
        db.session.add(us)
        db.session.commit()
        email_html = render_template('email.html')
        @copy_current_request_context
        def send_message(subject,email,html):
            enviar_email(subject,email,html)
        sender = threading.Thread(name='mail_sender',
        target = send_message,
        args = (["IMPACT contact",email,email_html])
        )
        sender.start()
        flash('{} check your inbox!'.format(email))
        return redirect(url_for('impact'))
    if request.method == 'POST' and not subscribe_form.validate():
        return render_template('impact.html',subscribe_form=subscribe_form, oos=oos, scroll=scroll, mod=True)

    return render_template('impact.html',subscribe_form=subscribe_form, oos=oos, scroll=scroll)


@app.route('/json')
def json_dwld():
    return jsonify(matches)

@app.route('/test')
def json_load():
    try:
        oos={}
        with open('last9.json') as json_file:
            oos = json.load(json_file)
        return jsonify(oos)    
    except:
        flash('Try later!')
    return redirect(url_for('impact'))

def enviar_email(subject,user_email,html):
    msg = Message(subject,
                    sender = app.config['MAIL_USERNAME'],
                    recipients = [user_email])
    msg.html = html
    mail.send(msg)

if __name__ == '__main__':
    
    csrf.init_app(app)
    mail.init_app(app)  
    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    app.run(host='0.0.0.0', port=8999, use_reloader=False)
