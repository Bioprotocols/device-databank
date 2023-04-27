# LabOP / SiLA Device Databank and Ontology


This project provides a infrastructure for the development of an open ontology for scientific device. 

It further develops a microservice that provides a SPARQL endpoint for querying the device ontology and a SiLA 2.0 server that can be addressed, e.g. by lab-automation tasks.

Potential use cases for the ontology are:

 * Device management : e.g. a device can be stored in a device management system
 * Device identification : e.g. a device can be identified by a barcode
 * Device tracking : e.g. a device can be tracked through the different steps of an experiment
 * Device documentation: e.g. a device can be documented with a picture, a description, a link to a protocol, etc.
 * Device interoperability: does a certain device fit into a certain instrument? does a certain lid fit onto a certain tube?
 * Device automation: e.g. liquid handling robots
 * Device recommendation: a LIMS system can recommend device based on the desired experiment


This is a shared project between the [LabOP project](https://bioprotocols.org/) and the [SiLA 2.0](https://www.sila-standard.org/) working group project.

## Features

 * Device Ontology
 * SPARQL endpoint for querying the device ontology (including a web interface)
 * SiLA 2.0 compliant endpoint for querying the device ontology

## Usage

### Installation

With docker-compose:

```bash
 wget https://raw.githubusercontent.com/Bioprotocols/device-databank/main/docker/docker-compose.yml
 # or with curl:
 curl -O https://raw.githubusercontent.com/Bioprotocols/device-databank/main/docker/docker-compose.yml

 # to pull the docker containers from the github container registry, run in the directory where the docker-compose file is located:
 docker-compose pull

 # to start the docker containers, run in the directory where the docker-compose file is located (add -d to run in the background):
 docker-compose up
```

Now you can access the SPARQL endpoint web interface at [localhost:8008](http://localhost:8008/).

The jupyter-lab notebook is available at [localhost:8009](http://localhost:8009/).
The default password for the jupyter server is `device`.

The SiLA 2.0 server listens at [localhost:50052](http://localhost:50052/).

### Access using the SPARQL endpoint with curl

```bash
   curl -X POST -H "Content-Type: application/sparql-query" -H "Accept: application/sparql-results+json" --data "SELECT * WHERE { ?s ?p ?o } LIMIT 10" http://localhost:8008/sparql
    curl --header "Accept: application/sparql-results+json"  -G 'http://localhost:8008/sparql' --data-urlencode query='
SELECT ?s WHERE {
 ?s ?p ?o
} LIMIT 10'
```


### Access using the SiLA 2.0 server

We provided some examples of how to access the ontology using the SiLA 2.0 server. You can find them in the [examples](examples/) folder.
For the ease of playing with the SiLA 2.0 server, we also provide a jupyter-lab notebook with some examples. You can find it in the [jupyter](jupyter/) folder.

 

## Documentation

The Documentation can be found here: [openlab.gitlab.io/labop-device-ontology](openlab.gitlab.io/labop-device-ontology) or [labop-device-ontology.gitlab.io](labop_device_ontology.gitlab.io/)


## Credits

This package was created with Cookiecutter* and the `opensource/templates/cookiecutter-pypackage`* project template.

[Cookiecutter](https://github.com/audreyr/cookiecutter )
[opensource/templates/cookiecutter-pypackage](https://gitlab.com/opensourcelab/software-dev/cookiecutter-pypackage) 
