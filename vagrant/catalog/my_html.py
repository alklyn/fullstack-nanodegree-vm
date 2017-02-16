


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

main_content = """
        <h2> Restaurants </h2>
        <p>
            <a href="#">Make A New Restaurant Here</a>
        </p>
        <ol>
            {}
        </ol>
"""

item_html = """
            <p>
                <li> {} </li> \n
                <div><a href="#">Edit</a></div>
                <div><a href="#">Delete</a></div>
            </p>
"""
