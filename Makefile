run_app:
	venv/bin/uvicorn user_doc.app:app --reload --log-level debug

format:
	isort user_doc
	black user_doc
