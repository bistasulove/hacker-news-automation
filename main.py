from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
from scrape_service.scrape import Scraper
from gdrive_service import gdrive

app = Flask(__name__)


@app.route('/', methods=['GET' , 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        interests = request.form['interests']

        email_present = gdrive.check_if_email_present(email)
        if not email_present:
            try:
                gdrive.add_to_gsheet(email, interests)
            except:
                return redirect('/error')
            return redirect('/success')
        else:
            return redirect(url_for('failure', email=True))

    return render_template('index.html', title='Home')
    

@app.route('/success')
def success():
    return render_template('next_step.html', content='success')

@app.route('/failure')
def failure():
    value = request.args.get('email')
    print(type(value))
    if value == 'True':
        content = 'email exists'
    else:
        content = 'email do not exist'
    return render_template('next_step.html', content=content)

@app.route('/error')
def error():
    return render_template('next_step.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
    
        email = request.form['email']

        email_present = gdrive.check_if_email_present(email)
        if email_present:
            try:
                gdrive.remove_from_gsheet(email)
                return redirect('/success')
            except:
                return redirect('/error')
        else:
            return redirect(url_for('failure', email=False))
    return render_template('delete.html', title='Delete')


@app.route('/scrape')
def scrape():
    records = gdrive.get_all_records()
    for record in records:
        print(f"Fetching news for {record.get('email')} with interests {record.get('interests')}")
        s = Scraper(record.get('email'), 'https://news.ycombinator.com/', record.get('interests'))
        s.fetch_headlines()
        s.store_news()
        s.mail_news()
    return "Successfully sent"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)