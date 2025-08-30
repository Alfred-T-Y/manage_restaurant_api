#   creer des nodes sur PWK : éxécuter les deux premieres instructions sur les autres nodes run kubeadm

#   récupérer le fichier config avec:
cat $HOME/.kube/config

#   copier tout le text afficher et le coler dans .kube/config.yaml

#   ajouter le chemin vers ce config en fonction de où tu te trouve
export KUBECONFIG=.kube/config.yaml

#   vérifie si tout est bien configurer avec:
kubectl config view

#   switch to docker domaen of minikube
eval $(minikube docker-env)

#   switch back to docker domaen of docker-desktop
eval $(minikube docker-env -u)

#   pour exporter une image   
docker save manage_restaurant_django:latest -o manage_restaurant_django.tar

#   pour la charger
minikube image load manage_restaurant_django.tar