# MusicExplorer
CS411 Final Project
### Installation
`git clone https://github.com/CS411-Salty-Fish/MusicExplorer.git`
### Virtual Environment
`source .venv/bin/activate`

### Project Structure
```
.
├── README.md
├── app
│   ├── __init__.py
│   ├── albumDB.py
│   ├── albumRoutes.py
│   ├── artistDB.py
│   ├── artistRoutes.py
│   ├── commentDB.py
│   ├── commentRoutes.py
│   ├── coverDB.py
│   ├── coverRoutes.py
│   ├── database.py
│   ├── profile.py
│   ├── profileRoutes.py
│   ├── routes.py
│   ├── signIn.py
│   ├── signInRoutes.py
│   ├── songDB.py
│   ├── songRoutes.py
│   ├── static
│   │   ├── css
│   │   │   ├── images
│   │   │   │   └── ...
│   │   │   └── style.css
│   │   ├── images
│   │   │   └── ...
│   │   ├── music
│   │   └── script
│   │       └── ...
│   ├── templates
│   │   ├── adv_sql_index.html
│   │   ├── album_form.html
│   │   ├── album_update.html
│   │   ├── artist_form.html
│   │   ├── artist_update.html
│   │   ├── comment_form.html
│   │   ├── comment_update.html
│   │   ├── cover_form.html
│   │   ├── cover_update.html
│   │   ├── index.html
│   │   ├── jinyang_adv_sql.html
│   │   ├── profile.html
│   │   ├── search.html
│   │   ├── shirley_adv_sql.html
│   │   ├── sign_in.html
│   │   ├── sign_up.html
│   │   ├── song_form.html
│   │   ├── song_update.html
│   │   ├── tongyun_adv_sql.html
│   │   └── wenjie_adv_sql.html
│   └── test.py
├── app.yaml
├── main.py
└── requirements.txt
```

### Usage (for group member)
1. Run locally

    `flask run`
2. Deploy to GCP

```
# installs gcloud
curl https://sdk.cloud.google.com | bash 

# installs components for python apps
gcloud components install app-engine-python 

# set the folder to a project on GCP
gcloud config set project music-explorer-307006

# login to set credental on the device
gcloud auth login

# deploy the app
gcloud app deploy
```
Link to the website: https://music-explorer-307006.uc.r.appspot.com

