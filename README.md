# Graphql-pycon.co2018  by carlosmart626

<p align="center">
  <img src="https://s3.amazonaws.com/carlosmart.co/pycon-logo.png">
</p>

Graphql implementation example to show some of the features of [Graphene-Django](http://graphene-python.org).

<p align="center">
  <img width="250" src="https://s3.amazonaws.com/carlosmart.co/graphene-logo.png">
</p>

This is an example of a **courses** platform allowing to create users and courses and to enroll into a desired course.

### Features
- Create students with profile
- Create courses
- Enroll students to courses

### Running the project
**Requires Docker installed**
To run the project execute: 

```
cd djcourses
docker-compose up
```

After run this command open your navigator at `http://localhost:8080/graphiql` to get into the Graphql query environment.

### Firsts Graphql queries

**Query**
``` json
query{
  hello
}
```

**Result**
``` json
{
  "data": {
    "hello": "world"
  }
}
```
