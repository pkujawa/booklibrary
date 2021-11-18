# booklibrary

Application which allows you to add books to the database and search in the database using title, author, language and published date.
You can also import the data of the book from the Google Books API, using author, title and ISBN number.

To access the API view,  add /api at the end of the url.

### Notes:
* date published - while importing from Google Books API, had to set months and days to 1 by default so it fits the date format - sometimes it is just year or year and month in the Google Library. Assumed this would be better since it was probably wanted to use the date field for this one.
* author - assumed they will be listed separated with comma if it's more than 1 while adding manually to database. Better approach would be using many to many relation - but this would bring many changes to the code and wouldn't let me use the standard method for filters etc. Assmued it was expected to treat it as one since it was named 'author' in the task description.
