from flask import Flask, request, Response, render_template, redirect
from flask.ext.sqlalchemy import SQLAlchemy
import os
import requests
import urllib
import json
import urlparse
import dt
from auth import requires_auth

SUPPLIER_URL = "http://hst-api.wialon.com/wialon/ajax.html?"

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Intervals(db.Model):
    __tablename__ = 'intervals'

    id = db.Column(db.Integer, primary_key=True)
    tbegin = db.Column(db.Integer())
    tend = db.Column(db.Integer())

    def __init__(self):
        a=1

    def __repr__(self):
        return '<id {}>'.format(self.id)


@app.route('/wialon/ajax.html')
def change_url():


        args = dict(urlparse.parse_qsl(urllib.unquote(urlparse.urlparse(request.url.encode('ascii')).query)))
        paramsstr = urlparse.urlparse(request.url.encode('ascii')).query
        pms = json.loads(args['params'])
        if args.has_key('svc') and args['svc'] == 'messages/load_interval':
            # and int(pms['timeTo']) - int(pms['timeFrom']) > 24*3600:
            _from = dt.date_time(dt.begin_date(int(pms['timeFrom'])+ 7200 + 1), int(Intervals.query.limit(1).first().tbegin)-7200)
            _to = dt.date_time(dt.begin_date(int(pms['timeTo']) + 7200), int(Intervals.query.limit(1).first().tend)-7200)
            print "Old: " + dt.htime(int(pms['timeFrom'])) + " - " + dt.htime(int(pms['timeTo']))
            print "New: " + dt.htime(_from) + " - " + dt.htime(_to)
            new_from = "\"timeFrom\":"+str(_from)
            new_to = "\"timeTo\":"+str(_to)
            paramsstr = paramsstr.replace("\"timeFrom\":"+str(pms['timeFrom']), new_from).replace("\"timeFrom\":\""+str(pms['timeFrom'])+"\"", new_from).replace("\"timeTo\":"+str(pms['timeTo']), new_to).replace("\"timeTo\":\""+str(pms['timeTo'])+"\"", new_to)
            # paramsstr = paramsstr.replace("\"timeTo\":"+str(pms['timeTo']), new_to).replace("\"timeTo\":\""+str(pms['timeTo'])+"\"", new_to)
        q = SUPPLIER_URL + paramsstr
        res = requests.get(q).text
        resp = Response(res)
        resp.headers['Content-Type']='application/json'
        return resp

@app.route('/admin')
@requires_auth
def admin():
    rec = Intervals.query.limit(1).first()
    _from = dt.sec_to_time(int(rec.tbegin))
    _to = dt.sec_to_time(int(rec.tend))
    return render_template('admin.html', _from = _from, _to = _to)

@app.route('/change_time', methods=['POST'])
def change_time():
    _from = request.form.get('from')
    _to = request.form.get('to')
    rec = Intervals.query.limit(1).first()
    rec.tbegin = dt.time_to_sec(_from)
    rec.tend = dt.time_to_sec(_to)
    db.session.commit()
    return redirect('/admin')

@app.route('/test')
def hello():
    return "OK " + os.environ['APP_SETTINGS'] + " - " + Intervals.query.limit(1).first().tend 

if __name__ == '__main__':
    app.run()