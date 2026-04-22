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
