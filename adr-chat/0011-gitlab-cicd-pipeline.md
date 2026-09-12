# ADR 011: GitLab CI/CD Pipeline — Test → Build → Deploy (Manual)

## Status
Accepted (Session: 2026-09-12 04:45+)

## Context
Added with "удали дефолтные заклинания... сделай их неограниченными" commit — user wanted CI/CD for automated deployment.

## Decision
**Create `.gitlab-ci.yml` with 3 stages:**

```yaml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  image: python:3.11-slim
  script:
    - pip install -r requirements.txt
    - python -c "import bot; print('Import OK')"
    - python -c "from bot import roll_dice; print([roll_dice('2d6+3') for _ in range(3)])"
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == "main"

build:
  stage: build
  image: docker:27
  services:
    - docker:27-dind
  script:
    - docker login -u "$CI_REGISTRY_USER" -p "$CI_REGISTRY_PASSWORD" $CI_REGISTRY
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - docker tag $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA $CI_REGISTRY_IMAGE:latest
    - docker push $CI_REGISTRY_IMAGE:latest
  rules:
    - if: $CI_COMMIT_BRANCH == "main"

deploy_railway / deploy_render / deploy_fly / deploy_vps:
  stage: deploy
  image: alpine:latest
  script: # curl to platform APIs
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual
```

## Alternatives Considered
- Auto-deploy on push (rejected — manual gate for production)
- Single deploy job with platform choice (rejected — separate for clarity)

## Consequences

### Positive
- Tests run on every MR
- Docker image built and pushed to GitLab Registry
- Manual deploy buttons in GitLab UI for each platform
- Platform-specific variables in CI/CD settings

### Negative
- Requires CI/CD variables setup per platform
- VPS deploy needs SSH key in variables
- Free runners may have queue delays

## Required CI/CD Variables (GitLab Settings → CI/CD → Variables)
| Variable | Platform | Protected |
|---|---|---|
| `RAILWAY_TOKEN`, `RAILWAY_ENVIRONMENT_ID` | Railway | Yes |
| `RENDER_API_KEY`, `RENDER_SERVICE_ID` | Render | Yes |
| `FLY_API_TOKEN`, `FLY_APP_NAME` | Fly.io | Yes |
| `VPS_HOST`, `VPS_USER`, `VPS_SSH_KEY` | VPS | Yes |

## Related Decisions
- ADR 002: Deployment guides reference these pipelines
- ADR 010: Repo created for this CI/CD