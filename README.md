# BackendProject

- An API to fetch latest videos sorted in reverse chronological order of their publishing date-time from youtube for a given tag/search query in a paginated response. <br />


Technologies used: Flask, Sqlite3 <br />

Steps to Install:<br />
<br />
Step 1: Download the Zip file or run ```git clone https://github.com/chandrashekarvt/BackendProject.git``` <br/>
<br />
Step 2: Run the server using the following steps :<br />
  - Navigate to BackendProject/ and create a virtual environment<br />
  - Run ```pip3 install -r requirements.txt```<br />
  - Now in the app.py file add your GOOGLE API KEY, set your data limit and search query.
  - Then run ```flask run```<br />
  <br />
  
Step 3: Visit ```http://127.0.0.1:5000/1``` in your local browser to view the first page of the response<br />
<br />
