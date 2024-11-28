# Setup Heroku

## Heroku Setup

- create heroku app: `heroku create qrcode-generator`
- create heroku files: `touch Procfile`, `touch Procfile.windows`(windows only)
- add buildpacks: `heroku buildpacks:add heroku/python`
- push to heroku: `git push heroku main`
- open heroku: `heroku open`
- logs: `heroku logs --tail` (to check if the app is running)
