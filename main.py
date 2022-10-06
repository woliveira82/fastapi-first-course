from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    return {'status': 'ok'}


@app.get('/blog/unpublished')
def get_unpublished_blog():
    return {'data': [1, 2]}


@app.get('/blog/{id}')
def get_blog(id: int):
    return {'data': id}


@app.get('/blog/{id}/comments')
def get_blog_comments(id: int):
    return {'data': [1, 2]}
