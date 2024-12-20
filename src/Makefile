start:
	uvicorn src.main:app --reload --port 4000

mongoimport:
	docker exec -i mongodb mongoimport -u admin -p admin --port 27017 --collection users --file default_user.json --jsonArray --authenticationDatabase admin