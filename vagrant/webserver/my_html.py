


base = """
<html>
    <head>
        <title>{title}</title>
    </head>

    <body>
        {content}
    </body>
</html>
"""


my_form = """
<form method='POST' enctype='multipart/form-data' action='/hello'>
    <h2> What would you like me to say?</h2>
    <input name='message' type='text'>
    <button> Submit </submit>
</form>
"""

hello_content = """
Hello!
{}
""".format(my_form)

hola_content = """
&#161Hola!
{}
""".format(my_form)

post_content = """
<h2> Okay, how about this: </h2>
<h1> {} </h1>
{}
"""
