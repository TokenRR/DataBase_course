python csv_to_db.py
python -m flask --app app db upgrade 3f4d76e9210d
python -m flask --app app db upgrade ba09343fb2cf
python -m flask --app app db upgrade c6d219f055c1
python final_query.py
python -m flask --app app run -h 0.0.0.0 -p 5000
