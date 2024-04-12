# django_soft_delete
An alternative to the default Django behavior of permanently removing records

**Features**
1. Check Delete: Restricts for Protected Records and Warn for related records before performing actual deletion
2. Delete: Applies soft deletion to related records recursively to root level.

**Data Structure**  
Refer data_structure.txt file

**Testing**  
visit "/delete/db_migration/" to create test records
