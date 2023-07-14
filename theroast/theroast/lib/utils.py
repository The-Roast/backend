from textwrap import dedent

NON_SECTIONS = ["title", "introduction", "conclusion"]

def construct_newsletter_html(data):

    
    k = list(data.keys())
    sh = [s for s in k if s not in NON_SECTIONS]
    body = "\n".join([f"<h3>{t}</h3>\n<p>{data[t]}</p>" for t in sh])

    return dedent(f'''\
        <div>
            <h1>{data["title"]}</h1>
            <p>{data["introduction"]}</p>
            <div>
                {body}
            </div>
            <p>{data["conclusion"]}</p>
        </div>''')