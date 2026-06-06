## first make networks:

docker network create \
 --driver overlay \
 --attachable \
 traefik-public

docker network create \
 --driver overlay \
 --attachable \
 web

docker network create \
 --driver overlay \
 --internal \
 internal

## you can make your local registry for dokply swarm

docker run -d -p 5000:5000 --name local-regsitry --restart=always registry:2

### then add insecure registry to /etc/docker/daemon.json

{
"insecure-registries" : ["localhost:5000"]
}
