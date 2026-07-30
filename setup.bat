@echo off
setlocal enabledelayedexpansion

echo ============================================
echo   Python RAG Tutor Bot - Automatic Setup
echo ============================================
echo.

REM --- 1. Create virtual environment if it doesn't already exist ---
if not exist venv (
    echo [1/8] Creating virtual environment...
    python -m venv venv
) else (
    echo [1/8] Virtual environment already exists, skipping.
)

REM --- 2. Activate it (call, so the rest of this script keeps running) ---
echo [2/8] Activating virtual environment...
call venv\Scripts\activate.bat

REM --- 3. Install dependencies ---
echo [3/8] Installing dependencies from requirements.txt (this may take a while)...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: pip install failed. Fix the error above and re-run this script.
    pause
    exit /b 1
)

REM --- 4. Download NLTK data ---
echo [4/8] Downloading NLTK data...
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('wordnet')"

REM --- 5. Make sure .env exists ---
if not exist .env (
    echo [5/8] No .env found - creating one from .env.example.
    copy .env.example .env >nul
    echo.
    echo IMPORTANT: .env was just created with placeholder values.
    echo Opening it in Notepad now - paste your real LLM_API_KEY, save, and close it.
    echo.
    notepad .env
) else (
    echo [5/8] .env already exists, skipping.
)

REM --- 6. Scrape fresh content from docs.python.org ---
echo [6/8] Scraping the knowledge base from docs.python.org...
python 00_scrape_documents.py
if errorlevel 1 (
    echo.
    echo WARNING: scraping failed or was skipped ^(e.g. no internet^). The app
    echo will automatically fall back to the curated topics built into
    echo 01_documents.py - this is not a fatal error, continuing.
)

REM --- 7. Run the retrieval evaluation (auto-tunes ALPHA) ---
echo [7/8] Running retrieval evaluation (auto-tunes ALPHA)...
python evaluation\evaluate_retrieval.py
if errorlevel 1 (
    echo.
    echo WARNING: evaluation failed or was skipped. The app will fall back to
    echo the default ALPHA=0.6 - this is not a fatal error, continuing.
)

REM --- 8. Build the vector store ---
echo [8/8] Building the vector store...
python 05_create_chroma_store.py
if errorlevel 1 (
    echo.
    echo ERROR: building the vector store failed. Check the error above.
    pause
    exit /b 1
)

echo.
echo ============================================
echo   Setup complete!
echo ============================================
echo.
set /p LAUNCH="Launch the app now with 'streamlit run streamlit_app.py'? (Y/N): "
if /i "%LAUNCH%"=="Y" (
    streamlit run streamlit_app.py
) else (
    echo You can launch it anytime with: streamlit run streamlit_app.py
    pause
)
