docker build -t sofomo-test:latest .
docker run -dp  5000:5000 --name sofomo-test sofomo-test
python -m pytest
docker exec -it sofomo-test
docker stop sofomo-test
docker rm sofomo-test
docker rmi sofomo-test:latest