# -*- coding: utf-8 -*-

"""
gitsuggest.suggest
~~~~~~~~~~~~~~~~~~

This module contains the primary objects that power GitSuggest.
"""

import itertools
from collections import defaultdict
from operator import attrgetter
from os import path

import enchant
import github
import nltk
from gensim import corpora, models
from nltk.tokenize import RegexpTokenizer


class GitSuggest(object):
    """Class to suggest git repositories for a user."""

    # Length of description of a repository over which it is a high chance
    # that it is a spammy repository.
    MAX_DESC_LEN = 300

    def __init__(self,
                 username=None,
                 password=None,
                 token=None,
                 deep_dive=False):
        """Constructor.

        Username and password is used to get an authenticated handle which has
        a higher rate limit when compared to unauthenticated handle which will
        have much lesser rate limit.

        :param username: Github username.
        :param password: Github password.
        :param token: Github access token.
        :param deep_dive: When set to True considers the repositories people
                          you follow have starred along with the ones you have
                          starred.
        """
        if token:
            self.github = github.Github(token)
            username = self.github.get_user().login
            assert username is not None, 'Invalid token'
        else:
            assert username is not None, "Suggest cannot work without username"
            # Github handle.
            if password is not None and password != '':
                self.github = github.Github(username, password)
            else:
                self.github = github.Github()

        self.deep_dive = deep_dive

        # Populate repositories to be used for generating suggestions.
        self.user_starred_repositories = list()
        self.user_following_starred_repositories = list()
        self.__populate_repositories_of_interest(username)

        # Construct LDA model.
        self.lda_model = None
        self.__construct_lda_model()

        # Suggested repository set.
        self.suggested_repositories = None
        # Search for repositories is the costliest operation so defer it as
        # much as possible.

    @staticmethod
    def get_unique_repositories(repo_list):
        """Method to create unique list of repositories from the list of
        repositories given.

        :param repo_list: List of repositories which might contain duplicates.
        :return: List of repositories with no duplicate in them.
        """
        unique_list = list()
        included = defaultdict(lambda: False)
        for repo in repo_list:
            if not included[repo.full_name]:
                unique_list.append(repo)
                included[repo.full_name] = True
        return unique_list

    @staticmethod
    def minus(repo_list_a, repo_list_b):
        """Method to create a list of repositories such that the repository
        belongs to repo list a but not repo list b.

        In an ideal scenario we should be able to do this by set(a) - set(b)
        but as GithubRepositories have shown that set() on them is not reliable
        resort to this until it is all sorted out.

        :param repo_list_a: List of repositories.
        :param repo_list_b: List of repositories.
        """
        included = defaultdict(lambda: False)

        for repo in repo_list_b:
            included[repo.full_name] = True

        a_minus_b = list()
        for repo in repo_list_a:
            if not included[repo.full_name]:
                included[repo.full_name] = True
                a_minus_b.append(repo)

        return a_minus_b

    def __populate_repositories_of_interest(self, username):
        """Method to populate repositories which will be used to suggest
        repositories for the user. For this purpose we use two kinds of
        repositories.

        1. Repositories starred by user him/herself.
        2. Repositories starred by the users followed by the user.

        :param username: Username for the user for whom repositories are being
                         suggested for.
        """
        # Handle to the user to whom repositories need to be suggested.
        user = self.github.get_user(username)

        # Procure repositories starred by the user.
        self.user_starred_repositories.extend(user.get_starred())

        # Repositories starred by users followed by the user.
        if self.deep_dive:
            for following_user in user.get_following():
                self.user_following_starred_repositories.extend(
                    following_user.get_starred())

    def __get_interests(self):
        """Method to procure description of repositories the authenticated user
        is interested in.

        We currently attribute interest to:
        1. The repositories the authenticated user has starred.
        2. The repositories the users the authenticated user follows have
        starred.

        :return: List of repository descriptions.
        """
        # All repositories of interest.
        repos_of_interest = itertools.chain(
            self.user_starred_repositories,
            self.user_following_starred_repositories)

        # Extract descriptions out of repositories of interest.
        repo_descriptions = [repo.description for repo in repos_of_interest]
        return list(set(repo_descriptions))

    def __get_words_to_ignore(self):
        """Compiles list of all words to ignore.

        :return: List of words to ignore.
        """
        # Stop words in English.
        english_stopwords = nltk.corpus.stopwords.words('english')

        here = path.abspath(path.dirname(__file__))

        # Languages in git repositories.
        git_languages = []
        with open(path.join(here, 'gitlang/languages.txt'), 'r') as langauges:
            git_languages = [line.strip() for line in langauges]

        # Other words to avoid in git repositories.
        words_to_avoid = []
        with open(path.join(here, 'gitlang/others.txt'), 'r') as languages:
            words_to_avoid = [line.strip() for line in languages]

        return list(itertools.chain(english_stopwords, git_languages,
                                    words_to_avoid))

    def __get_words_to_consider(self):
        """Compiles list of all words to consider.

        :return: List of words to consider.
        """
        return enchant.Dict('en_US')

    def __clean_and_tokenize(self, doc_list):
        """Method to clean and tokenize the document list.

        :param doc_list: Document list to clean and tokenize.
        :return: Cleaned and tokenized document list.
        """
        # Some repositories fill entire documentation in description. We ignore
        # such repositories for cleaner tokens.
        doc_list = filter(
            lambda x: x is not None and len(x) <= GitSuggest.MAX_DESC_LEN,
            doc_list)

        cleaned_doc_list = list()

        # Regular expression to remove out all punctuations, numbers and other
        # un-necessary text substrings like emojis etc.
        tokenizer = RegexpTokenizer(r'[a-zA-Z]+')

        # Get stop words.
        stopwords = self.__get_words_to_ignore()

        # Get english words.
        dict_words = self.__get_words_to_consider()

        for doc in doc_list:
            # Lowercase doc.
            lower = doc.lower()

            # Tokenize removing numbers and punctuation.
            tokens = tokenizer.tokenize(lower)

            # Include meaningful words.
            tokens = [tok for tok in tokens if dict_words.check(tok)]

            # Remove stopwords.
            tokens = [tok for tok in tokens if tok not in stopwords]

            # Filter Nones if any are introduced.
            tokens = [tok for tok in tokens if tok is not None]

            cleaned_doc_list.append(tokens)

        return cleaned_doc_list

    def __construct_lda_model(self):
        """Method to create LDA model to procure list of topics from.

        We do that by first fetching the descriptions of repositories user has
        shown interest in. We tokenize the hence fetched descriptions to
        procure list of cleaned tokens by dropping all the stop words and
        language names from it.

        We use the cleaned and sanitized token list to train LDA model from
        which we hope to procure topics of interests to the authenticated user.
        """
        # Fetch descriptions of repos of interest to authenticated user.
        repos_of_interest = self.__get_interests()

        # Procure clean tokens from the descriptions.
        cleaned_tokens = self.__clean_and_tokenize(repos_of_interest)

        # Setup LDA requisites.
        dictionary = corpora.Dictionary(cleaned_tokens)
        corpus = [dictionary.doc2bow(text) for text in cleaned_tokens]

        # Generate LDA model
        self.lda_model = models.ldamodel.LdaModel(
            corpus, num_topics=1, id2word=dictionary, passes=10)

    def __get_query_for_repos(self, term_count=5):
        """Method to procure query based on topics authenticated user is
        interested in.

        :param term_count: Count of terms in query.
        :return: Query string.
        """
        repo_query_terms = list()
        for term in self.lda_model.get_topic_terms(0, topn=term_count):
            repo_query_terms.append(self.lda_model.id2word[term[0]])
        return ' '.join(repo_query_terms)

    def __get_repos_for_query(self, query):
        """Method to procure git repositories for the query provided.

        IMPORTANT NOTE: This is the costliest of all the calls hence keep this
        to a minimum.

        :param query: String representing the repositories intend to search.
        :return: Iterator for repositories found using the query.
        """
        return self.github.search_repositories(query,
                                               'stars',
                                               'desc').get_page(0)

    def get_suggested_repositories(self):
        """Method to procure suggested repositories for the user.

        :return: Iterator to procure suggested repositories for the user.
        """
        if self.suggested_repositories is None:
            # Procure repositories to suggest to user.
            repository_set = list()
            for term_count in range(5, 2, -1):
                query = self.__get_query_for_repos(term_count=term_count)
                repository_set.extend(self.__get_repos_for_query(query))

            # Remove repositories authenticated user is already interested in.
            catchy_repos = GitSuggest.minus(repository_set,
                                            self.user_starred_repositories)

            # Filter out repositories with too long descriptions. This is a
            # measure to weed out spammy repositories.
            filtered_repos = []

            if len(catchy_repos) > 0:
                for repo in catchy_repos:
                    if repo is not None and \
                       repo.description is not None and \
                       len(repo.description) <= GitSuggest.MAX_DESC_LEN:
                        filtered_repos.append(repo)

            # Present the repositories, highly starred to not starred.
            filtered_repos = sorted(filtered_repos,
                                    key=attrgetter('stargazers_count'),
                                    reverse=True)

            self.suggested_repositories = GitSuggest.get_unique_repositories(
                filtered_repos)

        # Return an iterator to help user fetch the repository listing.
        for repository in self.suggested_repositories:
            yield repository
