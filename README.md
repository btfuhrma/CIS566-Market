- Installation requirements:
  - Python 3.12.*
  - Python Modules: django, pillow
    - pip install django, pillow
- How to run:
  - Move to the directory containging the project
      - This directory should be named 'Market'
          - 'cd market'
          - The directory should look like this 'insert-you-path\CIS566-Market\market'
  - run the commands:
  - 'python manage.py makemigrations'
  - 'python manage.py migrate'
      - This command ensures that all schema for the database are applied
  - run the command 'python manage.py runserver'
  - Running this command will automatically have the database included and there should be no issues with any features
  - The application will then be available at http://127.0.0.1:8000/ 
- Testing Admin Functionality
  - There is an account made for that with the username = 'admin' and password = 'password'
