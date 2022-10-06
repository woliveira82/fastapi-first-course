from fastapi import FastAPI

app = FastAPI()


@app.get('/blogs')
def list_all_blogs(sort, published: bool = True, limit: int = 10):
    phrase = f'{limit} blogs from database' if published else f'{limit} published blogs from database'
    return {'data': [phrase]}


@app.get('/blogs/unpublished')
def get_unpublished_blogs():
    return {'data': [1, 2]}


@app.get('/blogs/{id}')
def get_blog_by_id(id: int):
    return {'data': id}


@app.get('/blogs/{id}/comments')
def list_comments_from_blog_id(id: int, limit: int = 10):
    return {'data': [1, 2]}
