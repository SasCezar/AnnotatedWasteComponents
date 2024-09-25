<br />
<p align="center">
    <h1 align="center">Component Annotation Automated Pipeline for Abandoned Projects</h1>
    <p align="center"></p>
</p>

## About The Project

This project contains an automated pipeline that given a project from GitHub extracts the components based on the dependency graph
and labels them based on the files in each component. The end result is a dataframe containing information on the components and the files that
that they are comprised of.

## Getting started
### Prerequisites

- [Docker v4.25](https://www.docker.com/get-started) or higher.

## Running
This project uses Docker. You can run the application as follows:

- Run the docker-compose files to run all relevant services (`docker compose up` or `docker compose up --build`).

## Usage

The dockerfile for the pipeline service runs a `main.py` file. To run the pipeline one needs to instantiate the `ComponentAnnotator` class inside `main.py`. By default the class is instantiated to support Java projects. Once the class is instantiated one can run the `annotate_projects` method to retrieve `num_proj` number of projects from GitHub and process them. Once can also provide GitHub projects manually using the `annotate_project` or `annotate_project_list` methods. 

## License

#### License Update
This repository was previously licensed under the MIT License. However, it includes code that is licensed under the GNU General Public License (GPL). As a result, the entire project is now licensed under the GPL 3. All previous and future versions must comply with this license.
