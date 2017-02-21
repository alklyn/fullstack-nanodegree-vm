


base = """
<html>
    <head>
        <title>
            {title}
        </title>

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
                <li> {restaurant_name} </li> \n
                <div><a href="/restaurants/{restaurant_id}/edit">Edit</a></div>
                <div><a href="/restaurants/{restaurant_id}/delete">Delete</a></div>
            </p>
"""

new_restaurant_form = """
        <h1> Make A New Restaurant </h1>
        <form method="POST" enctype="multipart/form-data" action="/restaurants/add_new">
            <input name="new_restaurant" type="text">
            <button> Submit </submit>
        </form>
"""

edit_restaurant_form = """
        <h1> Edit Restaurant </h1>
        <form method="POST" enctype="multipart/form-data" action="/restaurants/edit_restaurant">
            <input name="new_name" type="text" value="{old_name}">
            <input name="restaurant_id" type="hidden" value="{restaurant_id}">
            <button> Edit Restaurant </submit>
        </form>
"""

delete_restaurant_form = """
        <h1> Edit Restaurant "{restaurant_name}"</h1>
        <form method="POST" enctype="multipart/form-data" action="/restaurants/delete_restaurant">
            <input name="restaurant_id" type="hidden" value="{restaurant_id}">
            <button> Delete Restaurant </submit>
        </form>
"""
