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

menu_content = """
        <h1> {restaurant_name} </h1>
        <h2> Menu Items </h2>
        <ol>
            {menu_list}
        </ol>
"""

menu_item = """
            <li>
                <div>{name}<div>
                <div>{price}<div>
                <div>{description}<div>
            </li>
            <hr>
"""
