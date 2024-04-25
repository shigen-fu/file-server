# auto deploy as docker container
SERVER_PORT="10003"
TAG="file-server:$(date +"%m%d%H%M%S")"


if [ ! -f 'Dockerfile' ]; then
    echo 'Dockerfile not found'
    exit -1
fi

echo "start docker build.... tag: $TAG"
echo "the process is running.... It takes about 200 seconds"
docker build -t $TAG .

echo "start docker container...."

docker run -d -p $SERVER_PORT:9000 --name file-server -v $(pwd)/file:/app/upload $TAG

echo "sucessfully started"