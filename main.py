import unittest

from app.main import create_app

app = create_app()

@app.cli.command('run')
def run():
     app.run()

@app.cli.command('test')
def test():
     tests = unittest.TestLoader().discover('app/main/test', pattern='*_test.py')
     result = unittest.TextTestRunner(verbosity=2).run(tests)
     if result.wasSuccessful():
          return 0
     return 1
     
if __name__ == '__main__':
     app.run()