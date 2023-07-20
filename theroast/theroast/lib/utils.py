from textwrap import dedent

NON_SECTIONS = ["title", "introduction", "conclusion"]

def construct_newsletter_html(data):

    
    body = "\n".join([f"<h3>{section['title']}</h3>\n<p>{section['body']}</p>" for section in data["sections"]])

    return dedent(f'''\
        <div>
            <h1>{data["title"]}</h1>
            <p>{data["introduction"]}</p>
            <div>
                {body}
            </div>
            <p>{data["conclusion"]}</p>
        </div>''')