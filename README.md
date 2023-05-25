# 20220277-TP3


# DevOps - TP2 - Weather scrapper API

<image src="https://www.syloe.com/wp-content/uploads/2020/11/Azure_Container_Registry.jpg" width=800 center>

[![Downloads](https://static.pepy.tech/personalized-badge/docker?period=month&units=international_system&left_color=blue&right_color=yellow&left_text=docker)](https://pepy.tech/project/docker)   [![Downloads](https://static.pepy.tech/personalized-badge/requests?period=month&units=international_system&left_color=brightgreen&right_color=orange&left_text=requests)](https://pepy.tech/project/requests) [![Downloads](https://static.pepy.tech/personalized-badge/openweather?period=month&units=international_system&left_color=blue&right_color=green&left_text=openweather)](https://pepy.tech/project/openweather) [![Downloads](https://static.pepy.tech/personalized-badge/github?period=month&units=international_system&left_color=black&right_color=orange&left_text=github)](https://pepy.tech/project/github) [![GitHub Actions](https://github.com/actions/toolkit/actions/workflows/main.yml/badge.svg)](https://github.com/actions/toolkit/actions/workflows/main.yml)

>>> ### Objectifs

> - Mettre à disposition son code dans un repository Github
> - Mettre à disposition son image (format API) sur Azure Container Registry (ACR) usingGithub Actions
> - Deployer sur Azure Container Instance (ACI) using Github Actions

>>> ### Prérequis

> - Docker
> - Github
> - Azure Container Registry (ACR)
> - Azure Container Instance (ACI)

https://learn.microsoft.com/en-us/azure/container-instances/container-instances-github-action?tabs=userlevel

> NOTE: Ce TP a pour principal objectif de déployer l'image de notre API de weather sur Azure Container Registry (ACR) comme fait au TP2 sur le DockerHub. Les paramètres (secrets) sont déjà créés dans l'environnement Azure. Nous allons donc les utiliser pour faire nos configurations au niveau du Github Actions.


>>> ### 1. Configuration d"un workflow Github Action
- Créer le fichier `.github/workflows/main.yml` dans le dossier du projet
- Ajouter le contenu suivant :
````
on: [push]
name: Linux_Container_Workflow

jobs:
    build-and-deploy:
        runs-on: ubuntu-latest
        steps:
        # checkout the repo
        - name: 'Checkout GitHub Action'
          uses: actions/checkout@main
          
        - name: 'Login via Azure CLI'
          uses: azure/login@v1
          with:
            creds: ${{ secrets.AZURE_CREDENTIALS }}
        
        - name: 'Build and push image'
          uses: azure/docker-login@v1
          with:
            login-server: ${{ secrets.REGISTRY_LOGIN_SERVER }}
            username: ${{ secrets.REGISTRY_USERNAME }}
            password: ${{ secrets.REGISTRY_PASSWORD }}
        - run: |
            docker build . -t ${{ secrets.REGISTRY_LOGIN_SERVER }}/20220277:${{ github.sha }}
            docker push ${{ secrets.REGISTRY_LOGIN_SERVER }}/20220277:${{ github.sha }}

        - name: 'Deploy to Azure Container Instances'
          uses: 'azure/aci-deploy@v1'
          with:
            resource-group: ${{ secrets.RESOURCE_GROUP }}
            dns-name-label: devops-20220277
            image: ${{ secrets.REGISTRY_LOGIN_SERVER }}/20220277:${{ github.sha }}
            registry-login-server: ${{ secrets.REGISTRY_LOGIN_SERVER }}
            registry-username: ${{ secrets.REGISTRY_USERNAME }}
            registry-password: ${{ secrets.REGISTRY_PASSWORD }}
            name: 20220277
            location: 'france central'
            secure-environment-variables: API_KEY=${{ secrets.API_KEY }}

````

Cette configuration permet de:
- Se connecter avec Azure CLI
- Construire et pusher l'image
- Deploy to Azure Container Instances

> Mise à partir les secrets défini en global pour le projet, nous avons redéfini un secret API_KEY pour l'API de openweather.

À la fin de la configuration, le workflow Github Action est disponible sur Github après push et biensûr paramétrage des `secrets` utilisés. Si les secrets ne sont pas paramétrés, vous aurez une erreur lors de l'appel de l'API.

Une fois le workflow Github Action exécuté avec succès, on peut aller dans Azure Container Instances pour voir notre image bien déployé. Nous pouvons dès à présent passer au test.


>>> ### 2. Tester l'API

Pour tester notre API, nous allons utiliser la commande suivante dans un terminal. Notez bien le `/weather` qui est rajouter au lien car ainsi défini dans l'API python.


```
curl "http://devops-20220277.francecentral.azurecontainer.io/weather?lat=5.902785&lon=102.754175"
```

>>> Response:
```
{
  "base": "stations",
  "clouds": {
    "all": 79
  },
  "cod": 200,
  "coord": {
    "lat": 5.9028,
    "lon": 102.7542
  },
  "dt": 1685006647,
  "id": 1736405,
  "main": {
    "feels_like": 305.65,
    "grnd_level": 981,
    "humidity": 69,
    "pressure": 1008,
    "sea_level": 1008,
    "temp": 302.13,
    "temp_max": 302.13,
    "temp_min": 302.13
  },
  "name": "Jertih",
  "sys": {
    "country": "MY",
    "sunrise": 1684968805,
    "sunset": 1685013517
  },
  "timezone": 28800,
  "visibility": 10000,
  "weather": [
    {
      "description": "broken clouds",
      "icon": "04d",
      "id": 803,
      "main": "Clouds"
    }
  ],
  "wind": {
    "deg": 37,
    "gust": 3.99,
    "speed": 4.44
  }
}
```

>>> Remarques

Dans ce TP nous avons rencontré quelques difficultés surtout au niveau du port qui de base était le port 8081 mais azure déployait par defaut sur le port 80. Nous coup, nous avons été amené soit à redéfinir le port dans notre code pour utiliser le port 80, soit configurer le port 80 dans le github action avec le paramètre `ports: 8081`.

>
> ################################################### \
> Etudiant: AGBONON EDAGBDJI Yao Anicey \
> Promo: BDML 2024 \
> Email: yao-anicet.agbonon-edagbedji@efrei.net
> ###################################################
>