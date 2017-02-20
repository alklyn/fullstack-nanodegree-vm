


base = """
<html>
    <head>
        <title>
            {title}
        </title>
        
        {my_js}
    </head>

    <body>
        {content}
    </body>
</html>
"""

main_content = """
        <h2> Restaurants </h2>
        <p>
            <a href="/restaurants/new">Make A New Restaurant Here</a>
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

new_restaurant_form = """
        <h1> Make A New Restaurant </h1>
        <form method='POST' enctype='multipart/form-data' action='/restaurants/add_new'>
            <input name='new_restaurant' type='text'>
            <button> Submit </submit>
        </form>
"""

my_js = """
            <script>
                function redirect(post_id){
                   window.location.href = "/blog/" + post_id;
                }
            </script>
"""

add_new_content = """
            <script>
                setTimeout(function() { redirect("/restaurants"); }, 50);
            </script>
"""
