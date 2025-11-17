@echo off
echo ========================================
echo AI Diet Plan Generator - Starting Server
echo ========================================
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting Flask server...
echo Server will run on http://localhost:5000
echo.
echo Open index.html in your browser to use the app
echo Press Ctrl+C to stop the server
echo.
python app.py
