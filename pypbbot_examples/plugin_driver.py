import os
from pypbbot import app, run_server
from pypbbot.driver import AffairDriver

setattr(app, 'driver_builder', AffairDriver)
setattr(app, 'plugin_path', os.path.join('pypbbot_examples', 'plugins'))

if __name__ == '__main__':
    run_server(app='__main__:app', host='localhost', port=8082, reload=True)
