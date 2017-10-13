import requests
import io, json


class Author(object):
    id = 0
    name = ""
    posts = []

    def __init__(self, id, name, posts):
        super(Author, self).__init__()
        self.id = id
        self.name = name
        self.posts = posts

    def get_data(self):
        print "Author:", self.name, "ID:", self.id, "Posts:", self.posts

posts = []
users = []

page_count = 1

while True:
    USER_URL = "http://manipalthetalk.org/wp-json/wp/v2/users?page=%d" %(page_count)
    response = requests.get(USER_URL).json()
    if len(response)==0:
        break
    else:
        users.append(response)
        page_count += 1

print "User data fetched"

output_user_list = []

for x in xrange(len(users)):
    for y in xrange(len(users[x])):
        output_user_list.append(Author(users[x][y]["id"], users[x][y]["name"], []))

page_count = 1

for author in output_user_list:
    print "Current Author:", author.id, " : ", author.name
    while True:
        POST_URL = "http://manipalthetalk.org/wp-json/wp/v2/posts?author=%d&per_page=100&page=%d" %(author.id, page_count)
        response = requests.get(POST_URL)
        if response.status_code != 200 or len(response.json())==0:
            print "Done."
            page_count = 1
            break
        else:
            author.posts.append(response.json())
            page_count += 1
            print "Adding..."

json_string = json.dumps([author.__dict__ for author in output_user_list], ensure_ascii=False)
print json_string
