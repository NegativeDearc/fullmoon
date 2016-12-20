from app import app

if app.config['CONFIG_NAME'] == 'development':
    app.run(port=5000,threaded=True)
if app.config['CONFIG_NAME'] == 'production':
    pass