import json
from flask import Blueprint, request, jsonify
from theroast.theroast.data.news import SOURCES
from theroast.theroast.lib.models import run_openai
from ...db.schemas import Users, Digests
from ...extensions import db, mail
from flask_jwt_extended import jwt_required, get_jwt_identity
from ...config import MAIL_USERNAME
from flask_mail import Message
from textwrap import dedent

core = Blueprint('core', __name__, url_prefix = "/v1")

@core.route("/digest/<uuid>", methods = ['GET'])
@jwt_required()
def get_digest(uuid):

    assert uuid and isinstance(uuid, str)

    digest: Digests = Digests.query.filter_by(uuid = uuid).first()
    if not digest:
        return {
            "response": {"message": "Digest not found."},
            "ok": False
         }, 404

    return {
        "response": digest.as_dict(),
        "ok": True
    }, 200

@core.route("/digest", methods = ['POST'])
@jwt_required()
def set_digest():

    id = get_jwt_identity()
    current_user = Users.query.filter_by(id = id).first()

    name = request.json["name"]
    settings = {
        "sources": [SOURCES[s.lower().strip()] for s in request.json["sources"].split(",") if s.lower().strip() in SOURCES.keys()],
        "interests": [i.lower().strip() for i in request.json["interests"].split(",")],
        "personality": request.json["personality"]
    }

    color = request.json["color"]["hex"]
    
    digest = Digests(
        name = name,
        settings = settings,
        color = color
    )

    db.session.add(digest)
    current_user.digests.append(digest)
    db.session.commit()

    return {
        "response": {"uuid": str(digest.uuid)},
        "ok": True
    }, 200

@core.route("/digest", methods = ['PUT'])
@jwt_required()
def update_digest():

    digest: Digests = Digests.query.filter_by(uuid = request.json["uuid"]).first()

    if not digest:
        return {
            "response": {"message": "Invalid uuid given."},
            "ok": False
        }, 404

    digest.settings = {
        "sources": [SOURCES[s.lower().strip()] for s in request.json["sources"].split(",") if s.lower().strip() in SOURCES.keys()],
        "interests": [i.lower().strip() for i in request.json["interests"].split(",")],
        "personality": request.json["personality"]
    }
    digest.name = request.json["name"]
    digest.color = request.json["color"]["hex"]

    db.session.commit()

    return {
        "response": {"uuid": str(digest.uuid)},
        "ok": True
    }, 200

@core.route("/digest", methods = ['DELETE'])
@jwt_required()
def delete_digest():

    id = get_jwt_identity()
    current_user = Users.query.filter_by(id = id).first()

    digest: Digests = Digests.query.filter_by(uuid = request.json["uuid"]).first()

    if not digest:
        return {
            "response": {"message": "Invalid uuid given."},
            "ok": False
        }, 404

    current_user.digests.remove(digest)

    db.session.commit()

    return {
        "response": {"message": "Deleted digest."},
        "ok": True
    }, 200

@core.route("/user/<id>", methods = ['GET'])
@jwt_required()
def get_user(id):

    user: Users = Users.query.filter_by(id = id).first()
    if not user:
        return {
            "response": {"message": "User not found."},
            "ok": False
        }, 404

    response = user.as_dict()
    response["digests"] = [d.as_dict() for d in user.digests]

    return {
        "response": response,
        "ok": True
    }, 200

@core.route("/user", methods = ['GET'])
@jwt_required()
def get_current_user():

    id = get_jwt_identity()

    return {
        "response": {"id": id},
        "ok": True
    }, 200

@core.route("/newsletter/<uuid>", methods = ['GET'])
@jwt_required()
def get_newsletter(uuid):

    digest: Digests = Digests.query.filter_by(uuid = uuid).first()
    
    if not digest:
        return {
            "response": {"message": "No digest exists"},
            "ok": False
        }, 404
    
    sects, coll, _ = run_openai(
        list(digest.settings["interests"]),
        list(digest.settings["sources"]),
        digest.settings["personality"]
    )
    response = coll
    for sect in sects:
        response[sect["title"]] = sect["body"]

    return {
        "response": response,
        "ok": True
    }, 200

@core.route("/chat", methods = ["GET"])
@jwt_required()
def chat():

    return {
        "response": {"message": "This is dummy text."},
        "ok": True
    }, 200

@core.route("/email", methods = ["GET"])
def email():
    msg = Message('Hello', sender = 'fishtuna908@gmail.com', recipients = ['fishtuna908@gmail.com'])
    msg.html = dedent('''\
        <div>
            <h1>NBA Draft Highlights and Exciting Developments</h1>
            <p>Welcome to our latest sports newsletter, where we dive into the exciting world of professional basketball. From surprising picks in the NBA draft to thrilling developments in the league, there's plenty to discuss. Let's jump right in!</p><div><h2>In the News: Tsitsipas Clarifies Comments, Aussies Discover 'Bazball'</h2><p><p>In a recent Netflix documentary, Break Point, comments made by Stefanos Tsitsipas about Nick Kyrgios at last year's Wimbledon were featured and perceived as controversial. However, Tsitsipas has now clarified that his remarks were misinterpreted <a href="https://www.bbc.co.uk/sport/av/basketball/65997138">(BBC News)</a>. Meanwhile, Australians have recently learned about a 19-year-old basketball sensation named Baz, whose skills have garnered attention <a href="https://www.independent.co.uk/news/espn-ap-nba-san-antonio-spurs-abc-b2363390.html">(Independent)</a>.</p></p></div><div><h2>NBA Draft Highlights: SEC Players, Tennessee's Success, and Historic Night for Penn State</h2><p><p>The 2023 NBA draft took place on Thursday night, and it was a night full of excitement and historic moments. Ten former SEC players were celebrated as draft picks, with six of them going in the first round <a href="https://volswire.usatoday.com/lists/every-tennessee-vols-basketball-player-selected-in-nba-draft-since-2000/">(USA Today)</a>. Tennessee, under the leadership of head coach Rick Barnes, has been a consistent producer of NBA draft selections, with 12 players drafted since 2000 <a href="https://nittanylionswire.usatoday.com/2023/06/24/andrew-funk-lands-nba-summer-league-deal-with-nba-champs/">(USA Today)</a>. Another highlight of the night was the historic moment for Penn State basketball, as Jalen Pickett and Seth Lundy became the first duo from Penn State to be drafted in the same year <a href="https://rolltidewire.usatoday.com/2023/06/23/alabama-basketball-nate-oats-alabama-are-quickly-becoming-an-nba-pipeline/">(USA Today)</a>. Additionally, the Alabama men's basketball program experienced a significant turnaround in terms of NBA draft picks after the hiring of coach Nate Oats in 2019 [7]. The Portland Trail Blazers made a notable selection in Scoot Henderson with the 3rd overall pick <a href="https://deadspin.com/nba-draft-grades-warriors-heat-celtics-mavs-lakers-jazz-1850571706">(Deadspin)</a>. Overall, the draft showcased the talent and potential of these players and the impact they could have in the NBA.</p></p></div><div><h2>NBA News: Rising Star Rayan Rupert Ready for NBA Debut; Defensive Duo Dillon Brooks and Patrick Beverley on the Move</h2><p><p>In the world of professional basketball, exciting developments are taking place as new talents emerge and seasoned players prepare for potential moves. Rayan Rupert, who gained valuable experience in the National Basketball League last season, is now poised to make his mark in the NBA. After being selected <a href="https://bleacherreport.com/articles/10079482-dillon-brooks-patrick-beverleys-top-free-agent-landing-spots-after-2023-nba-draft">(Bleacher Report)</a>, Rupert is eager to showcase his skills and contribute to the league. Meanwhile, two of the NBA's most notorious defensive irritants, Dillon Brooks and Patrick Beverley, are expected to switch teams this summer, generating considerable interest among potential suitors. Brooks and Beverley have established themselves as formidable forces on the defensive end, and their availability in the market is sure to attract attention [2]. Stay tuned for more updates on these intriguing developments in the world of professional basketball!</p></p></div><div><h2>NBA Trade Updates and Player Moves</h2><p><p>In recent NBA news, the Boston Celtics made a three-team trade that brought in Kristaps Porzingis but saw Marcus Smart head to the Memphis Grizzlies <a href="https://www.espn.com/nba/story/_/id/37903852/brad-stevens-porzingis-best-level-sad-see-marcus-smart-go">(ESPN)</a>. Meanwhile, Michigan's Kobe Bufkin, a top breakout guard in college basketball last season, is now a member of the Atlanta Hawks after being drafted 15th overall <a href="https://bleacherreport.com/articles/10075646-kobe-bufkins-draft-scouting-report-pro-comparison-updated-hawks-roster">(Bleacher Report)</a>. Additionally, there are rumors surrounding Ben Simmons' future with the Philadelphia 76ers, with a potential Karl-Anthony Towns trade not being ruled out completely <a href="https://bleacherreport.com/articles/10079641-every-teams-top-target-entering-chaotic-nba-trade-free-agency-season">(Bleacher Report)</a>. On a different note, Bryan Hoeing, a right-hander for the Miami Marlins, was once recruited by Brad Stevens, the current president of basketball operations for the Boston Celtics <a href="https://deadspin.com/marlins-turn-to-bryan-hoeing-in-bid-to-top-pirates-1850573301">(Deadspin)</a>. In disciplinary news, the NBA has suspended Ja Morant of the Memphis Grizzlies for at least 25 games, a decision that has the support of the team's general manager, Zach Kleiman <a href="https://bleacherreport.com/articles/10080415-ja-morants-25-game-suspension-was-appropriate-grizzlies-gm-zach-kleiman-says">(Bleacher Report)</a>. Lastly, following the resignation of West Virginia men's basketball coach Bob Huggins, Kerr Kriisa is re-entering the transfer portal, potentially seeking a new team <a href="https://bleacherreport.com/articles/10080451-3-west-virginia-basketball-players-enter-transfer-portal-after-bob-huggins-exit">(Bleacher Report)</a>. Kentucky star Oscar Tshiebwe, who was not selected in the 2023 NBA draft, will sign a two-way deal with the Indiana Pacers <a href="https://bleacherreport.com/articles/10080459-nba-rumors-oscar-tshiebwe-pacers-agree-to-2-way-contract-after-2023-nba-draft">(Bleacher Report)</a>.</p></p></div><div><h2>Sports News Roundup</h2><p><p>Qatar's Sovereign Wealth Fund Invests in Washington Sports Teams</p>
            <p>Qatar's sovereign wealth fund has recently acquired a 5% stake in the parent company of the NBA's Washington Wizards, NHL's Washington Capitals, and WNBA's Washington Mystics. This deal, worth $4.05 billion, solidifies Qatar's growing presence in the world of sports ownership. <a href="https://time.com/6289525/qatar-washington-wizards-capitals-mystics-sports-ownership/">(Time)</a></p>
            <p>Exciting Developments in the 2023 NBA Draft</p>
            <p>The 2023 NBA draft has already made waves with its first round. The top pick went to a remarkable 7-foot-5 talent, signaling the arrival of a generational player. The draft also saw several trades involving top-10 picks and a surprising slide for one player. The excitement and unpredictability of the draft continue to captivate basketball fans. <a href="https://www.espn.com/nba/story/_/id/37893062/nba-draft-2023-surprises-winners-losers-first-round">(ESPN)</a></p>
            <p>Fashion and Basketball Collide at the NBA Draft</p>
            <p>The NBA draft is not just about the players; it's also a showcase for fashion. This year, the intersection of basketball and menswear delivered some delightful gifts. Fans witnessed stylish outfits and unique fashion choices, making the draft a Christmas morning for fashion enthusiasts. <a href="https://www.gq.com/gallery/2023-nba-draft-biggest-fits">(GQ Magazine)</a></p>
            <p>Rediscovering the New Balance 550</p>
            <p>The New Balance 550 has been making waves in the world of sneakers, thanks to its collaboration with AimÃ© Leon Dore. However, many are surprised to learn that this basketball sneaker actually first hit the shelves in 1989. The enduring popularity of the New Balance 550 proves that classic designs can stand the test of time. <a href="https://www.highsnobiety.com/p/new-balance-550-thisisneverthat/">(Highsnobiety)</a></p></p></div><div><h2>Surprising Picks and Versatile Players in the 2023 NBA Draft</h2><p><p>The 2023 NBA draft saw some unexpected selections and the acquisition of versatile players who are poised to make an impact in the league. The Golden State Warriors raised eyebrows when they chose Brandin Podziemski with the 19th overall pick. Despite the skepticism, Podziemski's confidence and skill set suggest that he has the potential to be a valuable asset for the team <a href="https://bleacherreport.com/articles/10080520-warriors-brandin-podziemski-im-a-triple-double-guy-in-the-nba-in-a-few-seasons">(Bleacher Report)</a>. The New Orleans Pelicans made a smart move by selecting Jordan Hawkins from Connecticut with the No. 14 overall pick. Hawkins is known for his versatility and ability to make shots, making him a valuable addition to the Pelicans' roster <a href="https://bleacherreport.com/articles/10075642-jordan-hawkins-draft-scouting-report-pro-comparison-updated-pelicans-roster">(Bleacher Report)</a>. Another notable pick was Keyonte George, a shooting guard from Baylor, who was chosen by the Utah Jazz with the No. 16 overall pick. George's skills and potential have been recognized by Bleacher Report Draft Expert Jonathan Wasserman, making him an exciting prospect for the Jazz <a href="https://bleacherreport.com/articles/10075645-keyonte-georges-draft-scouting-report-pro-comparison-updated-jazz-roster">(Bleacher Report)</a>.</p></p></div><div><h2>Victor Wembanyama: The Phenomenal French Rookie</h2><p><p>In a highly anticipated move, the San Antonio Spurs selected Victor Wembanyama as the first overall pick in the 2023 NBA Draft <a href="https://www.theguardian.com/sport/2023/jun/22/future-arrives-as-spurs-pick-wembanyama-with-first-pick-of-nba-draft">(The Guardian)</a>. The 19-year-old French phenom is considered the most coveted draft prospect since LeBron James and Kareem Abdul-Jabbar <a href="https://bleacherreport.com/articles/10080221-biggest-winners-and-losers-from-2023-nba-draft-night">(Bleacher Report)</a>. Wembanyama's arrival in the United States was met with excitement as he experienced his first subway ride in New York City and threw out the first pitch at a baseball game <a href="https://deadspin.com/spurs-select-victor-wembanyama-first-overall-in-nba-dra-1850568337">(Deadspin)</a>. The 7ft 4in rookie has already captured the attention of fans and experts alike, with comparisons being drawn to some of the game's greatest players <a href="https://bleacherreport.com/articles/10080221-biggest-winners-and-losers-from-2023-nba-draft-night">(Bleacher Report)</a>. The Dallas Mavericks also made waves on draft night by trading Dvis Bertns' contract to the Oklahoma City Thunder <a href="https://bleacherreport.com/articles/10080549-spurs-popovich-victor-wembanyama-shouldnt-be-compared-to-lebron-kobe-duncan">(Bleacher Report)</a>. Meanwhile, San Antonio Spurs head coach Gregg Popovich remains unfazed by the comparisons and is focused on nurturing Wembanyama's unique talent [8]. With Wembanyama officially joining the Spurs, the era of this exceptional French rookie has begun <a href="https://www.espn.com/fantasy/basketball/story/_/id/37904164/nba-draft-picks-fantasy-basketball-rookies-biggest-impact-2023-24">(ESPN)</a>.</p></p></div><h1>Conclusion</h1><p>As we wrap up this edition of our sports newsletter, we've covered a range of topics, from the NBA draft highlights to intriguing player moves and even fashion at the draft. The basketball world is buzzing with excitement, and we can't wait to see how these stories unfold. Stay tuned for more updates and enjoy the thrilling action on the court!</p>
        </div>''')
    mail.send(msg)
    return "Sent"