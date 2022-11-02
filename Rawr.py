"""Reddit API Wrapper wRapper (RAWR) is a wrapper around praw providing a
friendly interface for data scraping.

Examples
--------
One can get the 10 top posts over the last year from the UPenn subreddit with
the following sequence:

>>> from Rawr import Rawr
>>> rawr = Rawr()
>>> sub = rawr.get_subreddit()
>>> list(sub.get_posts(limit=10, time_filter="year", order_by="top"))
[Submission(summary='How an Ivy League School Turned Against a Student', ...), Submission(summary='I’m tired of the fetishization of M&T students.', ...), ...]
"""
from __future__ import annotations
import os, praw, dataclasses as dc
from typing import Optional, Generator, Union
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

@dc.dataclass
class Award(object):
    name: str
    count: int
    coin_price: int
    coin_reward: int
    description: str

    @staticmethod
    def _make(award: dict):
        return Award(
            name=award["name"],
            count=award["count"],
            coin_price=award["coin_price"],
            coin_reward=award["coin_reward"],
            description=award["description"]
        )

@dc.dataclass
class Comment(object):
    text: str
    author_name: str
    score: int
    up_votes: int
    down_votes: int
    created: datetime
    awards: "list[Award]"
    depth: int
    by_op: bool
    url: str

    @staticmethod
    def _make(comment: praw.reddit.models.Comment) -> Comment:
        return Comment(
            text=comment.body,
            author_name=None if comment.author is None else comment.author.name,
            score=comment.score,
            up_votes=comment.ups,
            down_votes=comment.downs,
            created=datetime.utcfromtimestamp(comment.created_utc),
            awards=[Award._make(award) for award in comment.all_awardings],
            depth=comment.depth,
            by_op=comment.is_submitter,
            url=comment.permalink
        )

@dc.dataclass
class Submission(object):
    _client: Union[praw.reddit.models.Submission, praw.reddit.models.Comment]
    summary: str
    text: str
    author_name: str
    comment_count: int
    score: int
    up_votes: int
    down_votes: int
    flair: str
    created: datetime
    awards: "list[Award]"
    url: str

    def get_comments(self, limit: int = 50, order_by: str = "confidence") -> Generator[Comment, None, None]:
        """Yields the first comments returned by reddit.
        
        Parameters
        ----------
        limit: int
            Maximum number of comments to return
        order_by: str
            Ordering scheme for comments. Can be one of ["confidence",
            "controversial", "new", "old", "q&a", and "top"].
        
        Yields
        ------
        Comment
            Object containing comment details
            
        Examples
        --------
        >>> list(submission.get_comments(3))
        [Comment(text='[Compilation of similar threads](https://www.reddit.com/r/UPenn/comments/ml2r10/official_admitted_student_faq_and_can_i_talk_to/gtj7s1z/)', author_name='FailureAintFatal', ...), Comment(text='Honestly, after I got accepted I had the same fear from reddit. I was scared...', author_name='Trick_Commission_492'), ...]"""
        # Identify submission type and set parameters accordingly
        self._client.comment_limit = limit
        self._client.comment_sort = order_by
        comment_obj = self._client.comments

        def process_comment(comment: praw.reddit.models.Comment) -> Submission:
            return Comment._make(comment)
        
        for obj in comment_obj.list():
            # Case on whether or not this is a top level comment
            if isinstance(obj, praw.reddit.models.Comment):
                yield process_comment(obj)
            else:
                for comment in obj.comments():
                    yield process_comment(comment)
                    
    @staticmethod
    def _make(submission: praw.reddit.models.Submission):
        return Submission(
            _client=submission,
            summary=submission.title,
            text="".join(submission.selftext),
            author_name=None if submission.author is None else submission.author.name,
            comment_count=submission.num_comments,
            score=submission.score,
            up_votes=submission.ups,
            down_votes=submission.downs,
            flair=submission.link_flair_text,
            created=datetime.utcfromtimestamp(submission.created_utc),
            awards=[Award._make(award) for award in submission.all_awardings],
            url=submission.permalink
        )


@dc.dataclass
class Subreddit(object):
    _client: praw.reddit.models.Subreddit
    display_name: str
    title: str
    description: str
    subscriber_count: int
    created: datetime
    url: str

    def get_posts(self, limit: int = 50, time_filter: Optional[str] = None, order_by: str = "hot") -> Generator[Submission, None, None]:
        """Yields the first returned posts by Reddit when ordering by the input.
        
        Parameters
        ----------
        limit: int
            Maximum number of posts to return
        time_filter: Optional[str]
            If not "all", only returns posts within the most recent period of
            the specified time chunk. Can be one of ["all", "day", "hour",
            "month", "week", or "year"]. Cannot be passed if `order_by` is "hot".
        order_by: str
            Ordering scheme for posts. Can be one of ["hot", "top",
            "controversial", "new"]

        Yields
        ------
        Post
            Object representing post instance

        Examples
        --------
        >>> list(subreddit.get_posts(1))
        [Submission(summary='Is UPenn really as awful as Reddit makes it seem?!?!', ...)]

        Instead of getting the hottest posts, one could get the top 5 posts over
        the last year

        >>> list(subreddit.get_posts(5))
        [Submission(summary='How an Ivy League School Turned Against a Student', ...), Submission(summary='I’m tired of the fetishization of M&T students.', ...), ...]
        """
        if order_by == "hot"  and time_filter is not None:
            raise ValueError(f'If order_by is "hot", time filter must be `None`. Received {time_filter}.')

        kwargs = dict()
        if limit is not None:
            kwargs["limit"] = limit
        if time_filter is not None:
            kwargs["time_filter"] = time_filter

        if order_by == "hot":
            get_method = self._client.hot
        elif order_by == "top":
            get_method = self._client.top
        elif order_by == "controversial":
            get_method = self._client.controversial
        elif order_by == "new":
            get_method = self._client.new
        else:
            raise ValueError(f'Expected one of ["hot", "top", "controversial", "new"] for order_by, received {order_by}')

        for post in get_method(**kwargs):
            yield Submission._make(post)


class Rawr(object):
    """Wrapper around praw permitting easy interaction with Reddit API."""

    def __init__(self, client_id: Optional[str] = None, secret: Optional[str] = None, user_agent: Optional[str] = None):
        """Initializes the API wrapper.
        
        Parameters
        ----------
        client_id: Optional[str]
            Client ID associated with Reddit app. If `None`, looks in environment
            variables for 'CLIENT_ID'.
        secret: Optional[str]
            Secret associated with Reddit app. If `None`, looks in environment
            variables for 'SECRET'.
        user_agent: Optional[str]
            User agent associated with Reddit app. If `None`, looks in environment
            variables for 'USER_AGENT'."""
        # Validate inputs
        client_id = os.getenv('CLIENT_ID') if client_id is None else client_id
        secret = os.getenv('SECRET') if secret is None else secret
        user_agent = os.getenv('USER_AGENT') if user_agent is None else user_agent
        if client_id is None:
            raise ValueError(f"Missing client_id! Make sure to pass it or define 'CLIENT_ID' in your environment!")
        if secret is None:
            raise ValueError(f"Missing secret! Make sure to pass it or define 'SECRET' in your environment!")
        if user_agent is None:
            raise ValueError(f"Missing user_agent! Make sure to pass it or define 'USER_AGENT' in your environment!")

        self.client = praw.Reddit(client_id=client_id, client_secret=secret, user_agent=user_agent)

    def get_subreddit(self, subreddit_name: str) -> Subreddit:
        """Returns the Subreddit object associated with the input name.
        
        Parameters
        ----------
        subreddit_name: str
            Name of subreddit to get
            
        Examples
        --------
        >>> rawr.get_subreddit('upenn')
        Subreddit(_client=Subreddit(display_name='UPenn'), display_name='upenn', ...)
        """
        praw_sr: praw.reddit.models.Subreddit = self.client.subreddit(subreddit_name)
        return Subreddit(
            _client = praw_sr,
            display_name=praw_sr.display_name,
            title=praw_sr.title,
            description=''.join(praw_sr.description),
            subscriber_count=praw_sr.subscribers,
            created=datetime.utcfromtimestamp(praw_sr.created_utc),
            url=f"https://reddit.com{praw_sr.url}"
        )
