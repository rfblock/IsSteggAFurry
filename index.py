from flask import Flask, redirect, render_template, send_from_directory, request
import json
import os

#Init App
app = Flask(__name__)

#Rate Limit // Doesn't work with PythonAnywhere
#s = sched.scheduler(time.time, time.sleep)
rate_limited_ips = []
#def clear_rate_limit():
#    print("clearing")
#    global rate_limited_ips
#    if rate_limited_ips:
#        rate_limited_ips.clear()

#Load config
with open('config.json') as config_file:
    config = json.loads(config_file.read())

#Load counter
with open(config['PATH'], 'r+') as count_file:
    _json = json.loads(count_file.read())
    count = _json['count']
    daily = _json['daily']
print(count)

#Increment Counter
def increment(ip):
    global count, daily, rate_limited_ips
    if ip in rate_limited_ips:
        return (count, daily)
    rate_limited_ips.append(ip)
    print(ip)
    count = count + 1
    daily = daily + 1
    with open(config['PATH'], 'r+') as count_file:
        json.dump({'count': count, 'daily': daily}, count_file)
    return (count, daily)



#Routes



@app.errorhandler(404)
def page_not_found(e):
    return redirect('/furry?'), 404, {'Refresh': '0; url=/furry?'}

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/about')
def about():
    global count, daily
    return render_template('about.html', count=(count, daily), titles=config['TITLES'])

@app.route('/furry')
def furry():
    return render_template('index.html', count=increment(request.remote_addr), titles=config['TITLES'])


#Init App
if __name__ == '__main__':
    app.run(port=8080)