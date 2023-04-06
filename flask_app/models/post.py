from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user


class Post:

    db="facegram"

    def __init__(self,data):
        self.id = data['id']
        self.img_url = data['img_url']
        self.comment=data['comment']
        self.user_id = data['user_id']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.owner=None



    #CREATE
    @classmethod
    def save(cls,data):
        
        query="""
        INSERT INTO posts(img_url,comment,user_id) 
        VALUES(%(img_url)s,%(comment)s,%(user_id)s);
        """
        results = connectToMySQL(cls.db).query_db(query,data)
        return results
    
    #READ
    @classmethod
    def get_all(cls):
        query="""
        SELECT * FROM posts
        LEFT JOIN users
        ON posts.user_id = users.id;
        """
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        posts =[]
        for row in results:
            this_post = cls(row)
            data={
                'id':row["users.id"],
                'first_name':row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password':row['password'],
                'created_at':row['created_at'],
                'updated_at':row['updated_at']
            }
            this_post.owner = user.User(data)
            posts.append(this_post)
        return posts
    
    
    
    @classmethod
    def get_one(cls,id):
        data={
            "id":id
        }
        query="""
        SELECT * FROM posts 
        LEFT JOIN users
        ON posts.user_id = users.id
        WHERE posts.id=%(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query,data)
        print("WE ARE HERE")
        for key,value in results[0].items():
            print(key,"\t\t",value) 
        # print(results)
        return cls(results[0])

    #UPDATE
    @classmethod
    def update(cls, data):
        query = """
        UPDATE posts 
        SET img_url = %(img_url)s,
        comment = %(comment)s
        WHERE id = %(id)s;"""

        results = connectToMySQL(cls.db).query_db(query, data)
        return results


    #DELETE
    @classmethod
    def delete(cls,id):
        data={
            'id':id
        }
        query="""
        DELETE FROM posts
        WHERE id=%(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, data)
        return results
        


