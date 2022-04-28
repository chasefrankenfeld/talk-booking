# CICD using FastAPI, Docker, Terraform, Gitlab pipelines, and AWS (EC2 & RDS)

CICD using FastAPI, Docker, Terraform, Gitlab pipelines, and AWS (EC2 & RDS)

The goal of this project is to set up a reusabe API backend that can be spun up with ease through terraform onto AWS.

## Installation

Use the package manager [poetry](https://python-poetry.org/) to install foobar.

```bash
cd services/talk_booking/
poetry intstall
```

Set up a Gitlab Repo (note: if you want to use Github, you can setup a Gitlab repo to mirror it and still get all the benefits of the Pipeline)

## Things that need to change

1. talk-booking throughout the infrastructure
2. the domains in infrastructure/talk-booking-service/\*/main -> development and production
3. gitlab.com/chasefrankenfeld --> to your username
4. gitlab project ID in the terraform remote state of infrastructure and "lib-auto-reject-talk-publish" REPO_URL
5. Add AWS_ACCESS_KEY_ID, AWS_DEFAULT_REGION, AWS_SECRET_ACCESS_KEY and CODECOV_TOKEN to Gitlab Settings CI/CD Variables

## Local

Set up DB

```
docker run --name some-postgres -e POSTGRES_DB=talkbooking -e POSTGRES_USER=app -e POSTGRES_PASSWORD=talkbooking -p 5432:5432 -d postgres
```

Run Migrations

```
poetry run alembic upgrade head
```

Run the server

```
poetry run gunicorn --bind 0.0.0.0:8000 web_app.main:app -k uvicorn.workers.UvicornWorker --reload
```

## Infrastructure

Set up through the Gitlab CI/CD pipeline using terraform to spin up:

1. VPC
2. Networks (public and private subnets)
3. Security Groups
4. HTTPS
5. Load balancers
6. ERC's
7. ECS
8. RDS - postgres
9. IAM policies
10. Logs - Cloud Watch
11. Alarms for slow responses
