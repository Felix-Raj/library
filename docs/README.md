# A Small Library App Backend #

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
5. Search by book_id
    ```text
    /book/?book_id=book_id
    ```
6. Search by category
    ```text
    /book/?category=category
    ```
    Where category can be `magazine`, `book`, `comics`.
    
6. Or use a combination of any of 2, 3, 4, 5, 6
7. See details of a book with pk `pk`
    ```text
    /book/pk
    ```
8. Create a new Book
    ```text
    /book/new
    ```
9. Add tag to a book with pk `pk`
    ```text
    /book/pk/tag/?tags=tag1,tag2, tag 3
    ```
    
##### Library Users Related #####
1. List all Library Users
    ```text
    /lib_user/
    ```
    
2. Search for user in list using pk
    ```text
    /lib_user/?pk=pk
    ```
    
3. Search for user in list using name
    ```text
    /lib_user/?name=name
    ```
    
4. Search for user in list using uid
    ```text
    /lib_user/?uid=uid
    ```
    
5. Combine any of 2,3 and 4

6. Search for any using
    ```text
    /lib_user/?search=term
     ```
     term can be `author`, `title`, `booktag`, `book_id`, `category` 
     
7. Specify ordering by
    ```term
    /lib_user/?ordering=field_one, field_two
    ```
    field can be any of `author`, `title`, `book_id`, `category`
    
8. Create a new user
    ```text
    /lib_user/new
    ```
        
8. Get users with upcoming birthdays
    ```text
    /lib_user/birthdays/
    ```

9. List books lent by a user, using users pk
    ```text
    /lib_user/pk/lent/pending/
    ```

10. See recent birthdays
    ```text
       /lib_user/birthdays/
    ```
    
11. Activate an user
    ```text
        /lib_user/pk/activate/
    ```
    
12. Deactivate an user
    ```text
        /lib_user/pk/deactivate
    ```


##### Lent Related #####
1. List all lents
    ```text
    /lib_user/lent/
    ```
    
2. List all lents - search for user with pk `pk`
    ```text
    /lib_user/lent/?lib_user=pk
    ```
    
3. List all lents - search  for book with pk `pk`
    ```text
    /lib_user/lent/?book=pk
    ```
    
4. List all lents - search for user with name containing `name`
    ```text
    /lib_user/lent/?lib_user__name=name
    ```
    
5. List all lents - search for book with name containing `name`
    ```text
    /lib_user/lent/?book_title=name
    ```
    
6. List all lents - can mix any of the above queries

7. Create new Lent
    ```text
    /lib_user/lent/new/
    ```

8. Upcoming or Missed Dues
    ```text
    /lib_user/lent/recent_dues/
    ```

#### Notes ####
Users can add note
1. List all notes
    ```text
    /note/
    ```
    
2. Create new note
    ```text
    /note/new/
    ```
    
3. Delete note
    ```text
     /note/pk/delete
    ```

### Demo ###
A Sample of API can be found [here](https://boiling-scrubland-41951.herokuapp.com).
