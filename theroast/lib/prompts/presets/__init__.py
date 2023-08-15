from textwrap import dedent

DEFAULT_TEMPLATE = dedent('''\
<response>
    <newsletter>
        <title>
            Title of the newsletter section
        </title>
        <introduction>
            Introduction of the newsletter section
        </introduction>
        <body>
            Body of the newsletter section with markdown formatting and lists where needed
        </body>
        <conclusion>
            Conclusion of the newsletter section
        </conclusion>
    </newsletter>
</response>
''')