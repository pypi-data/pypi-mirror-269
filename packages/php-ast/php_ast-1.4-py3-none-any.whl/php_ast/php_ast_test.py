from php_ast import php_ast

php=php_ast()
ast=php.get_file_ast("/www/wwwroot/192.168.1.72/upload/upload/1111.php")
print(ast)
