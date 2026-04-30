import pytest

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    assert res.status_code == 200
    assert len(res.json()) == len(test_posts)

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/99999")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    
    # DIAGNOSTIC PROBE: Print the raw JSON to the terminal
    print("\n[DIAGNOSTIC] RAW API RESPONSE:", res.json())
    
    assert res.status_code == 200
    post = res.json()
    post_id = post['Post']['id'] if 'Post' in post else post['id']
    assert post_id == test_posts[0].id

@pytest.mark.parametrize("title, content, published", [
    ("Azure AZ-400 Target", "Studying CI/CD", True),
    ("Mastering C#", ".NET 9 is next", False),
    ("Linux File Permissions", "chmod 777 is trash", True),
])
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    assert res.status_code == 201
    assert res.json()['title'] == title

def test_unauthorized_user_create_post(client):
    res = client.post("/posts/", json={"title": "Hack", "content": "Bypass"})
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_non_existent(authorized_client, test_user, test_posts):
    res = authorized_client.delete("/posts/9999999")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_posts):
    # test_user is logged in, but post[2] belongs to test_user2
    res = authorized_client.delete(f"/posts/{test_posts[2].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {"title": "Updated Title", "content": "Updated Content", "id": test_posts[0].id}
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 200
    assert res.json()['title'] == data['title']

def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {"title": "Malicious Update", "content": "Hacked", "id": test_posts[2].id}
    res = authorized_client.put(f"/posts/{test_posts[2].id}", json=data)
    assert res.status_code == 403