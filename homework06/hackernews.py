from bottle import (
    route, run, template, request, redirect
)
import string
from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    label = request.query.label
    id_ = request.query.id
    s = session()
    news = s.query(News).get(id_)
    news.label = label
    s.commit()
    redirect("/news")


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


@route("/update")
def update_news():
    new_news = get_news("https://news.ycombinator.com/newest", 1)
    s = session()
    for i in new_news:
        title = i["title"]
        author = i["author"]
        exists = s.query(News).filter(News.title == title and News.author == author).first()
        if exists:
            continue
        news = News(**i)
        s.add(news)
        s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    model = NaiveBayesClassifier()
    s = session()
    X_train = []
    y_train = []
    cl_news = s.query(News).filter(News.label != None).all()
    for news in cl_news:
        X_train.append(clean(news.title).lower())
        y_train.append(news.label)
    model.fit(X_train, y_train)
    X = []
    notcl_news = s.query(News).filter(News.label == None).all()
    for news in notcl_news:
        X.append(clean(news.title).lower())
    predicts = model.predict(X)
    for label, news in zip(predicts, notcl_news):
        news.label = label
    s.commit()
    ans = []
    classes = ["good", "maybe", "never"]
    for cl in classes:
        for news in notcl_news:
            if news.label == cl:
                ans.append(news)
    return ans


@route('/recommendations')
def recommendations():
    classified_news = classify_news()
    return template('recs_template', rows=classified_news)


if __name__ == "__main__":
    run(host="localhost", port=8080)