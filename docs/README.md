# A Small Library App #

A _small_ library app. Half Baked.

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
4. Or combine 3 and 4
    ```text
    /book/?title=title_name&&author=author_name
    ```
5. See details of a book with pk `pk`
    ```text
    /book/pk
    ```
6. Create a new Book
    ```text
    /book/new
    ```
7. Add tag to a book with pk `pk`
    ```text
    /book/pk/tag
    ```
