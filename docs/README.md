# A Small Library App Backend#

A _small_ library app backend. Half Baked.

### Installation ###
* Clone Me
* Create a virtual environment if required.
* Install dependencies from requirements.txt
* Set environment variable `DATABASE_URL` to database connector URI.
* Make migrations, migrate and run


### APIs ###
##### Book related #####
1. List all books
    ```text
    /book/     
    ```
2. Search by author in book list
    ```text
    /book/?author=author_name
    ```
3. Search by title in book list
    ```text
    /book/?title=title_name
    ```
4. Search by book tag
    ```text
    /book/?booktag__tag=tag
    ```
4. Or use a combination of any of 2, 3, 4
6. See details of a book with pk `pk`
    ```text
    /book/pk
    ```
7. Create a new Book
    ```text
    /book/new
    ```
7. Add tag to a book with pk `pk`
    ```text
    /book/pk/tag/?tags=tag1,tag2, tag 3
    ```

### Demo ###
A Sample of API can be found [here](https://boiling-scrubland-41951.herokuapp.com).