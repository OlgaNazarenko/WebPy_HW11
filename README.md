## WebPy_HW12
REST API for storing and managing contacts [^1].

Run the following command to start the FastAPI server:

    python3 main.py

In the code was added the following:
- An authentication mechanism in the application; 
- An authorization using JWT tokens, so that all operations with contacts are performed only by registered users; 
- The user has access only to his/her operations with contacts.

[^1]: It was done with SQLite.
